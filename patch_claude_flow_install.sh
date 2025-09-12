#!/bin/bash
# Claude Flow Setting 安裝後自動執行 CLAUDE.md 設定
# 這個腳本用來擴充現有的安裝流程

set -e

echo "🔧 Claude Flow Setting 後續設定..."

# 如果當前目錄已經有 claude-code-voice，執行語音設定
if [[ -d "claude-code-voice" && -f "claude-code-voice/init_voice.py" ]]; then
    echo "🚀 找到本地 claude-code-voice，執行語音初始化..."
    python3 claude-code-voice/init_voice.py
elif [[ -f "$HOME/Documents/claude-code-voice/auto_setup_claude_md.sh" ]]; then
    echo "🚀 使用全域語音設定..."
    bash "$HOME/Documents/claude-code-voice/auto_setup_claude_md.sh"
else
    echo "⚠️ 沒有找到語音設定，請手動執行："
    echo "   curl -sSL https://raw.githubusercontent.com/youlinhsieh/claude-code-voice/main/auto_setup_claude_md.sh | bash"
fi

echo "✅ Claude Flow Setting 後續設定完成！"