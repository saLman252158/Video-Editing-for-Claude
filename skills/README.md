# Claude video-editing skills

| Skill | What it does |
|---|---|
| `reel-visual-language/` | Visual training from the Figma inspo boards and trending reels: hooks, captions, on-screen UI pop-ups, full-screen animation scenes, colour, type and motion rules. Presets A–D (D = walk & talk kinetic, with `scripts/person_matte.swift` for text behind the speaker). |
| `raw-cut/` | Standing rule: any raw video → word-level transcript → remove every silence and bad take → ~20 ms padding → hand back the cut. Scripts included. |
| `edit-planner/` | After the cut: builds a planning page (style picker + live preview, script by scene, per-scene type: Captions / Caption + UI / Half Screen / Full Screen, editing plan) and reads back `edit-plan.json`. |
| `remotion-setup/` | Sets up the pinned Remotion reel studio (Reel 1080x1920@30, media folders, house CLAUDE.md, Remotion's official agent skills) with one command. |
| `reel-sound-design/` | Sound training: whooshes / textures / risers & hits, levels, the 3-pass workflow, track rules, acceptance checks. Original doc in `source/`. |

## Install on any computer

```bash
git clone https://github.com/saLman252158/Video-Editing-for-Claude.git
mkdir -p ~/.claude/skills
cp -R Video-Editing-for-Claude/skills/raw-cut Video-Editing-for-Claude/skills/edit-planner Video-Editing-for-Claude/skills/remotion-setup Video-Editing-for-Claude/skills/reel-visual-language Video-Editing-for-Claude/skills/reel-sound-design ~/.claude/skills/
brew install ffmpeg whisper-cpp node   # raw-cut needs ffmpeg + whisper; Remotion needs node
bash ~/.claude/skills/remotion-setup/scripts/setup.sh ~/remotion-studio   # Remotion studio
```

Restart Claude Code. The skills load automatically when they apply: drop a raw video → raw-cut → edit-planner; visuals → reel-visual-language; SFX → reel-sound-design. You can also call one by name, e.g. "use the edit-planner skill".

Workflow: **raw video → raw-cut (rough cut handed back) → Claude asks: "customize the animation plan, or leave it to me with the client's reference style?" → either you fill in the edit-planner page and send it back, or Claude plans from the references → edit built in Remotion (remotion-setup) using reel-visual-language + reel-sound-design.**

To update later, run `git pull`, then copy the folder again. On this Mac, `~/.claude/skills/raw-cut`, `edit-planner`, `remotion-setup`, `reel-visual-language` and `reel-sound-design` are symlinks to these folders, so edits here take effect immediately.

Claude.ai (web/desktop): zip each skill folder and upload it under Settings → Capabilities → Skills.
