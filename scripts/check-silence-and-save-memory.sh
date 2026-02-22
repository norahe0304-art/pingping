#!/bin/bash
# 检查各 Discord 群是否超过10分钟沉默，如果是则自动存记忆

WORKSPACE="$HOME/clawd/workspace"
MEMORY_DIR="$WORKSPACE/memory/shared"
LAST_ACTIVE_FILE="$MEMORY_DIR/last-active.json"

# 需要监控的频道（可配置）
CHANNELS=(
  "1474184255734022276"  # 🎲-瞎玩
)

# 创建 memory 目录
mkdir -p "$MEMORY_DIR"

# 获取当前时间
NOW=$(date +%s)

# 检查每个频道
for CHANNEL_ID in "${CHANNELS[@]}"; do
  # 获取频道最近一条消息的时间（使用 Discord API）
  LAST_MSG_TIME=$(curl -s "https://discord.com/api/v9/channels/$CHANNEL_ID/messages?limit=1" \
    -H "Authorization: Bot $(grep -E '^discord.*token' ~/openclaw/config.yaml | awk '{print $2}')" \
    2>/dev/null | jq -r '.[0].timestamp // empty' 2>/dev/null)
  
  if [ -z "$LAST_MSG_TIME" ]; then
    continue
  fi
  
  # 转换时间戳
  LAST_MSG_EPOCH=$(date -d "$LAST_MSG_TIME" +%s 2>/dev/null)
  if [ -z "$LAST_MSG_EPOCH" ]; then
    continue
  fi
  
  DIFF=$((NOW - LAST_MSG_EPOCH))
  
  # 超过10分钟（600秒）
  if [ $DIFF -gt 600 ]; then
    echo "[$(date)] Channel $CHANNEL_ID 沉默超过10分钟 ($DIFF 秒)，触发记忆保存"
    
    # 拉取最近消息历史
    MESSAGES=$(curl -s "https://discord.com/api/v9/channels/$CHANNEL_ID/messages?limit=50" \
      -H "Authorization: Bot $(grep -E '^discord.*token' ~/openclaw/config.yaml | awk '{print $2}')" \
      2>/dev/null | jq -r '.[] | "\(.author.username): \(.content)"' 2>/dev/null)
    
    # 存到记忆文件
    DATE=$(date +%Y-%m-%d)
    echo "## $DATE - Channel $CHANNEL_ID" >> "$MEMORY_DIR/shared.md"
    echo "$MESSAGES" >> "$MEMORY_DIR/shared.md"
    echo "" >> "$MEMORY_DIR/shared.md"
    
    echo "[$(date)] 记忆已保存"
  fi
done
