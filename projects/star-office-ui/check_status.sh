#!/bin/bash
# 每5分钟检查 Star Office 状态
RESPONSE=$(curl -s http://127.0.0.1:18791/status)
STATE=$(echo $RESPONSE | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('state','unknown'))")
DETAIL=$(echo $RESPONSE | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('detail',''))")
PROGRESS=$(echo $RESPONSE | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('progress',0))")
UPDATED=$(echo $RESPONSE | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('updated_at',''))")

echo "📊 Star Office 状态监控"
echo "状态: $STATE"
echo "详情: $DETAIL"
echo "进度: $PROGRESS%"
echo "更新时间: $UPDATED"
