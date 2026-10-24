#!/usr/bin/env python3
"""Cut a raw video down to the kept words: every silence and every bad take removed, tight padding.

Usage:
  cut.py <video> <words.json> <out.mp4> [--keep keep.json] [--pad 0.02] [--min-silence 0.15]

keep.json (written after reading the transcript) lists the word ranges to KEEP, inclusive word indices:
  {"keep": [[0, 41], [57, 130], [131, 210]]}
Omit --keep to keep every word (silence removal only).

How a cut is placed:
  1. Kept words are grouped into runs of consecutive indices.
  2. Each run's start/end is snapped to the real speech onset/offset in the waveform, because whisper word
     times drift 50-100 ms. Otherwise a 20 ms pad would clip word starts and endings.
  3. Any silence longer than --min-silence inside a run is removed too.
  4. --pad (default 20 ms) is added around every kept piece, and a 5 ms audio fade at every cut prevents clicks.
Stdlib only, plus ffmpeg/ffprobe on PATH (or set FFMPEG / FFPROBE).
"""
import argparse, array, json, math, os, shutil, subprocess, sys, tempfile

FFMPEG = os.environ.get("FFMPEG") or shutil.which("ffmpeg") or "/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg"
FFPROBE = os.environ.get("FFPROBE") or shutil.which("ffprobe") or "/opt/homebrew/opt/ffmpeg-full/bin/ffprobe"
SR, HOP = 16000, 0.005  # 5 ms analysis frames


def probe(path):
    out = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration:stream=codec_type,avg_frame_rate",
                          "-of", "json", path], capture_output=True, text=True, check=True).stdout
    d = json.loads(out)
    dur = float(d["format"]["duration"])
    fps = next((s["avg_frame_rate"] for s in d["streams"] if s["codec_type"] == "video"), "30/1")
    try:
        n_, d_ = (float(x) for x in fps.split("/")); f = n_ / d_ if d_ else 30.0
    except ValueError:
        f = 30.0
    # phone footage is often VFR with odd averages: snap to the nearest standard rate
    std = {23.976: "24000/1001", 24: "24", 25: "25", 29.97: "30000/1001", 30: "30", 50: "50", 59.94: "60000/1001", 60: "60"}
    fps = std[min(std, key=lambda k: abs(k - f))] if f > 1 else "30"
    return dur, fps


