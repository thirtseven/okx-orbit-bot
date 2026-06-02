#!/bin/bash
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

REPO_DIR="/mnt/c/Users/Lenovo/okx-orbit-bot"
cd "$REPO_DIR" || exit 1

CHANGES=$(git status --porcelain)
if [ -z "$CHANGES" ]; then
    echo -e "${YELLOW}没有需要提交的更改${NC}"
    exit 0
fi

COMMIT_MSG="${1:-Auto-commit: $(date '+%Y-%m-%d %H:%M:%S')}"

git add .
git commit -m "$COMMIT_MSG"
git push origin master 2>&1

echo -e "${GREEN}✓ 已推送到 GitHub${NC}"
