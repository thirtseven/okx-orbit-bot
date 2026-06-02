#!/bin/bash
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}=== OKX Orbit 域名配置脚本 ===${NC}"
echo ""

WSL_IP=$(hostname -I | awk '{print $1}')
echo -e "WSL IP: ${YELLOW}${WSL_IP}${NC}"
echo ""

echo -e "${GREEN}请在 Windows 中执行以下操作:${NC}"
echo ""
echo -e "1. 以管理员身份打开 PowerShell"
echo -e "2. 运行以下命令添加 hosts 记录:"
echo ""
echo -e "   ${YELLOW}Add-Content -Path C:\\Windows\\System32\\drivers\\etc\\hosts -Value \"${WSL_IP} orbit.okx.local\"${NC}"
echo ""
echo -e "3. 刷新 DNS 缓存:"
echo ""
echo -e "   ${YELLOW}ipconfig /flushdns${NC}"
echo ""
echo -e "${GREEN}配置完成后访问:${NC}"
echo -e "   ${YELLOW}http://orbit.okx.local:8081/${NC}"
