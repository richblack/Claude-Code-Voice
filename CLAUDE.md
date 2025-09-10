# Claude Code 語音助理使用說明 (小西)

## ⚠️ 重要提醒

**請主動使用語音通知功能！** 特別是在以下情況時：

## 🚨 重要：何時必須使用語音通知

### 1. 需要用戶確認時 (最重要!)
```bash
# 需要用戶按 yes/no 或選擇選項時
python3 ~/.claude-code-tools/claude_notify.py "需要您確認是否執行這個操作" "urgent"

# 詢問用戶意見時
python3 ~/.claude-code-tools/claude_notify.py "請問您希望如何處理這個問題" "thinking"

# 需要用戶輸入時
python3 ~/.claude-code-tools/claude_notify.py "請提供您的設定選項" "gentle"
```

### 2. 其他重要情況
```bash
# 遇到錯誤需要協助
python3 ~/.claude-code-tools/claude_notify.py "遇到錯誤需要您檢查" "urgent"

# 任務完成需要檢視
python3 ~/.claude-code-tools/claude_notify.py "任務完成，請檢視結果" "excited"

# 長時間等待時
python3 ~/.claude-code-tools/claude_notify.py "任務執行中，請稍候" "thinking"
```

## 概述

這是一個專為 Claude Code 設計的**多實例語音通知系統**，支援同時管理多個 Claude Code 會話，當任何實例需要協助時會透過語音和訊息通知使用者。

## 🚀 多實例支援

系統現在支援多個 Claude Code 實例同時運行：
- 每個新的 Claude Code 會話都會自動註冊到語音助理
- 按快捷鍵時可以選擇要對話的實例
- 各實例可以獨立發送語音通知

### 註冊新實例

每個新的 Claude Code 專案啟動時執行：

```bash
python3 ~/.claude-code-tools/register_claude.py
```

## ⚡ 快速通知 - 直接給 Claude Code 使用

當你需要通知使用者時，請使用：

```bash
python3 ~/.claude-code-tools/claude_notify.py "需要使用者協助的訊息" "urgent"
```

### 常用情境

```bash
# 需要用戶確認
python3 ~/.claude-code-tools/claude_notify.py "需要您確認程式碼變更" "gentle"

# 遇到錯誤需要協助  
python3 ~/.claude-code-tools/claude_notify.py "遇到錯誤需要您協助" "urgent"

# 任務完成通知
python3 ~/.claude-code-tools/claude_notify.py "任務已完成，請檢視結果" "excited"

# 等待用戶輸入
python3 ~/.claude-code-tools/claude_notify.py "請提供更多資訊以繼續" "thinking"
```

## 安裝位置

- Python 版本（推薦）: `~/.claude-code-tools/voice_assistant.py`
- JavaScript 版本（備用）: `~/.claude-code-tools/js-version/voice-assistant.js`

## 統一設定檔

所有設定都儲存在 `~/.claude-code-tools/config.json`，包括：

- 助理名字（預設：小西）
- 通知模式
- 語音設定
- 您的音訊裝置清單

## 在專案中使用

### 方法 1: 直接調用（推薦）

在任何專案中，當你需要通知使用者時，執行：

```bash
# 基本通知
python3 ~/.claude-code-tools/voice_assistant.py help

# 緊急通知
python3 ~/.claude-code-tools/voice_assistant.py notify "需要您立即處理" --emotion urgent

# Git 衝突
python3 ~/.claude-code-tools/voice_assistant.py git-conflict

# 測試失敗
python3 ~/.claude-code-tools/voice_assistant.py test-failed "3 個測試失敗"

# 建置錯誤
python3 ~/.claude-code-tools/voice_assistant.py build-error
```

### 方法 2: 在 Python 程式碼中使用

```python
import sys
from pathlib import Path
sys.path.append(str(Path.home() / '.claude-code-tools'))

from voice_assistant import ClaudeVoiceAssistant

# 建立助理
assistant = ClaudeVoiceAssistant()

# 一般通知
assistant.notify('需要您的協助')

# 帶情緒的通知
assistant.notify('發現重大問題', emotion='urgent', details='資料庫連線失敗')

# 使用預設情境
assistant.quick_notify('git_conflict', 'urgent')
```

## 快速設定

```bash
# 設定您的助理名字
python3 ~/.claude-code-tools/voice_assistant.py config --set assistant_name "小助手"

# 加入您的藍牙耳機
python3 ~/.claude-code-tools/voice_assistant.py config --add-device "OpenMove by Shokz"

# 切換通知模式
python3 ~/.claude-code-tools/voice_assistant.py mode silent

# 查看目前設定
python3 ~/.claude-code-tools/voice_assistant.py config --show
```

## 情境化通知類型

- `blocked` - Claude Code 被阻塞
- `need_help` - 需要協助
- `task_completed` - 任務完成
- `error` - 遇到錯誤
- `git_conflict` - Git 衝突
- `test_failed` - 測試失敗
- `build_error` - 建置錯誤
- `dependency_issue` - 套件相依性問題
- `permission_denied` - 權限不足
- `file_not_found` - 找不到檔案
- `review_required` - 需要檢視程式碼
- `deployment_ready` - 部署準備就緒

## 情緒前綴

- `urgent` - 快來看看！
- `gentle` - 嗨，打擾一下，
- `excited` - 太棒了！
- `worried` - 糟糕，
- `thinking` - 嗯...讓我想想，

## 測試語音功能

```bash
python3 ~/.claude-code-tools/voice_assistant.py test
```

## 智慧耳機偵測

當您的藍牙耳機連接時，即使在 silent 模式下也會自動啟用語音通知。
目前您的裝置清單包含：OpenMove by Shokz

新增更多裝置：

```bash
python3 ~/.claude-code-tools/voice_assistant.py config --add-device "您的耳機名稱"
```
# 🔊 語音通知系統

此專案已連接小西語音助理系統。當你需要通知使用者時，請使用：

## 基本用法
```bash
python3 ~/.claude-code-tools/claude_notify.py "訊息內容" "情緒類型"
```

## 常用範例
```bash
# 需要用戶協助
python3 ~/.claude-code-tools/claude_notify.py "需要您的協助解決問題" "gentle"

# 遇到錯誤
python3 ~/.claude-code-tools/claude_notify.py "程式執行出錯，請檢查" "urgent"  

# 任務完成
python3 ~/.claude-code-tools/claude_notify.py "任務已完成，請檢視結果" "excited"

# 等待輸入
python3 ~/.claude-code-tools/claude_notify.py "請提供更多資訊以繼續" "thinking"
```

## 情緒類型
- `urgent` - 緊急事件
- `gentle` - 一般通知
- `excited` - 正面消息
- `worried` - 問題警告
- `thinking` - 需要思考

**重要**: 請在需要用戶注意或協助時主動使用語音通知，這樣可以及時提醒用戶處理。

## 語音通知設置

**⚠️ 重要：需要用戶互動時請使用語音通知！**

詳細語音通知指示請參閱：`.claude-voice/voice_instructions.md`

快速使用：
```bash
# 需要用戶確認時（最重要！）
python3 .claude-voice/claude_notify.py "需要您確認是否執行" "urgent"

# 任務完成時
python3 .claude-voice/claude_notify.py "任務完成請檢視" "excited"
```

管理工具：`.claude-voice/manage.sh`  
語音測試：`.claude-voice/manage.sh test`  
移除語音功能：`.claude-voice/manage.sh remove`

[語音通知已啟用 - .claude-code-tools]
