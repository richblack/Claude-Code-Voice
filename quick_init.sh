#!/bin/bash
# Claude Code 語音通知快速初始化腳本
# 在新專案中執行此腳本，會自動設置語音通知功能

set -e

echo "🚀 Claude Code 語音通知快速初始化"
echo "=================================="

# 檢查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 需要 Python 3"
    exit 1
fi

# 尋找 claude-code-voice 位置
CLAUDE_VOICE_PATHS=(
    "$HOME/Documents/claude-code-voice"
    "$HOME/claude-code-voice" 
    "$HOME/Documents/claude-code-voice-main"
)

FOUND_PATH=""
for path in "${CLAUDE_VOICE_PATHS[@]}"; do
    if [[ -f "$path/init_voice.py" ]]; then
        FOUND_PATH="$path"
        break
    fi
done

if [[ -z "$FOUND_PATH" ]]; then
    echo "❌ 找不到 claude-code-voice"
    echo "💡 請先執行："
    echo "   curl -fsSL https://raw.githubusercontent.com/youlinhsieh/claude-code-voice/main/quick_install.sh | bash"
    exit 1
fi

echo "✅ 找到 claude-code-voice: $FOUND_PATH"

# 執行初始化
echo "🔧 正在初始化語音通知系統..."
python3 "$FOUND_PATH/init_voice.py"

echo ""
echo "🎉 設置完成！現在可以使用："
echo "   python3 .claude-voice/claude_notify.py \"訊息\" \"情緒\""