#!/bin/bash
# Claude Code 語音通知一鍵安裝腳本
# 下載並設置 claude-code-voice 到標準位置

set -e

echo "🚀 Claude Code 語音通知一鍵安裝"
echo "==============================="

INSTALL_DIR="$HOME/Documents/claude-code-voice"

# 檢查是否已安裝
if [[ -d "$INSTALL_DIR" ]]; then
    echo "⚠️  已存在安裝: $INSTALL_DIR"
    read -p "是否要重新安裝? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ 取消安裝"
        exit 0
    fi
    
    echo "🗑️  移除舊版本..."
    rm -rf "$INSTALL_DIR"
fi

# 檢查 git
if ! command -v git &> /dev/null; then
    echo "❌ 需要 Git"
    exit 1
fi

# 建立 Documents 目錄（如果不存在）
mkdir -p "$HOME/Documents"

# 下載 claude-code-voice
echo "📥 下載 claude-code-voice..."
git clone https://github.com/richblack/Claude-Code-Voice.git "$INSTALL_DIR"

if [[ ! -d "$INSTALL_DIR" ]]; then
    echo "❌ 下載失敗"
    exit 1
fi

echo "✅ 下載完成: $INSTALL_DIR"

# 設置權限
chmod +x "$INSTALL_DIR"/*.py 2>/dev/null || true
chmod +x "$INSTALL_DIR"/*.sh 2>/dev/null || true

echo ""
echo "🎉 安裝完成！"
echo ""
echo "📋 使用方法："
echo "1. 在新專案中執行："
echo "   python3 ~/Documents/claude-code-voice/init_voice.py"
echo ""
echo "2. 或使用快速腳本："
echo "   curl -fsSL https://raw.githubusercontent.com/richblack/Claude-Code-Voice/main/quick_init.sh | bash"
echo ""
echo "3. 然後就可以使用語音通知："
echo "   python3 .claude-voice/claude_notify.py \"訊息\" \"情緒\""