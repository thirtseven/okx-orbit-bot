#!/bin/bash
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}=== 启动 Edge 浏览器 (CDP 模式) ===${NC}"

EDGE_PATH="/mnt/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
CDP_PORT=9222

if [ ! -f "$EDGE_PATH" ]; then
    EDGE_PATH="/mnt/c/Program Files/Microsoft/Edge/Application/msedge.exe"
fi

if [ ! -f "$EDGE_PATH" ]; then
    echo "未找到 Edge 浏览器"
    exit 1
fi

echo -e "${YELLOW}启动 Edge 浏览器...${NC}"
echo -e "CDP 端口: ${GREEN}${CDP_PORT}${NC}"
echo ""

powershell.exe -Command "Start-Process '$EDGE_PATH' -ArgumentList '--remote-debugging-port=${CDP_PORT}'" 2>/dev/null

sleep 3

echo -e "${GREEN}✓ Edge 浏览器已启动${NC}"
echo ""
echo -e "请在 Edge 浏览器中:"
echo -e "1. 登录 OKX 账户"
echo -e "2. 访问 https://www.okx.com/zh-hans/orbit/feed"
echo -e "3. 然后在控制面板点击 '启动并导航'"
