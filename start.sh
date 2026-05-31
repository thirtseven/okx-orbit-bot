#!/bin/bash
# OKX Orbit Bot 启动脚本

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}=== OKX Orbit Bot 启动脚本 ===${NC}"

# 停止现有进程
echo -e "${YELLOW}停止现有进程...${NC}"
pkill -f "python3 main.py" 2>/dev/null
tmux kill-session -t okx-orbit 2>/dev/null
sleep 2

# 启动应用
echo -e "${YELLOW}启动 OKX Orbit Bot...${NC}"
cd /mnt/c/Users/Lenovo/okx-orbit-bot
tmux new-session -d -s okx-orbit "python3 main.py 2>&1 | tee /tmp/okx-orbit.log"
sleep 8

# 检查应用状态
if lsof -i :8081 > /dev/null 2>&1; then
    echo -e "${GREEN}✓ OKX Orbit Bot 已启动 (端口 8081)${NC}"
else
    echo -e "${RED}✗ OKX Orbit Bot 启动失败${NC}"
    exit 1
fi

# 获取 WSL IP
WSL_IP=$(hostname -I | awk '{print $1}')
echo ""
echo -e "${GREEN}=== 访问地址 ===${NC}"
echo -e "从 WSL 访问: ${YELLOW}http://localhost:8081/${NC}"
echo -e "从 Windows 访问: ${YELLOW}http://${WSL_IP}:8081/${NC}"
echo ""
echo -e "${GREEN}=== 管理命令 ===${NC}"
echo -e "查看日志: ${YELLOW}tail -f /tmp/okx-orbit.log${NC}"
echo -e "停止服务: ${YELLOW}tmux kill-session -t okx-orbit${NC}"
echo -e "重启服务: ${YELLOW}okx-orbit-restart${NC}"
