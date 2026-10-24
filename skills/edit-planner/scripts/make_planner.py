#!/usr/bin/env python3
"""Build the edit-planning page for a cut video.

Usage:
  make_planner.py <words.json> <out.html> [--cut-report <video>_cut.cut.json] [--video <cut.mp4>]
                  [--title "..."] [--scenes scenes.json] [--max-scene 8] [--min-scene 3.5] [--open]

- words.json: word-level transcript of the RAW video (raw-cut's transcribe.sh output).
- --cut-report: raw-cut's report. Word times are remapped onto the CUT timeline, and words that were cut out are dropped.
  Without it, the times are used as-is (e.g. the words.json already belongs to the cut video).
- --scenes: optional scenes.json ([{"start","end","script","type","plan"}]) to use instead of auto-splitting,
  e.g. after Claude has grouped the script into beats and pre-suggested scene types.
Auto-split: sentence boundaries; a scene closes once it is >= min-scene seconds long and the next sentence would
push it past max-scene, or at a pause > 0.8 s. Every scene starts as type "captions".
"""
import argparse, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "assets", "planner-template.html")


def remap(words, report):
    """Map raw-timeline words onto the cut timeline. Kept words come from the report (exact);
    each is placed in its nearest kept segment, because whisper times can sit inside removed gaps."""
    segs = report["segments"]
    keep = set(report.get("kept_words", range(len(words))))
    offs, acc = [], 0.0
    for s, e in segs:
        offs.append(acc); acc += e - s
    out = []
    for k, w in enumerate(words):
        if k not in keep:
            continue
        mid = (w["s"] + w["e"]) / 2
        j = min(range(len(segs)), key=lambda i: 0 if segs[i][0] <= mid <= segs[i][1] else min(abs(mid - segs[i][0]), abs(mid - segs[i][1])))
        s, e = segs[j]; o = offs[j]
        ns = o + min(max(w["s"], s), e) - s
        ne = o + min(max(w["e"], s), e) - s
        out.append({"w": w["w"], "s": round(ns, 3), "e": round(max(ne, ns + 0.02), 3)})
    out.sort(key=lambda w: w["s"])
    return out, acc


def split(words, max_scene, min_scene):
    sents, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        gap = words[i + 1]["s"] - w["e"] if i + 1 < len(words) else 0
        if re.search(r"[.!?]['\"]?$", w["w"]) or gap > 0.8:
            sents.append((cur, gap)); cur = []
    if cur: sents.append((cur, 0))
    scenes, buf = [], []
    for sent, gap in sents:
        if buf:
            dur_now = buf[-1]["e"] - buf[0]["s"]
            dur_with = sent[-1]["e"] - buf[0]["s"]
            if dur_now >= min_scene and dur_with > max_scene:
                scenes.append(buf); buf = []
        buf = buf + sent
        if gap > 0.8 and buf[-1]["e"] - buf[0]["s"] >= min_scene:
            scenes.append(buf); buf = []
    if buf: scenes.append(buf)
    return [{"id": f"s{i+1}", "start": round(sc[0]["s"], 2), "end": round(sc[-1]["e"], 2),
             "script": " ".join(w["w"] for w in sc), "type": "captions", "plan": ""} for i, sc in enumerate(scenes)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("words"); ap.add_argument("out")
    ap.add_argument("--cut-report"); ap.add_argument("--video", default="")
    ap.add_argument("--title"); ap.add_argument("--scenes")
    ap.add_argument("--max-scene", type=float, default=8.0); ap.add_argument("--min-scene", type=float, default=3.5)
    ap.add_argument("--open", action="store_true")
    a = ap.parse_args()

    words = json.load(open(a.words))
    duration = 0.0
    if a.cut_report:
        words, duration = remap(words, json.load(open(a.cut_report)))
    elif words:
        duration = words[-1]["e"]
    if a.scenes:
        scenes = json.load(open(a.scenes))
        for i, s in enumerate(scenes):
            s.setdefault("id", f"s{i+1}"); s.setdefault("type", "captions"); s.setdefault("plan", "")
    else:
        scenes = split(words, a.max_scene, a.min_scene)
    if not scenes:
        sys.exit("no words to build scenes from")

    video = os.path.basename(a.video) if a.video else ""
    title = a.title or (os.path.splitext(video)[0] if video else os.path.splitext(os.path.basename(a.out))[0])
    project = re.sub(r"[^a-z0-9]+", "-", (title + "-" + str(round(duration, 1))).lower()).strip("-")
    data = {"project": project, "title": title, "video": video, "duration": round(duration, 2),
            "style": {"mainColor": "#3B7BFF", "font": "Inter", "fontColor": "#FFFFFF"}, "scenes": scenes}
    html = open(TEMPLATE, encoding="utf-8").read()
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = html.replace("/*__PLAN_DATA__*/", blob)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    open(a.out, "w", encoding="utf-8").write(html)
    print(f"{len(scenes)} scenes, {duration:.1f}s -> {a.out}")
    for i, s in enumerate(scenes, 1):
        print(f"  {i:>2}. {s['start']:6.2f}-{s['end']:6.2f}  {s['script'][:90]}")
    if a.open and sys.platform == "darwin":
        subprocess.run(["open", a.out])


if __name__ == "__main__":
    main()
