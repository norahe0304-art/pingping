#!/bin/bash
# 生成 skills index
# 用法: ./generate-skill-index.sh

SKILLS_DIR="$HOME/.agents/skills"
INDEX_FILE="$SKILLS_DIR/index.json"

echo "{" > "$INDEX_FILE"
echo '  "skills": [' >> "$INDEX_FILE"

first=true
for skill_dir in "$SKILLS_DIR"/*/; do
  if [ -f "$skill_dir/SKILL.md" ]; then
    skill_name=$(basename "$skill_dir")
    
    # 读取 description (第一行非空)
    description=$(grep -m1 "^[^#]" "$skill_dir/SKILL.md" | head -c 200)
    
    if [ "$first" = true ]; then
      first=false
    else
      echo "," >> "$INDEX_FILE"
    fi
    
    printf '    {"name": "%s", "description": "%s"}' "$skill_name" "$description" >> "$INDEX_FILE"
  fi
done

echo "" >> "$INDEX_FILE"
echo "  ]" >> "$INDEX_FILE"
echo "}" >> "$INDEX_FILE"

echo "Done! Index generated at $INDEX_FILE"
