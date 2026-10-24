---
name: remotion-setup
description: Sets up (or finds) the user's Remotion reel studio on the current computer. It is a pinned Remotion 4.0.538 project with a `Reel` composition (1080x1920, 30 fps, duration read from the cut video), media folders for footage/SFX families/music/assets, house CLAUDE.md conventions, and Remotion's official agent skills. Use it when the user asks to install or set up Remotion, when an edit needs to be built in Remotion and no studio exists on this machine yet, or when moving to a new computer.
---

# Remotion Setup

The user's Remotion project is the place where edits get built after `raw-cut` → `edit-planner`, using `reel-visual-language` and `reel-sound-design`. This skill makes it identical on every computer.

## 1. Find an existing studio first
Look for a folder with a `remotion.config.ts` and a `Reel` composition in `src/Composition.tsx`. Check, in order:
1. `~/claude for sajid/remotion-studio` (the user's main Mac)
2. `~/remotion-studio`
3. Ask the user.

If one exists, use it and don't set up a second one. Run `npm run lint` there to confirm it still works.

## 2. Set up a new one
```bash
bash ~/.claude/skills/remotion-setup/scripts/setup.sh "<target folder>"   # default ~/remotion-studio
```
The script:
1. Checks Node (needs 20.19+, 22.13+ or 24+; otherwise `brew install node` or `brew upgrade node`).
2. Copies `template/` into the target folder.
3. Installs exact versions with `npm ci` (from the pinned lockfile).
4. Creates `public/footage`, `public/sfx/{whooshes,textures,risers,hits}`, `public/music` and `public/assets`.
5. Installs Remotion's official `remotion-*` agent skills into `~/.claude/skills`.
6. Runs lint and the TypeScript check.

It refuses to overwrite an existing project.

Then verify with a real render before telling the user it's ready:
```bash
cd "<target>" && npx remotion still Reel /tmp/slate.png --frame=30
```
Look at the PNG. It should be a dark slate reading "REMOTION STUDIO". The first render downloads Remotion's headless browser once. If the Studio is already running on port 3000, add `--port=3101` to renders, or the render will reach the Studio and fail with "getStaticCompositions is undefined".

Start the Studio for the user with `npm run dev` (run it in the background), on http://localhost:3000.

## 3. What's in the template
| File | Purpose |
|---|---|
| `src/Composition.tsx` | `Reel` composition, 1080x1920 @ 30 fps. Props: `src` (cut video in `public/`, e.g. `footage/x_cut.mp4`), `title`, `accent`. Duration comes from the video via mediabunny. With no `src`, it shows a placeholder slate. |
| `src/Root.tsx`, `src/index.ts` | Standard Remotion entry |
| `package.json` + `package-lock.json` | Remotion 4.0.538 with `@remotion/media`, `@remotion/captions`, `@remotion/google-fonts`, `@remotion/transitions`, `@remotion/media-utils`, `mediabunny` 1.62.0 |
| `CLAUDE.md` | House conventions: how `edit-plan.json` scenes and types, the visual rules and the sound families map onto Remotion code |
| `remotion.config.ts`, `tsconfig.json`, `eslint.config.mjs`, `.prettierrc`, `gitignore` | Stock Remotion config |

## Notes
- **Adding packages:** use `npx remotion add <pkg>` so versions stay in sync. Upgrade with the `remotion-upgrade` skill.
- **Keeping the template current:** after an upgrade, copy the changed `package.json` / `package-lock.json` (and any new house components in `src/`) back into `template/` and push the skills repo.
- **License:** Remotion is free for individuals and companies of up to 3 people. Larger companies need a company license (remotion.pro/license).
