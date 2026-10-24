#!/usr/bin/env bash
# Set up the user's Remotion reel studio on this computer.
# Usage: setup.sh [target-dir]   (default: ~/remotion-studio)
#   - copies the pinned project template (Remotion 4.0.538, Reel 1080x1920@30)
#   - installs exact package versions from package-lock.json
#   - creates the media folders
#   - installs Remotion's official agent skills for Claude Code (global)
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
TARGET="${1:-$HOME/remotion-studio}"

command -v node >/dev/null || { echo "Node.js is missing. Install it: brew install node  (or https://nodejs.org)" >&2; exit 1; }
NODE_MAJOR="$(node -p 'process.versions.node.split(".")[0]')"
NODE_MINOR="$(node -p 'process.versions.node.split(".")[1]')"
if [ "$NODE_MAJOR" -lt 20 ] || { [ "$NODE_MAJOR" -eq 20 ] && [ "$NODE_MINOR" -lt 19 ]; } || { [ "$NODE_MAJOR" -eq 22 ] && [ "$NODE_MINOR" -lt 13 ]; } || [ "$NODE_MAJOR" -eq 21 ] || [ "$NODE_MAJOR" -eq 23 ]; then
  echo "Node $(node -v) is too old for Remotion 4.0.538 (needs 20.19+, 22.13+ or 24+). Upgrade: brew upgrade node" >&2; exit 1
fi

if [ -e "$TARGET/package.json" ]; then
  echo "$TARGET already has a project. Not overwriting. Pass a different folder." >&2; exit 1
fi
mkdir -p "$TARGET"
cp -R "$HERE/template/." "$TARGET/"
mv "$TARGET/gitignore" "$TARGET/.gitignore"
for d in footage sfx/whooshes sfx/textures sfx/risers sfx/hits music assets; do
  mkdir -p "$TARGET/public/$d"; touch "$TARGET/public/$d/.gitkeep"
done

echo "Installing packages (exact versions)..."
(cd "$TARGET" && npm ci --no-fund --no-audit --loglevel=error)

echo "Installing Remotion's official agent skills for Claude Code..."
(cd "$TARGET" && npx -y skills add remotion-dev/skills -g -a claude-code -y --copy \
  -s remotion-best-practices -s remotion-captions -s remotion-create -s remotion-docs -s remotion-markup \
  -s remotion-multimedia -s remotion-render -s remotion-studio -s remotion-upgrade >/dev/null) \
  || echo "WARNING: could not install the remotion-* agent skills (network?). Re-run later: npx skills add remotion-dev/skills -g -a claude-code" >&2

echo "Checking the project..."
(cd "$TARGET" && npm run -s lint)

echo
echo "Done. Remotion studio is at: $TARGET"
echo "  Start the Studio:  cd \"$TARGET\" && npm run dev     (http://localhost:3000)"
echo "  Put cut videos in public/footage, SFX in public/sfx/<family>, music in public/music."
