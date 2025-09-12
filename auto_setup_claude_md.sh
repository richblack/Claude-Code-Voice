#!/bin/bash
# 自動執行 CLAUDE.md 設定的擴充腳本
# 這個腳本會被其他安裝流程呼叫

set -e

echo "🔧 自動設定 CLAUDE.md 語音通知..."

# 尋找 claude-code-voice 位置
CLAUDE_VOICE_PATHS=(
    "$PWD/claude-code-voice"
    "$HOME/Documents/claude-code-voice"
    "$HOME/claude-code-voice" 
    "$HOME/Documents/claude-code-voice-main"
)

FOUND_PATH=""
for path in "${CLAUDE_VOICE_PATHS[@]}"; do
    if [[ -f "$path/init_voice.py" ]]; then
        FOUND_PATH="$path"
        break
    elif [[ -f "$path/setup_claude_md.py" ]]; then
        FOUND_PATH="$path"
        break
    fi
done

if [[ -z "$FOUND_PATH" ]]; then
    echo "⚠️ 找不到 claude-code-voice，手動建立基本 CLAUDE.md"
    
    # 建立基本的 CLAUDE.md
    cat > CLAUDE.md << 'EOF'
# CLAUDE

## 需查看文件

每次開始工作前後要查看及維護 rfp，requirements, kanban，留下記錄。

每個工作階段要留下記憶，以免下次開啓時要從零開始。

## 🔊 語音通知系統 (小西)

### ⚠️ 重要：必須主動使用語音通知

**當需要用戶注意或互動時，請立即使用語音通知。**

### 🔴 最高優先級：第一次需要人工介入必須通知！例如 Bash command

**絕對規則：當你第一次遇到需要用戶介入的情況時，必須立即發送語音通知，不要等待或假設用戶在看螢幕。**

#### 🚨 何時必須使用語音通知

##### 1. 需要用戶確認時（最重要！）

```bash
# 需要用戶確認操作時
python3 ~/Documents/claude-code-voice/claude_notify.py "需要您確認是否執行這個操作" "urgent"

# 詢問用戶選擇時  
python3 ~/Documents/claude-code-voice/claude_notify.py "請問您希望如何處理這個問題" "thinking"

# 需要用戶輸入時
python3 ~/Documents/claude-code-voice/claude_notify.py "請提供您的設定選項" "gentle"
```

##### 2. 遇到錯誤或問題時

```bash
# 程式錯誤需要檢查
python3 ~/Documents/claude-code-voice/claude_notify.py "遇到錯誤需要您檢查" "urgent"

# 測試失敗
python3 ~/Documents/claude-code-voice/claude_notify.py "測試失敗，請檢視錯誤" "worried"

# 建置失敗
python3 ~/Documents/claude-code-voice/claude_notify.py "建置失敗，需要修正" "urgent"
```

##### 3. 任務完成需要檢視時

```bash
# 任務完成
python3 ~/Documents/claude-code-voice/claude_notify.py "任務完成，請檢視結果" "excited"

# 程式碼分析完成
python3 ~/Documents/claude-code-voice/claude_notify.py "程式碼分析完成，發現 X 個問題" "gentle"
```

### 🎭 情緒類型說明

- `urgent` - 緊急事件，需要立即注意
- `gentle` - 一般通知，溫和提醒
- `excited` - 正面消息，完成通知
- `worried` - 問題警告，需要檢查
- `thinking` - 思考等待，正在處理

### 🔧 備用方案

如果全域語音助理不可用，可使用：

```bash
# 檢查語音助理狀態
python3 ~/Documents/claude-code-voice/detect_voice_assistant.py

# 使用直接路徑
python3 ~/Documents/claude-code-voice/claude_notify_direct.py "訊息" "情緒"
```

## 語音通知使用指引

語音通知已啟用 - 請主動使用以提升用戶體驗
EOF
    
    echo "✅ 基本 CLAUDE.md 已建立"
    exit 0
fi

echo "✅ 找到 claude-code-voice: $FOUND_PATH"

# 優先使用 init_voice.py
if [[ -f "$FOUND_PATH/init_voice.py" ]]; then
    echo "🚀 執行 init_voice.py..."
    python3 "$FOUND_PATH/init_voice.py"
elif [[ -f "$FOUND_PATH/setup_claude_md.py" ]]; then
    echo "🚀 執行 setup_claude_md.py..."
    python3 "$FOUND_PATH/setup_claude_md.py"
else
    echo "❌ 找不到設定腳本"
    exit 1
fi

echo "✅ CLAUDE.md 語音通知設定完成！"