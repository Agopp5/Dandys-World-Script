#!/bin/bash
# One-time setup for making the MTK lessons on a Mac: manim + LaTeX + ffmpeg + the Lato font + ManimToolkit (mtk).
# Run from anywhere:  bash astronautics_video/setup_local_mac.sh
# Safe to re-run: each step skips what is already installed. Not tested on a real Mac yet; if a step fails,
# paste its error into a Claude session.
set -euo pipefail

say() { printf '\n==> %s\n' "$*"; }

if ! command -v brew >/dev/null; then
  say "Installing Homebrew (it will ask for your Mac password)"
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  eval "$(/opt/homebrew/bin/brew shellenv 2>/dev/null || /usr/local/bin/brew shellenv)"
fi

say "Command-line tools: python, uv, ffmpeg, cairo, pango"
brew install git python uv ffmpeg cairo pango pkg-config

say "LaTeX (for equations) and the Lato font (several GB; the slowest step)"
brew list --cask mactex-no-gui >/dev/null 2>&1 || brew install --cask mactex-no-gui
brew list --cask font-lato >/dev/null 2>&1 || brew install --cask font-lato
eval "$(/usr/libexec/path_helper)"   # puts the new TeX binaries on PATH for this shell

say "ManimToolkit (mtk)"
MTK_DIR="${MTK_DIR:-$HOME/code/ManimToolkit}"
if [ ! -d "$MTK_DIR/.git" ]; then
  mkdir -p "$(dirname "$MTK_DIR")"
  git clone https://github.com/abhichavali/ManimToolkit.git "$MTK_DIR"
fi
(cd "$MTK_DIR" && ./install.sh)

case ":$PATH:" in *":$HOME/.local/bin:"*) ;; *)
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
  export PATH="$HOME/.local/bin:$PATH" ;;
esac

say "Check: re-run one finished scene (uses cached narration, costs nothing)"
REPO="$(cd "$(dirname "$0")/.." && pwd)"
(cd "$REPO/astronautics_video/orbit_det" && mtk check s04_turn_omega.py)

if [ -z "${OPENROUTER_API_KEY:-}" ]; then
  echo
  echo "Last step, by hand: add your OpenRouter key so new narration can be voiced:"
  echo "  echo 'export OPENROUTER_API_KEY=sk-or-...' >> ~/.zshrc && source ~/.zshrc"
fi
say "Done. Open a new terminal (or the Claude app) in $REPO and start the lesson."
