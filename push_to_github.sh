#!/bin/bash
# OKX Orbit Bot - GitHub 推送脚本

set -e

echo "================================"
echo "OKX Orbit Bot - GitHub 推送"
echo "================================"
echo ""

cd /mnt/c/Users/Lenovo/okx-orbit-bot

# 检查 SSH 连接
echo "检查 GitHub SSH 连接..."
ssh -T git@github.com 2>&1 | head -1
echo ""

# 检查 gh 认证状态
echo "检查 GitHub CLI 认证..."
if ! gh auth status &>/dev/null; then
    echo "需要登录 GitHub CLI..."
    echo "请选择认证方式："
    echo "1) 浏览器认证 (推荐)"
    echo "2) Token 认证"
    read -p "选择 (1/2): " choice
    
    if [ "$choice" = "1" ]; then
        gh auth login -h github.com -w
    else
        echo "请输入 GitHub Personal Access Token:"
        echo "(创建: GitHub Settings → Developer settings → Personal access tokens)"
        read -s token
        echo "$token" | gh auth login -h github.com --with-token
    fi
fi

echo ""
echo "创建 GitHub 私人仓库..."
gh repo create okx-orbit-bot --private --source=. --push

echo ""
echo "================================"
echo "完成！仓库已创建并推送"
echo "================================"
echo ""
gh repo view thirtseven/okx-orbit-bot --web
