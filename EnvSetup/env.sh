#!/bin/zsh

/bin/zsh -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

brew update && brew upgrade && brew cleanup --prune=all && brew autoremove

brew install node gcc neofetch fzf exa thefuck neovim bat

npm install -g @vue/cli

if command -v curl >/dev/null 2>&1; then
  bash -c "$(curl -fsSL https://raw.githubusercontent.com/ayamir/nvimdots/HEAD/scripts/install.sh)"
else
  bash -c "$(wget -O- https://raw.githubusercontent.com/ayamir/nvimdots/HEAD/scripts/install.sh)"
fi

nvim
