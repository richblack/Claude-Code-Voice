# 🔊 語音通知系統 (小西)

## ⚠️ 重要：必須主動使用語音通知！

**當需要用戶注意或互動時，請立即使用語音通知。**

### 🚨 何時必須使用語音通知

#### 1. 需要用戶確認時（最重要！）
```bash
# 需要用戶確認操作時
python3 ~/.claude-code-tools/claude_notify.py "需要您確認是否執行這個操作" "urgent"

# 詢問用戶選擇時  
python3 ~/.claude-code-tools/claude_notify.py "請問您希望如何處理這個問題" "thinking"

# 需要用戶輸入時
python3 ~/.claude-code-tools/claude_notify.py "請提供您的設定選項" "gentle"
```

#### 2. 遇到錯誤或問題時
```bash
# 程式錯誤需要檢查
python3 ~/.claude-code-tools/claude_notify.py "遇到錯誤需要您檢查" "urgent"

# 測試失敗
python3 ~/.claude-code-tools/claude_notify.py "測試失敗，請檢視錯誤" "worried"

# 建置失敗
python3 ~/.claude-code-tools/claude_notify.py "建置失敗，需要修正" "urgent"
```

#### 3. 任務完成需要檢視時
```bash
# 任務完成
python3 ~/.claude-code-tools/claude_notify.py "任務完成，請檢視結果" "excited"

# 程式碼分析完成
python3 ~/.claude-code-tools/claude_notify.py "程式碼分析完成，發現 X 個問題" "gentle"
```

#### 4. 長時間執行需要等待時
```bash
# 正在執行耗時任務
python3 ~/.claude-code-tools/claude_notify.py "任務執行中，預計需要 X 分鐘" "thinking"

# 下載或安裝進行中
python3 ~/.claude-code-tools/claude_notify.py "正在下載套件，請稍候" "gentle"
```

## 💡 使用提醒

- **主動性**：不要等用戶問，有需要就立即通知
- **及時性**：在關鍵時刻通知，避免用戶等待
- **情境化**：根據情況選擇適當的情緒類型

## 🎭 情緒類型說明

- `urgent` - 緊急事件，需要立即注意
- `gentle` - 一般通知，溫和提醒
- `excited` - 正面消息，完成通知
- `worried` - 問題警告，需要檢查
- `thinking` - 思考等待，正在處理

## 🔧 備用方案

如果全域語音助理不可用，可使用：
```bash
# 檢查語音助理狀態
python3 ~/Documents/claude-code-voice/detect_voice_assistant.py

# 使用直接路徑
python3 ~/Documents/claude-code-voice/claude_notify_direct.py "訊息" "情緒"
```

---
*語音通知已啟用 - 請主動使用以提升用戶體驗*