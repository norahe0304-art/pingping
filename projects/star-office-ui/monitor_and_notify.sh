#!/bin/bash
# Star Office 状态监控 + Discord 通知
# 需要安装 openclaw CLI 并配置好

RESPONSE=$(curl -s http://127.0.0.1:18791/status)
STATE=$(echo $RESPONSE | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('state','unknown'))")
DETAIL=$(echo $RESPONSE | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('detail',''))")
UPDATED=$(echo $RESPONSE | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('updated_at','')[11:19])")

MESSAGE="📊 Star Office 监控
状态: $STATE
详情: $DETAIL
更新时间: $UPDATED"

# 发送到 Discord 频道
openclaw message send --channel discord --target 1476795665618042930 --message "$MESSAGE"
