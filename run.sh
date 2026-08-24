#!/usr/bin/env bash
set -euo

cd /root/github-counter

git pull origin main --rebase

# 2. Uruchomienie skryptu Pythona
python3 main.py

# 3. Commit i push
git add counter.txt
if ! git diff --staged --quiet; then
  git commit -m "github counter"
  git push origin main
fi