def energy_db(path):
    raw = subprocess.run([FFMPEG, "-nostdin", "-v", "error", "-i", path, "-vn", "-ac", "1", "-ar", str(SR),
                          "-f", "s16le", "-"], capture_output=True, check=True).stdout
    a = array.array("h"); a.frombytes(raw[: len(raw) // 2 * 2])
    n = int(SR * HOP); out = []
    for i in range(0, len(a) - n + 1, n):
        seg = a[i:i + n]; ms = sum(x * x for x in seg) / n
        out.append(10 * math.log10(ms + 1e-9) - 90.3)  # dBFS
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("words"); ap.add_argument("out")
    ap.add_argument("--keep", help="keep.json with inclusive word-index ranges")
    ap.add_argument("--pad", type=float, default=0.02)
    ap.add_argument("--min-silence", type=float, default=0.18, help="silences longer than this are removed")
    ap.add_argument("--thresh-db", type=float, default=None, help="speech threshold dBFS (default: noise floor + 6)")
    ap.add_argument("--crf", type=int, default=16)
    a = ap.parse_args()

    words = json.load(open(a.words))
    if a.keep:
        keep = set()
        for lo, hi in json.load(open(a.keep))["keep"]:
            keep.update(range(int(lo), int(hi) + 1))
    else:
        keep = set(range(len(words)))
    dur, fps = probe(a.video)

    print("analysing audio energy...", file=sys.stderr)
    db = energy_db(a.video)
    nf = len(db)
    floor = sorted(db)[int(nf * 0.10)] if nf else -70
    thr = a.thresh_db if a.thresh_db is not None else max(floor + 6, -60)
    loud = [x > thr for x in db]
    F = lambda t: max(0, min(nf - 1, int(t / HOP)))

    # 1. runs of consecutive kept words
    idx = sorted(i for i in keep if 0 <= i < len(words))
    runs, cur = [], []
    for i in idx:
        if cur and i != cur[-1] + 1:
            runs.append(cur); cur = []
        cur.append(i)
    if cur: runs.append(cur)

    # 2. snap run edges to the waveform
    pieces = []
    for r in runs:
        s, e = words[r[0]]["s"], words[r[-1]]["e"]
        f = F(s)
        if loud[f]:                       # speech already under way: walk back to the onset (<= 500 ms; whisper can be ~400 ms late)
            lim = F(s - 0.50)
            while f > lim and loud[f - 1]: f -= 1
            if f == lim and loud[f]:      # no silence (words run together): cut in the quietest dip
                f = min(range(F(s - 0.50), F(s + 0.04) + 1), key=lambda k: db[k])
        else:                             # whisper started early: walk forward to the onset (<= 150 ms)
            lim = F(s + 0.15)
            while f < lim and not loud[f]: f += 1
        s2 = f * HOP
        g = F(e)
        if loud[g]:                       # tail still sounding: walk forward to the offset (<= 500 ms)
            lim = F(e + 0.50)
            while g < lim and loud[g + 1 if g + 1 < nf else g]: g += 1
            if g == lim and loud[g] and g < nf - 1:   # runs straight into the next word: quietest dip
                g = min(range(F(e - 0.04), F(e + 0.50) + 1), key=lambda k: db[k])
        else:                             # whisper ended late: walk back to the offset (<= 150 ms)
            lim = max(F(e - 0.15), F(s2))
            while g > lim and not loud[g]: g -= 1
        e2 = (g + 1) * HOP
        if e2 <= s2: s2, e2 = s, e
        # 3. remove silences inside the run
        #    (never inside a word: quiet consonants/closures sit below the threshold too)
        inner = [(words[i]["s"] + 0.08, words[i]["e"] - 0.08) for i in r]
        start, quiet = F(s2), 0
        for k in range(F(s2), F(e2) + 1):
            if loud[k]:
                gs, ge = (k - quiet) * HOP, k * HOP
                if quiet * HOP >= a.min_silence and not any(ws <= gs and ge <= we for ws, we in inner):
                    pieces.append((start * HOP, gs)); start = k
                quiet = 0
            else:
                quiet += 1
        pieces.append((start * HOP, e2))

    # 4. pad + merge
    segs = []
    for s, e in pieces:
        s, e = max(0.0, s - a.pad), min(dur, e + a.pad)
        if e - s < 0.04: continue
        if segs and s <= segs[-1][1]: segs[-1][1] = max(segs[-1][1], e)
        else: segs.append([s, e])
    if not segs: sys.exit("nothing to keep")

    kept = sum(e - s for s, e in segs)
    # edges that still land on speech (possible clipped word): flag for a listen-check
    warn = []
    for s, e in segs:
        if s > 0.05 and db[F(s)] > thr + 10: warn.append(f"in  {s:.2f}s ({db[F(s)]:.0f} dB)")
        if e < dur - 0.05 and db[F(e) - 1] > thr + 10: warn.append(f"out {e:.2f}s ({db[F(e) - 1]:.0f} dB)")
    fade = 0.005
    lines = []
    n = len(segs)
    lines.append(f"[0:v]split={n}" + "".join(f"[v{i}]" for i in range(n)) + ";")
    lines.append(f"[0:a]asplit={n}" + "".join(f"[a{i}]" for i in range(n)) + ";")
    for i, (s, e) in enumerate(segs):
        d = e - s
        lines.append(f"[v{i}]trim=start={s:.3f}:end={e:.3f},setpts=PTS-STARTPTS[vv{i}];")
        lines.append(f"[a{i}]atrim=start={s:.3f}:end={e:.3f},asetpts=PTS-STARTPTS,"
                     f"afade=t=in:d={fade},afade=t=out:st={max(0, d - fade):.3f}:d={fade}[aa{i}];")
    lines.append("".join(f"[vv{i}][aa{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[v][a]")
    tmp = tempfile.mkdtemp()
    fs = os.path.join(tmp, "cut.txt"); open(fs, "w").write("\n".join(lines))
    cmd = [FFMPEG, "-nostdin", "-v", "error", "-y", "-i", a.video, "-/filter_complex", fs, "-map", "[v]", "-map", "[a]",
           "-c:v", "libx264", "-preset", "medium", "-crf", str(a.crf), "-pix_fmt", "yuv420p", "-fps_mode", "cfr", "-r", fps,
           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", a.out]
    print(f"rendering {n} pieces...", file=sys.stderr)
    subprocess.run(cmd, check=True)
    shutil.rmtree(tmp, ignore_errors=True)

    report = {"source": a.video, "source_duration": round(dur, 2), "output_duration": round(kept, 2),
              "removed_seconds": round(dur - kept, 2), "removed_percent": round(100 * (dur - kept) / dur, 1),
              "pieces": len(segs), "pad": a.pad, "loud_edges": warn, "threshold_db": round(thr, 1),
              "dropped_words": " ".join(w["w"] for k, w in enumerate(words) if k not in keep),
              "kept_words": sorted(k for k in keep if 0 <= k < len(words)),
              "segments": [[round(s, 3), round(e, 3)] for s, e in segs]}
    rp = os.path.splitext(a.out)[0] + ".cut.json"
    json.dump(report, open(rp, "w"), indent=1)
    print(f"{dur:.1f}s -> {kept:.1f}s ({report['removed_percent']}% removed), {n} pieces. Report: {rp}")
    if warn: print("LISTEN-CHECK these cuts (edge lands on loud audio):\n  " + "\n  ".join(warn))


if __name__ == "__main__":
    main()
