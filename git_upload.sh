#!/bin/bash
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

REPO_DIR="/mnt/c/Users/Lenovo/okx-orbit-bot"

echo -e "${GREEN}=== Git 自动上传脚本 ===${NC}"

cd "$REPO_DIR" || exit 1

if [ ! -d ".git" ]; then
    echo -e "${RED}✗ 不是 Git 仓库${NC}"
    exit 1
fi

CHANGES=$(git status --porcelain)
if [ -z "$CHANGES" ]; then
    echo -e "${YELLOW}没有需要提交的更改${NC}"
    exit 0
fi

echo -e "${YELLOW}检测到更改:${NC}"
git status --short
echo ""

DEFAULT_MSG="Auto-commit: $(date '+%Y-%m-%d %H:%M:%S')"
read -p "提交信息 (回车使用默认: $DEFAULT_MSG): " COMMIT_MSG
COMMIT_MSG=${COMMIT_MSG:-$DEFAULT_MSG}

echo -e "${YELLOW}添加文件...${NC}"
git add .

echo -e "${YELLOW}提交更改...${NC}"
git commit -m "$COMMIT_MSG"

echo -e "${YELLOW}推送到远程...${NC}"
if git push origin master 2>&1; then
    echo -e "${GREEN}✓ 上传成功！${NC}"
else
    echo -e "${RED}✗ 推送失败，尝试强制推送？(y/N)${NC}"
    read -p "> " FORCE
    if [ "$FORCE" = "y" ] || [ "$FORCE" = "Y" ]; then
        git push origin master --force
        echo -e "${GREEN}✓ 强制推送成功！${NC}"
    fi
fi

echo ""
echo -e "${GREEN}完成！${NC}"
