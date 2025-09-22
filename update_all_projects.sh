#!/bin/bash

# 更新所有專案的語音通知系統路徑
# 從錯誤的 ~/.claude-code-tools 改為 ~/Documents/claude-code-voice

echo "🔧 開始更新所有專案的語音通知系統..."

# 顏色定義
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 計數器
updated=0
failed=0

# 找出所有包含 .claude-voice 的專案
echo -e "${BLUE}🔍 掃描專案...${NC}"
projects=$(find ~ -name ".claude-voice" -type d 2>/dev/null | grep -v "Library/Caches")

for project_voice_dir in $projects; do
    project_dir=$(dirname "$project_voice_dir")
    project_name=$(basename "$project_dir")

    echo -e "\n${BLUE}📁 處理專案: $project_name${NC}"
    echo "   路徑: $project_dir"

    # 更新 claude_notify.py
    notify_file="$project_voice_dir/claude_notify.py"
    if [ -f "$notify_file" ]; then
        echo "   更新 claude_notify.py..."

        # 複製新版本
        cp ~/Documents/claude-code-voice/claude_notify.py "$notify_file"

        # 修改路徑引用
        sed -i '' 's|~/.claude-code-tools|~/Documents/claude-code-voice|g' "$notify_file"
        sed -i '' 's|\.claude-code-tools|Documents/claude-code-voice|g' "$notify_file"

        echo -e "   ${GREEN}✓ claude_notify.py 已更新${NC}"
    fi

    # 更新 CLAUDE.md
    claude_md="$project_dir/CLAUDE.md"
    if [ -f "$claude_md" ]; then
        echo "   更新 CLAUDE.md..."

        # 替換路徑
        sed -i '' 's|~/.claude-code-tools|~/Documents/claude-code-voice|g' "$claude_md"
        sed -i '' 's|\.claude-code-tools|Documents/claude-code-voice|g' "$claude_md"

        echo -e "   ${GREEN}✓ CLAUDE.md 已更新${NC}"
    fi

    # 更新 voice_assistant.py（如果存在）
    voice_assistant="$project_voice_dir/voice_assistant.py"
    if [ -f "$voice_assistant" ]; then
        echo "   更新 voice_assistant.py..."

        # 複製新版本
        cp ~/Documents/claude-code-voice/voice_assistant.py "$voice_assistant"

        # 修改路徑引用
        sed -i '' 's|~/.claude-code-tools|~/Documents/claude-code-voice|g' "$voice_assistant"
        sed -i '' 's|\.claude-code-tools|Documents/claude-code-voice|g' "$voice_assistant"

        echo -e "   ${GREEN}✓ voice_assistant.py 已更新${NC}"
    fi

    # 更新 claude_notify_direct.py（如果存在）
    direct_notify="$project_voice_dir/claude_notify_direct.py"
    if [ -f "$direct_notify" ]; then
        echo "   更新 claude_notify_direct.py..."

        # 複製新版本
        cp ~/Documents/claude-code-voice/claude_notify_direct.py "$direct_notify"

        # 修改路徑引用
        sed -i '' 's|~/.claude-code-tools|~/Documents/claude-code-voice|g' "$direct_notify"
        sed -i '' 's|\.claude-code-tools|Documents/claude-code-voice|g' "$direct_notify"

        echo -e "   ${GREEN}✓ claude_notify_direct.py 已更新${NC}"
    fi

    ((updated++))
    echo -e "   ${GREEN}✅ 專案更新完成${NC}"
done

echo -e "\n${GREEN}===========================================
✅ 更新完成！
- 已更新專案數: $updated
- 失敗數: $failed
===========================================${NC}"

echo -e "\n${BLUE}💡 測試提示：${NC}"
echo "您可以在任何專案中測試語音通知："
echo -e "${GREEN}python3 ~/Documents/claude-code-voice/claude_notify.py \"測試語音通知\" \"excited\"${NC}"
echo ""
echo "或在專案目錄內："
echo -e "${GREEN}python3 .claude-voice/claude_notify.py \"測試語音通知\" \"excited\"${NC}"