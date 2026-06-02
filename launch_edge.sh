#!/bin/bash
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}=== Edge CDP 启动器 ===${NC}"

CDP_PORT=${1:-9222}
EDGE_PATHS=(
    "/mnt/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
    "/mnt/c/Program Files/Microsoft/Edge/Application/msedge.exe"
)

EDGE_PATH=""
for path in "${EDGE_PATHS[@]}"; do
    if [ -f "$path" ]; then
        EDGE_PATH="$path"
        break
    fi
done

if [ -z "$EDGE_PATH" ]; then
    echo -e "${RED}✗ 未找到 Edge 浏览器${NC}"
    exit 1
fi

echo -e "Edge 路径: ${YELLOW}${EDGE_PATH}${NC}"
echo -e "CDP 端口: ${YELLOW}${CDP_PORT}${NC}"

if netstat -tlnp 2>/dev/null | grep -q ":${CDP_PORT} "; then
    echo -e "${GREEN}✓ CDP 端口 ${CDP_PORT} 已在监听${NC}"
    exit 0
fi

echo -e "${YELLOW}启动 Edge 浏览器...${NC}"

USER_DATA_DIR="$HOME/.edge-cdp-profile"
mkdir -p "$USER_DATA_DIR"

powershell.exe -Command "
    Start-Process -FilePath '$EDGE_PATH' -ArgumentList @(
        '--remote-debugging-port=${CDP_PORT}',
        '--user-data-dir=$USER_DATA_DIR',
        '--no-first-run',
        '--no-default-browser-check'
    ) -WindowStyle Normal
" 2>/dev/null

echo -e "${YELLOW}等待 CDP 端口就绪...${NC}"
for i in {1..30}; do
    if netstat -tlnp 2>/dev/null | grep -q ":${CDP_PORT} "; then
        echo -e "${GREEN}✓ Edge 已启动，CDP 端口 ${CDP_PORT} 就绪${NC}"
        echo ""
        echo -e "请在 Edge 浏览器中:"
        echo -e "1. 登录 OKX 账户"
        echo -e "2. 访问 https://www.okx.com/zh-hans/orbit/feed"
        exit 0
    fi
    sleep 1
done

echo -e "${RED}✗ CDP 端口启动超时${NC}"
exit 1
