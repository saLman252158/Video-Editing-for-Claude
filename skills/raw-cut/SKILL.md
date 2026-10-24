---
name: raw-cut
description: Standing rule. Whenever the user gives access to a raw video or audio file (raw footage, A-roll, a talking-head recording, "here's the raw", or a file dropped in a folder), cut it automatically. Make a word-level transcript, remove every silence and every bad take (retakes, false starts, stumbles, repeated lines, off-camera chatter), keep ~20 ms padding around the speech, and hand back the fully cut video. Run this before any further editing. Then immediately ask whether the user wants to customize the animation plan (edit-planner page) or leave it to Claude with the client's reference style.
---

# Raw Cut

**The rule (from the user):** every time they give you a raw file or video:
1. Create a **word-level transcript**.
2. Remove **every silence** and **every bad take**.
3. Keep the **padding around 20 ms**.
4. **Hand back the fully cut video.**

Don't ask before cutting. Just do it, then report. Right after handing back the cut, ask the animation-plan question (step 6). The full edit (`reel-visual-language`, `reel-sound-design`, `reel-editor`) follows from that answer.

## Requirements (one-time, any Mac)
```bash
brew install ffmpeg whisper-cpp     # python3 comes with macOS; the scripts are stdlib-only
```
The Whisper model (~470 MB) downloads itself on first use to `~/.cache/whisper-cpp/`.

Scripts are in `scripts/` next to this file. Below, `$RC` = this skill folder (e.g. `~/.claude/skills/raw-cut`).

## Workflow

**0. Ingest.**
- `ffprobe` the file: duration, resolution, fps, audio streams.
- If there are several raw clips, transcribe each one. If they're parts of one recording, concat them in order first.
- Keep the original untouched. Write outputs next to it in a `cut/` folder, or wherever the user asks.

**1. Transcribe:** `bash $RC/scripts/transcribe.sh raw.mov cut/words.json`
- Word times are DTW-aligned to the audio by default (`--dtw`). Plain Whisper offsets drift up to ~0.4 s, which makes word-by-word captions pop early or late. Use these same aligned times, remapped onto the cut timeline via the cut report's `kept_words`, for the captions in the edit.
- Pass `[lang]` as a third argument for non-English (`bn`, `hi`, `auto`…). That switches to the multilingual model.
- It prints the transcript as numbered lines, with a new line at every pause over 0.6 s, e.g. `[  7-69 ]  3.10s  Now we're going to…`. Read all of it.

**2. Decide the bad takes.** This is editor judgement, so do it by reading the transcript.
- **Retake / restart:** the same sentence (or its start) said twice or more. Keep the **last complete, clean** take and drop the earlier ones. (Example: "Today we're going to try perfume oil. Now we're going to try this perfume oil." → keep the second.)
- **False starts and stumbles:** "So the— so the first one…". Drop the broken fragment, keep the clean restart.
- **Mid-sentence corrections:** "it costs fifty, sorry, fifteen dollars" → drop "fifty, sorry,".
- **Off-camera chatter, greetings to someone else, "is it recording?", "okay cut", laughs between takes:** drop.
- **Filler words ("um", "uh", "like", "you know") as their own words:** drop when they stand alone. Whisper often leaves out "um/uh" entirely; those land in the gaps and the silence pass removes them.
- **Never** drop content words that change the meaning. If you're unsure whether something is a retake or intentional repetition (emphasis, "again and again"), keep it and mention it.

Write `cut/keep.json` with the inclusive word-index ranges to keep:
```json
{"keep": [[7, 69], [71, 123]]}
```
If there are no bad takes, skip `--keep` (it keeps all words and removes silences only).

**3. Cut:** `python3 $RC/scripts/cut.py raw.mov cut/words.json cut/<name>_cut.mp4 --keep cut/keep.json`
- **Padding:** default `--pad 0.02` (20 ms), the user's standard. Don't change it unless asked.
- **Snapping:** each kept piece's edges are snapped to the real speech onset and offset in the waveform before padding, because Whisper word times drift 50–400 ms. When words run together with no silence, it cuts in the quietest dip.
- **Silences:** every silence longer than `--min-silence` (default 0.18 s) is removed, including pauses inside a kept take. Quiet consonants *inside* a word are never cut.
- **Fades:** a 5 ms audio fade on every cut prevents clicks.
- **Output:** H.264 CRF 16 (`--crf` to change), AAC 48 kHz, same resolution, VFR phone footage conformed to the nearest standard frame rate.
- **Report:** `<name>_cut.cut.json` holds segments, the removed %, the dropped words and `loud_edges`.

**4. Check before handing back:**
- **Read the printed line.** A "% removed" of about 10–35% is normal for raw talking-head footage. Over 45% means you probably dropped too much; re-read `keep.json`.
- **If it prints `LISTEN-CHECK`,** an edge landed on loud audio. Extract ±0.5 s around that time from the cut (`ffmpeg -ss T-0.5 -t 1 -i cut.mp4 chk.wav`), look at the level with `astats`, and if a word is clipped, widen that piece (adjust `keep.json` or raise `--pad` for that run) and re-cut.
- **Room noise:** if the room is noisy and pauses aren't being removed, lower the sensitivity with `--thresh-db` (e.g. `-35`). If soft speech is being cut, raise the floor (e.g. `--thresh-db -45`).
- **Don't trust a re-transcription of the cut as a check.** Whisper hallucinates on tightly cut audio (repetition loops).
- Spot-check 3 frames around cuts for flash frames or a mid-blink jump.

**5. Hand back:**
- The path to the cut video.
- Original duration → cut duration (% removed) and the number of pieces.
- The takes and lines removed, in plain words (from `dropped_words` plus your judgement).
- Anything you weren't sure about, so the user can ask to put it back.

**6. Then ask immediately, in the same message as the hand-back:**
> "Do you want to customize the animation plan yourself, or should I plan it using the client's reference style?"

- **If the user customizes:** build the planning page with the `edit-planner` skill (same `words.json` + cut report), hand it over, and wait for them to fill it in and send back `edit-plan.json` (or the Markdown).
- **If you plan it:** don't build the page. Plan every scene yourself from the client's reference style (see `edit-planner` → "If the user leaves it to you"), then build the edit.

## Notes
- **Multicam / two speakers:** transcribe the mixed audio and cut on it, but never drop the other speaker's lines as "chatter" unless they're clearly off-topic setup talk.
- **Music under the raw audio:** silence detection gets less reliable. Rely more on the transcript (word gaps) and check the edges.
- **Next step:** if the user then wants the full edit, the cut is the input to `reel-editor` (skip its silence-removal step, it's already done, and use `--noise` only for framing splits), plus `reel-visual-language` and `reel-sound-design`.
