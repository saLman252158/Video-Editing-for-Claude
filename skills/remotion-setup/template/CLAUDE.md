# Remotion Studio: house setup

This is the Remotion project for the user's reels. Remotion 4.0.538 runs on Node; the studio opens with `npm run dev` at http://localhost:3000.

## Conventions
- **Format:** 1080x1920, 30 fps. The main composition is `Reel` in `src/Composition.tsx`, and its duration comes from the video via mediabunny.
- **Media goes in `public/`, referenced with `staticFile()`:**
  - `public/footage/`: the cut video from the `raw-cut` skill (`<name>_cut.mp4`).
  - `public/sfx/whooshes|textures|risers|hits/`: sound-effect library, one folder per family (`reel-sound-design`).
  - `public/music/`: music, used under the talking head only.
  - `public/assets/`: images, logos, icons, cut-outs.
- **Packages:**
  - `@remotion/media` (`<Video>`, `<Audio>`), `@remotion/captions`, `@remotion/google-fonts`, `@remotion/transitions`, `@remotion/media-utils`, `mediabunny`.
  - Add more with `npx remotion add <pkg>`, which keeps versions in sync.
- **Animations:** drive every animation with `useCurrentFrame()` + `interpolate`/`spring`. Never use CSS transitions or `setTimeout`.

## How the user's skills map onto Remotion
- **`edit-planner`:** `edit-plan.json` (style + scenes with `type` and `plan`) becomes one `<Sequence>` per scene, timed from the scene start/end (seconds × 30).
  - `style.mainColor` / `font` / `fontColor` are the accent, caption font and text colour.
  - Scene types: `captions` = video + captions; `caption_ui` = plus one lower-half UI element over a darkened bed; `half` = graphics on top, talker reframed to the bottom half; `full` = full-screen animation, voice continues.
- **`reel-visual-language`:** caption, UI-card, scene and motion rules.
- **`reel-sound-design`:** one `<Audio>` layer group per family (WHOOSHES, TEXTURES, RISERS, HITS, MUSIC), named that way in the Studio timeline.
  - Volumes are clip gains relative to the voice (e.g. -12 dB → `volume={Math.pow(10, -12 / 20)}`).
  - Mute original audio, never delete it.
- **Remotion's official skills** (`remotion-*` in `~/.claude/skills`): load `remotion-best-practices` first for any Remotion code.

## Commands
- `npm run dev`: the Studio (preview, timeline, props).
- `npx remotion render Reel out/reel.mp4 --props='{"src":"footage/x_cut.mp4"}'`: render.
- `npm run lint`: ESLint + TypeScript check.
- While the Studio is running on port 3000, add `--port=3101` to `remotion render` / `remotion still`.

## License
Remotion is free for individuals and companies of up to 3 people. Larger companies need a company license (remotion.pro/license).
