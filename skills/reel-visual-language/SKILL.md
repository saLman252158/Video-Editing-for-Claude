---
name: reel-visual-language
description: The user's visual training for short-form video editing. Covers how hooks, captions, name lower thirds, on-screen UI pop-ups, data widgets, full-screen animated scenes, colour, type and motion should look in their vertical 9:16 talking-head reels. It was learned from their Figma inspo boards. Use it whenever you plan, design, animate or review any visual element of a reel/short/TikTok (captions, hook text, overlays, motion graphics, scene graphics, thumbnails-in-video), and alongside the `reel-editor` skill when it is installed. It turns "make it look good" into concrete, repeatable decisions.
---

# Reel Visual Language

This skill is what the user taught by curating inspiration boards. It sets **how a reel looks**: hook, captions, on-screen animation, full-screen animation and design rules. A pipeline skill such as `reel-editor` sets **how a reel gets cut and rendered**. Use both: decide the visuals here, then build them with the pipeline's tools (ASS captions, ffmpeg, HyperFrames).

Before designing anything, look at the boards in `reference/`. They are the ground truth; this text is the summary.

| File | What it shows |
|---|---|
| `reference/05-caption-frames.jpg` | 9 real caption frames. The caption look to copy. |
| `reference/06-overlay-in-context.jpg` | 5 frames of UI pop-ups over a talking head. The overlay look to copy. |
| `reference/02-hook-lessons.jpg` | The hook rules with 5 annotated hooks. |
| `reference/04-onscreen-ui-overlays.jpg` | On-screen animation lesson + 34 UI references (glow cards, widgets, bento, light glass). |
| `reference/03-minimal-animation-style.jpg` | The minimal "white paper" full-screen animation style: backgrounds, scene types, layout grid, design rules. |
| `reference/01-drive-inspo-captions-onscreen-animation.jpg` | 67 sorted references: caption styles, on-screen animation, light/reveal scenes, kinetic posters. |
| `reference/00-neon-promo-board.jpg` | The older neon-lime promo preset (what `reel-editor`'s house style produces). |

Source Figma file (owner's account): https://www.figma.com/design/LkEH9tmFMAa691dUOSfeCk. Pages: Drive Inspo, Hook Inspo, Animation Inspo, On-screen Animation Inspo.

---

## 1. What the user wants (the intent behind the boards)

1. **Premium, cinematic, calm. Never cheap or loud.** Warm graded podcast and interview footage, generous negative space, thin elegant type mixed with one bold word. Think "documentary meets Apple keynote", not "meme edit".
2. **Every visual earns its place by making one idea land.** One hero word per caption line, one element per pop-up, one subject per scene. If two things fight for attention, cut one.
3. **Show what the speaker says.** When they say a number, the number appears as a widget. A tool name brings up the app icon. A list gets tiles. An abstract idea becomes an object scene (brain, iceberg, hourglass, chain). This "visualize the key word" habit is the core skill.
4. **The speaker stays the star.** Graphics sit in the lower half and never cover the face. Full-screen scenes are short cutaways and the voice keeps playing.
5. **Two graphic worlds, used on purpose:**
   - **Dark tech glow** (blue/violet glass, light streaks, glowing charts) for business, AI, tools, numbers, growth.
   - **Minimal white paper** (off-white textured paper, halftone cut-outs, cast shadows, black + white + one accent) for ideas, psychology, branding, storytelling.
   Pick one world per video and stay in it.

---

## 2. Choose the preset first

| Preset | When | Look |
|---|---|---|
| **A · Cinematic Podcast** (default for talking heads) | Interviews, podcasts, expert/founder talking heads, educational content | Warm film grade, serif-italic/script hero words in gold or lime, thin sans lead-ins, name lower third, dark-glass UI pop-ups |
| **B · Minimal Paper** | Concept explainers, storytelling, branding/psychology topics, or whenever the user asks for "the white/minimal animation style" | Full-screen off-white scenes between talking-head shots, halftone objects, 3-tone palette |
| **C · Neon Promo** (`reel-editor` house style) | Local-business promo ads with a CTA, or when the user names that style or brand (e.g. Allegiant West) | Rounded bold lowercase captions, neon #D7FF1F keyword glow, charcoal value cards, light-leak flashes |

Presets A and B mix well: an A talking head with B cutaways. Never mix B and C in one video. If you're unsure which preset fits, A is the default. Tell the user which preset you chose and why, in one line.

---

## 3. Hook: the first 1–3 seconds (from "Hook Inspo")

Every hook does three things:

1. **Show the main speaker** in the first frame, so viewers can decide "do I know or want this person?".
   - Add a **name lower third**: name in a medium sans, plus a tiny title line under it ("Founder of She Sells Academy").
   - Variants: a white pill tag with dark text (`Shelby Sapp`), or plain white text with a thin rule.
   - For a big-name guest, optionally set the name huge in a fashion serif *behind* the speaker (depth-sorted: text behind the person, as in "Marina Mogilko").
2. **Put the subtitle in the lower half** at chest height, never over the face. Use a sans font for regular words, and a **bolder/serif/script font with colour and glow for the special word**.
3. **Hook messaging.** Ask "what's the one thing that makes them watch?" and visualize THAT word. Pick it by type:

| Hook-word type | Example | Treatment |
|---|---|---|
| Scary / curiosity term | "gap between" | Lime script with glow |
| Topic of the video | "Social media" | Bold sans, butter-yellow and glow |
| Common audience desire | "GROWTH" | Wide extended caps, white, tiny lead-in line above |
| Attractive number | "$100,000", "30,000ft", "60mins" | Big numerals, pale mint or gold glow |
| Negative word | "steal" | Orange/gold script mixed into caps ("I WANT YOU TO *steal* TODAY") |

Hook choreography:
- The hero word appears on the spoken word.
- Hold the lower third about 2–3 s, then fade it out.
- No full-screen graphic before the speaker has been seen.

---

## 4. Captions (from "text inspo" + hook frames)

**Layout**
- 2 lines max, centered, in the lower half: y ≈ 1050–1350 of 1920.
- Keep it clear of the IG UI: nothing in the top 220 px or bottom 420 px.
- **Clear of the mouth, including on punch-ins.** At 1.12–1.2× zoom the mouth drops to about y ≈ 900, so the caption block's top edge goes no higher than y ≈ 1050 (feedback from the user: captions at y 930 covered the talker's mouth). Check a punched-in frame before rendering.
- A line is a **small lead-in** of 1–5 words in thin or regular sans, plus a **big hero word or phrase** 2–3× larger.
- The lead-in sits above, beside or in front of the hero word. Tight leading, so the two lines overlap optically.

**Hero-word styles.** Rotate between them across a video, but keep one dominant style.

| Style | Font (free options) | Colour | Use for |
|---|---|---|---|
| Gold serif italic | Playfair Display Bold Italic, Instrument Serif Italic, DM Serif Display Italic | Gradient #F7C873 → #E8903A, soft glow | Default hero word in warm footage ("30,000ft", "Resting Heart Rate", "Wind Down") |
| Script | Pinyon Script, Great Vibes, Allura | Lime #C6F25A or gold | Emotional/curiosity words, and the one accent per video |
| Bold sans | Inter/Manrope ExtraBold | Butter yellow #F3E36A or white + glow | Topics, product names |
| Wide caps | Unbounded, Syne ExtraBold, Michroma | White, thin glow | Desire words, one-word statements |
| Numbers | Inter Tight / Manrope SemiBold with tabular numbers | Pale mint #D7F5CF or gold | Money, %, time, counts |

**Lead-in text**
- Inter or Manrope Regular/Medium in white at 85–95% opacity.
- Small drop shadow (0 2px 8px rgba(0,0,0,.45)).
- Tiny ALL-CAPS tracking (+8%) is fine for 1–2-word lead-ins ("WHICH", "YOU SAID").

**Glow**
- Same hue as the word, blur 12–24 px, 35–55% opacity.
- It should read as light on the lens, not a neon sign.

**Timing**
- Words appear on the spoken word (from words.json).
- The hero word gets the bigger move (see §8). Hold each group until the next starts. Never leave dead caption time.

**Economy**
- One hero word per caption group. If everything is highlighted, nothing is.
- Captions mostly sentence case. Caps only for wide-caps hero words.

---

## 5. On-screen animation: UI over the talking head (from "On-screen Animation Inspo" + in-context frames)

**Placement rule (from the lesson)**
- The element goes in the **lower third and takes up big space**: 60–85% of frame width, centered or slightly offset, top edge around y ≈ 1000.
- **Darken and blur the footage behind it.** Use a bottom gradient, black 0% → 55–70%, plus 6–12 px blur under the card, so the UI reads clearly.
- The caption stays visible just above the element.
- When the captions move down, move every card down with them (one shared offset), so the gap between caption and card stays about 30 px and the card never covers line 2. Keep the card's bottom above y ≈ 1700.

**What to show, by what the speaker says**

| Speaker says… | Show… | Reference |
|---|---|---|
| A number, growth, result ("1,262 editors", "400%", "$70,318") | Big number that **counts up** plus a chart (bars, dot-matrix histogram, glowing line or ring) filling in | data-widgets, "1,262" frame |
| Clients / people / leads | Stack of notification or inquiry cards (avatar initial, name, one line, "now") sliding in one by one | "working with clients", "to find you" |
| Consistency / schedule / days | Calendar grid with days lighting up in blue in sequence, plus a progress counter ("15/30") | "to posting" |
| Content, videos, views | Row of video thumbnails, the active one highlighted, view count ticking up | "don't give up" |
| Tools / apps / AI | Glowing app-icon tiles (Notion, n8n, ChatGPT…) popping in with a stagger; optionally a finger or tap pulse on one | n8n tile, AI model cards |
| A process / connection | Node-and-line flow: sources on the left, lines drawing to one hub | "Gyanaguru" connector, You → clients |
| Features / list of 3–6 | Bento tiles: icon + 2–4 words each, staggered | bento-components |
| A setting / switch / decision | Toggle flipping, slider moving, "Restart Now" style button press | controls, "System Update" card |

**Card style (dark glow)**
- Card fill #0E1017 at 75–85% opacity, with backdrop blur if the renderer supports it.
- 1 px border rgba(255,255,255,0.10). Inner top highlight rgba(255,255,255,0.06).
- Corner radius 20–28 px at 1080 width.
- **Glow from one edge only**: a soft blue #2F6BFF, violet #7B5CFF or cyan #38D6FF bloom leaking from the bottom or one side, blur 40–80 px.
- Text: Inter/Manrope. Title in SemiBold white. Secondary text in #8A8FA3. Numbers big and light (300–500 weight).
- One accent colour per video. Default electric blue #3B7BFF; violet is the alternative. Lime #C6FF3D only in preset C.

**One element per moment.** Extract a single card or widget, never a whole dashboard screenshot.

**Light-glass variant**: use this when the video is preset B or the footage is bright.
- Frosted white card rgba(255,255,255,0.55), blur, soft shadow 0 20px 60px rgba(0,0,0,0.12).
- Pastel gradient accent (blue → violet → pink).

---

## 6. Full-screen animation scenes (from "Animation Inspo" + Drive "Animation")

These are 1.5–3.5 s cutaways that replace the talking head while the voice continues. Use them at topic changes, for abstract ideas, and as the "value" moment. Aim for 1 every 8–15 s, at most.

### 6a. Minimal Paper style (preset B)

**Background.** Never a flat fill. Pick one per video:
1. **Plain white**: off-white #EEEBE5.
2. **White + cast shadow + grid**: white → grey gradient, a soft window-light cast shadow overlay, and a thin light grey grid (#D5D2CC, 1 px, about 90 px cells).
3. **Yellow + cast shadow + grid**: warm yellow → grey (#EFE6C8 → #D9D6CF), with shadow overlay and an optional grid.

Add paper texture plus a subtle halftone/dot grain over everything.

**Scene types.** Each scene has one hero:
- **Text-only**: a text line in the middle, nothing else.
- **Text + object**: text takes most of the frame; a secondary object adds depth.
- **Text + graphic**: centred text with graphic shapes around it (thick black brush marks, colour bars, corner brackets).
- **Person-centric**: either a cut-out person in the centre with a graphic block behind (red panel, circle, frame), or the person on one side with their name and text beside them.
- **Object-centric**: a halftone cut-out object in the centre (brain, eye, flask, sneaker, skull, coffee cup), with text on top or under it, or graphics around it.
- **Graphic-centric**: one graphic carries the point (stop sign, sprouting plant, masks, gears, orbit diagram).

**Layout method** (think of the 9:16 frame as a 3×3 grid):
1. Lay the background.
2. Put the **focal point** (the hero) in the **centre cell**.
3. Place **supporting elements** in the ring around it: text on top for an object hero, or an object at the side for a text hero.
4. Place **depth elements** in the outer cells and corners: brush marks, cracks, colour blocks, out-of-focus objects.

**Design rules**
- **Colour**: a 3-tone palette of paper, ink #1C1C1C, and ONE accent.
  - Teal #2E8B6A, deep red #A3121B, or purple #7A4CE0.
  - Blue #2F6BFF is fine for a business topic.
- **Fonts**: sans for the main text, script or serif italic for the highlighted word. Pattern: small script line above, bold sans word below.
- **Text colour**: a very subtle gradient, never a flat fill.
- **Objects**: cast shadows plus texture (halftone).
- **Backgrounds**: gradient + texture + cast shadow.
- **UI-ish details** are welcome: dashed selection boxes with corner handles and a cursor, used to highlight a phrase ("This is the *one*").

### 6b. Dark Tech scenes (go with preset A)

- **Light and reveals**: light streaks, glowing orb or planet-horizon rim light, lens flare.
  - Use these for intros and section titles: thin white text appears as the light sweeps.
- **Hero stat**: one giant number ("400%", "$12B", "78%") inside a glowing glass card or over a glowing curve. Count it up.
- **Kinetic posters**: bold editorial layouts.
  - "The Tip You See" iceberg, chaos-scribble → clean cube "SYSTEM", "2026" number roll, hourglass.
  - Serif italic plus sans, deep blue or violet.
- **Product/web scene**: a phone or landing page, minimal, blue-white, floating app icons.

---

## 7. Colour and type tokens (quick copy)

```
Preset A (Cinematic Podcast)
  grade: warm, soft contrast, slightly lifted blacks, skin natural, background falls off darker
  exposure: phone footage against a bright window or backlight reads dark on the face; lift it
           (Remotion/CSS: brightness(1.14) contrast(1.05) saturate(1.08)). Keep the caption
           readability bed light (start ~48% down, max ~0.45 opacity) so the frame stays bright.
  hero gold   #F7C873 → #E8903A      hero lime  #C6F25A      butter  #F3E36A
  mint nums   #D7F5CF                orange     #FF8A1F      text    #FFFFFF @ 90%
  UI card     #0E1017 @ 80%  border rgba(255,255,255,.10)  radius 24
  glow blue   #3B7BFF   violet #7B5CFF   cyan #38D6FF   secondary text #8A8FA3
Preset B (Minimal Paper)
  paper #EEEBE5  warm paper #EFE6C8  ink #1C1C1C  grid #D5D2CC
  accent: teal #2E8B6A | red #A3121B | purple #7A4CE0 | blue #2F6BFF   (one per video)
Preset C (Neon Promo, see reel-editor)
  neon #D7FF1F  charcoal #1E1E1E  font Arial Rounded MT Bold
Fonts (free, Google Fonts): Inter, Manrope, Playfair Display, Instrument Serif,
  DM Serif Display, Pinyon Script, Great Vibes, Unbounded, Syne
```
Fonts must be installed before rendering. With HyperFrames, load them via `@font-face` or Google Fonts. With ASS, install them system-wide and use the exact family name.

---

## 8. Motion language

- **Easing**: fast-out, slow-settle. Use `cubic-bezier(0.16, 1, 0.3, 1)` (expo-out) for entries and ease-in for exits. No linear moves, no bounces except the caption pop.
- **Caption lead-in words**: fade + 8 px rise, 160 ms each, on the word.
- **Hero word**: blur 12 → 0 px, scale 92% → 100%, opacity 0 → 1, over 280–350 ms. The glow blooms 100 ms after.
  - Script words can **write on** with a left-to-right mask, about 400 ms.
- **UI cards**: rise 40–60 px, fade, blur 10 → 0 over 350–450 ms. Lists stagger 70–90 ms per item.
- **Background dim**: the darken/blur under a UI card fades in over 200 ms, slightly before the card.
- **Numbers**: count up over 0.8–1.4 s with ease-out, landing on the spoken number. Bars, rings and lines fill in sync.
- **Idle drift**: nothing is fully static. Hold elements with a slow 1–2% scale or 4–8 px drift.
- **Exits**: 180–250 ms fade/slide down, on the next cut or the next sentence. Never leave a graphic lingering into an unrelated sentence.
- **Transitions**: mostly hard cuts on the talking head.
  - Into and out of full-screen scenes: a quick light sweep or flash (dark tech), or a paper slide/wipe (minimal).
  - Pair each with a soft whoosh at -24 to -30 dB.
- **SFX**: soft pop or tick on each card entry, shimmer on the hero number, whoosh on scene changes. Felt, not heard.

---

## 9. How to build it

- **Captions with mixed fonts and glow**: ASS (via `reel-editor`'s captions.py, with `keywords` = hero words and `accents` = script words) or HyperFrames.
  - In ASS, use `\fn` to switch font per word, `\blur` on a duplicated glow layer under the text, and `\t` for the scale/blur entry.
- **UI pop-ups, widgets, scenes**: build as HTML/CSS/GSAP in HyperFrames (`hyperframes:hyperframes` skill). Render 1080x1920 at 30 fps.
  - Over-speaker overlays: transparent (ProRes 4444/WebM alpha).
  - Full-screen scenes: opaque.
  - Composite in RGB so colours stay neutral.
- **Name lower third / text behind the speaker**: needs a person matte. Use rembg/MediaPipe segmentation, or HyperFrames media-use cutouts. Without a matte, put the name in front.
- **Background dim under UI**: an ffmpeg `gblur` + `colorchannelmixer`/`curves` on a gradient-masked region, or a gradient layer in the overlay comp.
- **Halftone objects (preset B)**: cut out the object, desaturate, apply a halftone/dot filter, add a cast shadow (offset, blurred, 25–35% opacity).
- **Time everything to words.json** (the rough-cut timeline).

---

## 10. Decision checklist: run it for every reel before rendering

- [ ] Preset chosen (A / B / C) and stated to the user. One graphic world per video.
- [ ] **Hook**: speaker visible in frame 1. Name lower third. Hook word picked by type (scary / topic / desire / number / negative) and styled as the hero.
- [ ] Captions in the lower half (y ≈ 1050–1350), clear of the face and IG zones. Lead-in sans + ONE hero word per group.
- [ ] Check a punched-in frame: caption below the mouth/beard. Check overall brightness: the face is not dim against a bright background.
- [ ] Every number the speaker says (that matters) gets a widget or hero number that counts up.
- [ ] Every tool, list, process or consistency claim got the matching UI element from the §5 table.
- [ ] Each UI element: lower third, 60–85% wide, darkened/blurred bed behind it, caption still visible above it.
- [ ] One element per moment. No full dashboards, no two pop-ups at once.
- [ ] Full-screen scenes: one hero in the centre cell, support ring, depth corners, textured background, 3-tone palette.
- [ ] One accent colour across the whole video. Glow subtle.
- [ ] Motion: expo-out entries, staggered lists, idle drift, clean exits on the next sentence.
- [ ] Compare 3–5 rendered frames side by side with `reference/05-caption-frames.jpg` and `reference/06-overlay-in-context.jpg`. If it looks cheaper, busier or louder than the references, simplify.

## 11. Anti-patterns (the boards say "not this")

- Captions over the face or in the top/bottom IG zones.
- Every word highlighted, rainbow colours, or more than one accent colour.
- Heavy stroke outlines and meme-style yellow Impact text (outside preset C).
- Full dashboard screenshots pasted over the speaker. Tiny unreadable UI.
- Flat white or flat black backgrounds on full-screen scenes.
- Static graphics with no entry or idle motion. Graphics that outstay their sentence.
- Mixing minimal paper and neon promo in one video.

## 12. Keep learning

When the user adds a new inspo board or folder:
1. Analyze it the same way (category → what it means → rule).
2. Add the rule to the matching section here, and add a reference image to `reference/`.
3. Keep this file the single source of truth.
