---
name: edit-planner
description: Standing rule for every new project or video. Right after handing back the rough cut (raw-cut), immediately ask the user whether they want to customize the animation plan themselves or leave it to Claude using the client's reference style. If they customize, build and hand over the edit-planning page, then wait for them to fill it in and return it. If not, plan the scenes yourself from the client references. The page is a self-contained HTML file with (1) a visual-style section (main colour, caption font, font colour, live 9:16 preview) and (2) a two-panel workspace: the cut video's script split into scenes on the left, and on the right a per-scene type picker (Captions / Caption + UI / Half Screen / Full Screen Animation) plus a large editing-plan text area. Also use it when the user asks to plan an edit, plan scenes or "make the planning page". Later, read the saved edit-plan.json to build the edit.
---

# Edit Planner

**The rule (from the user):** after cutting a video, give them a planning page where they:
- set the **visual style**: main colour, font, font colour, with a live preview;
- see the **script split into scenes** on the left;
- on the right, pick a **scene type per scene** and write the **full editing plan** for that scene: animations, transitions, sound effects, visual references, timing.

## The flow, every new project or video

1. `raw-cut` hands back the rough cut.
2. **In the same message, ask immediately:**
   > "Do you want to customize the animation plan yourself, or should I plan it using the client's reference style?"
3. **If the user wants to customize:** build the page (below), open it and hand it over with one line on how to return it (**Save plan (JSON)** → put `edit-plan.json` next to the cut, or **Copy as Markdown** → paste in chat). Then **stop and wait**. Don't start the edit until they send the filled-in plan back.
4. **If the user leaves it to you:** don't build the page. Plan it yourself (see "If the user leaves it to you" below), then build the edit.
5. When the filled plan comes back, follow "After the user plans".

Ask once per project. If the user already said which way they want it for this project, don't ask again.

## If the user leaves it to you
- **Use the client's reference style first:** reference videos, brand colours, fonts or boards the client provided for this project. Look at them before planning. If there are none, use `reel-visual-language` (pick and state the preset) and `reel-sound-design`.
- **Plan every scene:**
  - Split the script into beats.
  - Give each scene a type, using the rules of thumb under "Optional pre-fill" below.
  - Write a short plan per scene: animation, transition, SFX, timing.
- **Show the plan before rendering:** give the user a compact scene list (scene · time · type · one-line plan) in chat, then build the edit unless they object.
- **Save the plan:** write it as `edit-plan.json` (same format as the page exports) next to the cut, so the user can open it later with the page's **Import** if they want to tweak it.

## Build it

```bash
python3 $EP/scripts/make_planner.py cut/words.json cut/edit-plan.html \
  --cut-report cut/<name>_cut.cut.json --video cut/<name>_cut.mp4 --title "<short title>" --open
```
- `$EP` is this skill folder (e.g. `~/.claude/skills/edit-planner`).
- **`words.json`** is raw-cut's transcript of the RAW video. With `--cut-report`, words are remapped onto the cut timeline using the exact kept-word list, so scene times match the cut video.
- **Auto scenes:** split at sentence ends. A scene closes once it's ≥ 3.5 s and the next sentence would push it past 8 s (`--min-scene` / `--max-scene`), or at a pause > 0.8 s.
- **Better scenes (recommended):** read the printed scene list. If the beats are wrong (a hook split in two, a list spread over three scenes), write `cut/scenes.json` and rebuild with `--scenes cut/scenes.json`:
  ```json
  [{"start":0.0,"end":3.2,"script":"…","type":"captions","plan":""}, …]
  ```
- **Optional pre-fill:** a suggested `type` and a starter `plan` per scene, following `reel-visual-language`:
  - the hook → Captions with a hero word;
  - numbers / tools / lists → Caption + UI;
  - an explainer with a visual → Half Screen;
  - an abstract idea or topic change → Full Screen Animation.

  Tell the user these are suggestions. Leave `plan` empty if they want to write it themselves.
- **`--open`** opens the page in their default browser (macOS). On other systems, give them the file path.

## What the page does
- **01 Visual style**:
  - Main colour: 10 presets from the visual skill plus a custom picker/hex.
  - Font: 11 Google Fonts (Inter, Manrope, Montserrat, Playfair Display, Instrument Serif, DM Serif Display, Unbounded, Syne, Bebas Neue, Pinyon Script, Great Vibes).
  - Font colour.
  - A live 9:16 preview: talker, caption with lead-in + hero word in the main colour, and a small UI card.
- **02 Script & editing plan**:
  - **Left:** the scene cards, each with number, timecode, editable script text, type badge and controls (↑ ↓ / Merge with next / Duplicate / Delete), plus "+ Add scene".
  - **Right:** the selected scene's script, the 4 scene-type cards (label, description, mini 9:16 preview, highlighted when selected; set independently per scene), and the large plan text area with quick-insert chips (Animations / Transitions / Sound effects / Visual references / Timing).
- **Storage:** autosaves in the browser (localStorage). **Save plan (JSON)** downloads `edit-plan.json`. **Copy as Markdown** puts the whole plan on the clipboard. **Import** restores a saved JSON. **Reset** reloads from the transcript.
- **Fonts:** load from Google Fonts. Offline, the page still works with fallback fonts.

## After the user plans
Ask the user to click **Save plan (JSON)** and put `edit-plan.json` next to the cut video, or paste the Markdown in chat. Then read it and build the edit:
- **`style.mainColor` / `font` / `fontColor`:** use these as the accent, caption font and text colour (they override the preset defaults in `reel-visual-language`).
- **Per scene `type`:**
  - `captions` → talker + captions only, no extra graphics.
  - `caption_ui` → talker + captions + one UI element/animation in the lower half (darken/blur bed).
  - `half` → graphics in the top half (0–960 px), talker reframed into the bottom half (960–1920 px).
  - `full` → full-screen animation, no talker; the voice continues.
- **Per scene `plan`:** follow it literally for animations, transitions, SFX and timing. Fill gaps with `reel-visual-language` and `reel-sound-design`. Times in the plan are on the cut timeline.
- If the user edited script text in the planner, treat that as caption-text corrections. It doesn't change the cut.

## Files
- `assets/planner-template.html`: the page (data is injected at `/*__PLAN_DATA__*/`).
- `scripts/make_planner.py`: transcript → scenes → page. Stdlib only.
