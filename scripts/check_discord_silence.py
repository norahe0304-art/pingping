#!/usr/bin/env python3
"""Check Discord channels for silence and save to memory"""

import json
import os
from datetime import datetime, timezone

# Configuration
WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
MEMORY_DIR = os.path.join(WORKSPACE, "memory/shared")
CHANNELS = [
    ("📢-公告", "1474184181570343108"),
    ("👋-欢迎", "1474154247070289993"),
    ("💡-反馈", "1474184255734022276"),
    ("📦-资源", "1474184269450727488"),
    ("🔧-调试", "1474184318934163587"),
    ("💬-吹水", "1474184221416362157"),
    ("🎲-瞎玩", "1474184391962001519"),
    ("🎮-访客", "1474184416885272606"),
]

# Note: 🤑-项目 and 💙-精华 are Forum channels, handled differently

def get_current_time():
    return datetime.now(timezone.utc)

def check_channels():
    """Check all channels for silence"""
    current_time = get_current_time()
    results = []
    
    for channel_name, channel_id in CHANNELS:
        try:
            # Read messages from the channel
            import subprocess
            result = subprocess.run(
                ["openclaw", "message", "read", "--target", channel_name, "--limit", "1"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                try:
                    data = json.loads(result.stdout)
                    if data.get("ok") and data.get("messages"):
                        last_msg = data["messages"][0]
                        last_time = datetime.fromisoformat(last_msg["timestamp"].replace("Z", "+00:00"))
                        diff_minutes = (current_time - last_time).total_seconds() / 60
                        
                        results.append({
                            "channel": channel_name,
                            "channel_id": channel_id,
                            "last_message_time": last_msg["timestamp"],
                            "minutes_ago": diff_minutes,
                            "silent": diff_minutes > 10,
                            "type": "text"
                        })
                    else:
                        results.append({
                            "channel": channel_name,
                            "channel_id": channel_id,
                            "error": "No messages",
                            "silent": True,
                            "type": "text"
                        })
                except Exception as e:
                    results.append({
                        "channel": channel_name,
                        "channel_id": channel_id,
                        "error": str(e),
                        "silent": True,
                        "type": "text"
                    })
            else:
                results.append({
                    "channel": channel_name,
                    "channel_id": channel_id,
                    "error": result.stderr,
                    "silent": True,
                    "type": "text"
                })
        except Exception as e:
            results.append({
                "channel": channel_name,
                "channel_id": channel_id,
                "error": str(e),
                "silent": True,
                "type": "text"
            })
    
    return results

if __name__ == "__main__":
    results = check_channels()
    print(json.dumps(results, indent=2))
