#!/usr/bin/env bash
# Word-level transcript of a raw video with whisper.cpp.
# Usage: transcribe.sh <video> <out_words.json> [lang]
#   lang: en (default, uses the English model) or any whisper code / "auto" (uses the multilingual model)
# Env overrides: FFMPEG, WHISPER, WHISPER_MODEL
set -euo pipefail
IN="$1"; OUT="$2"; LANG_CODE="${3:-en}"

FFMPEG="${FFMPEG:-$(command -v ffmpeg || echo /opt/homebrew/opt/ffmpeg-full/bin/ffmpeg)}"
WHISPER="${WHISPER:-$(command -v whisper-cli || command -v whisper-cpp || echo /opt/homebrew/bin/whisper-cli)}"
[ -x "$FFMPEG" ] || { echo "Missing ffmpeg: brew install ffmpeg" >&2; exit 1; }
[ -x "$WHISPER" ] || { echo "Missing whisper.cpp: brew install whisper-cpp" >&2; exit 1; }

if [ "$LANG_CODE" = "en" ]; then MODEL_NAME=ggml-small.en.bin; DTW=small.en; else MODEL_NAME=ggml-small.bin; DTW=small; fi
WHISPER_MODEL="${WHISPER_MODEL:-$HOME/.cache/whisper-cpp/$MODEL_NAME}"
if [ ! -f "$WHISPER_MODEL" ]; then
  echo "Downloading Whisper model $MODEL_NAME (one time, ~470MB)..." >&2
  mkdir -p "$(dirname "$WHISPER_MODEL")"
  curl -fL --progress-bar -o "$WHISPER_MODEL" "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/$MODEL_NAME"
fi

TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
"$FFMPEG" -nostdin -v error -y -i "$IN" -vn -ar 16000 -ac 1 "$TMP/a.wav"
# -ml 1 + -sow = one entry per word with millisecond offsets.
# --dtw aligns word times to the audio; plain offsets can drift up to ~0.4 s, which is too much for word-by-word captions.
# The preset must match the model (small.en / small); with a custom WHISPER_MODEL set NO_DTW=1 or WHISPER_DTW=<preset>.
DTW="${WHISPER_DTW:-$DTW}"
if [ -z "${NO_DTW:-}" ] && "$WHISPER" -m "$WHISPER_MODEL" -l "$LANG_CODE" -f "$TMP/a.wav" -ml 1 -sow -oj -of "$TMP/w" -np --dtw "$DTW" >/dev/null 2>&1; then
  :
else
  echo "DTW alignment unavailable, using plain word offsets" >&2
  "$WHISPER" -m "$WHISPER_MODEL" -l "$LANG_CODE" -f "$TMP/a.wav" -ml 1 -sow -oj -of "$TMP/w" -np >/dev/null 2>&1
fi

python3 - "$TMP/w.json" "$OUT" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
words = []
for s in d["transcription"]:
    t = s["text"].strip()
    if not t or t.startswith("[") or t.startswith("("):
        continue
    words.append({"i": len(words), "w": t, "s": round(s["offsets"]["from"] / 1000, 3), "e": round(s["offsets"]["to"] / 1000, 3)})
json.dump(words, open(sys.argv[2], "w"), indent=0)
print(f"{len(words)} words -> {sys.argv[2]}\n")
# Numbered read-out, new line at every pause > 0.6 s, so retakes and false starts are easy to spot.
line, start = [], None
for k, w in enumerate(words):
    if line and w["s"] - words[k - 1]["e"] > 0.6:
        print(f"[{start:>4}-{k-1:<4}] {words[start]['s']:7.2f}s  " + " ".join(line))
        line = []
    if not line:
        start = k
    line.append(w["w"])
if line:
    print(f"[{start:>4}-{len(words)-1:<4}] {words[start]['s']:7.2f}s  " + " ".join(line))
PY
