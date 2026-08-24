#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="/opt/github-counter"
GIT_SSH_COMMAND="ssh -i ~/.ssh/id_repo_deploy -o IdentitiesOnly=yes"

cd "$REPO_DIR"

# Synchronizacja przed zmianami
GIT_SSH_COMMAND="$GIT_SSH_COMMAND" git pull --rebase origin main

# Wykonanie skryptu
/usr/bin/python3 increment.py

# Zatwierdzenie i wysłanie
git add counter.txt
if ! git diff --staged --quiet; then
  git commit -m "counter"
  GIT_SSH_COMMAND="$GIT_SSH_COMMAND" git push origin main
fi
