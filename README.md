# Claude Code 語音助理工具

一個為 Claude Code 設計的智慧語音通知系統，讓 Claude Code 在需要用戶互動時能主動語音通知您。

> **⚠️ 注意：此工具僅支援 macOS**  
> 本工具使用 macOS 內建的 `say` 命令進行語音合成，因此只能在 Mac 系統上運行。

## 🌟 核心特色

- 🔊 **智慧語音通知**: Claude Code 需要協助時自動語音提醒
- 📁 **專案內建**: 每個專案都有獨立的語音通知系統
- ⚙️ **自動初始化**: 一行指令就能為新專案設置語音通知
- 🔍 **智慧尋找**: 自動找到 claude-code-voice 並複製到專案內
- 🎵 **情境化通知**: 根據不同情況使用不同語音提示
- 🔔 **系統通知整合**: 同時發送語音和視覺通知

## 🚀 快速設置

### **第一步：一次性系統安裝**

```bash
# 一鍵安裝（一台電腦只需執行一次）
curl -fsSL https://raw.githubusercontent.com/richblack/Claude-Code-Voice/main/quick_install.sh | bash
```

或手動安裝：

```bash
git clone https://github.com/youlinhsieh/claude-code-voice.git ~/Documents/claude-code-voice
```

### **第二步：為新專案設置語音通知**

**在 VSCode 打開新專案後，執行以下任一指令：**

```bash
# 方法一：直接初始化
python3 ~/Documents/claude-code-voice/init_voice.py

# 方法二：使用快速腳本
curl -fsSL https://raw.githubusercontent.com/richblack/Claude-Code-Voice/main/quick_init.sh | bash
```

✅ **設置完成後，專案內會出現：**

- `.claude-voice/` 目錄（包含語音通知系統）
- `CLAUDE.md` 更新（包含使用說明）

## 🎯 使用方法

### **在專案中使用語音通知**

**設置完成後，在專案中直接使用：**

```bash
# 需要用戶確認時（最重要！）
python3 ~/Documents/claude-code-voice/claude_notify.py "需要您確認是否執行" "urgent"

# 任務完成時
python3 ~/Documents/claude-code-voice/claude_notify.py "任務完成請檢視" "excited"

# 遇到錯誤時
python3 ~/Documents/claude-code-voice/claude_notify.py "發生錯誤需要協助" "worried"

# 需要等待時
python3 ~/Documents/claude-code-voice/claude_notify.py "任務執行中請稍候" "thinking"

# 一般通知
python3 ~/Documents/claude-code-voice/claude_notify.py "需要您的協助" "gentle"
```

### **智慧路由系統**

專案內的 `claude_notify.py` 會自動選擇最佳的語音助理：

1. **全域助理** (`~/Documents/claude-code-voice/`) - 新系統預設位置
2. **本地助理** (`./.claude-voice/`) - 專案內建版本
3. **直接路徑** (`~/Documents/claude-code-voice/`) - 備用方案

### **測試和管理**

```bash
# 測試語音通知功能
python3 .claude-voice/claude_notify.py "測試語音通知" "excited"

# 檢查語音助理狀態
python3 ~/Documents/claude-code-voice/detect_voice_assistant.py

# 重新初始化專案語音通知
python3 ~/Documents/claude-code-voice/init_voice.py
```

## 🚨 Claude Code 必須使用語音通知的情況

### 1. 需要用戶確認時（最重要！）

```bash
python3 .claude-voice/claude_notify.py "需要您確認是否執行" "urgent"
```

### 2. 遇到錯誤時

```bash
python3 .claude-voice/claude_notify.py "發生錯誤需要協助" "worried"
```

### 3. 任務完成時

```bash
python3 .claude-voice/claude_notify.py "任務完成請檢視" "excited"
```

### 4. 需要等待時

```bash
python3 .claude-voice/claude_notify.py "任務執行中請稍候" "thinking"
```

### 5. 需要用戶輸入時

```bash
python3 .claude-voice/claude_notify.py "需要您提供更多資訊" "gentle"
```

## 🎭 情緒類型

- `urgent` - 緊急事件，需要立即注意
- `excited` - 正面消息，完成通知
- `worried` - 問題警告，需要檢查
- `thinking` - 思考等待，正在處理
- `gentle` - 一般通知，溫和提醒

## 📋 專案結構

設置完成後，專案內會有以下結構：

```
your-project/
├── .claude-voice/
│   ├── claude_notify.py        # 語音通知入口（智慧路由）
│   ├── voice_assistant.py      # 語音助理核心
│   ├── claude_notify_direct.py # 直接通知腳本
│   ├── config.json            # 語音設定檔
│   └── .claude-voice-config.json # 專案設定
└── CLAUDE.md                   # 更新或建立使用說明
```

## 🔇 模式設定

此工具支援三種模式：

- **full** (預設) - 完整語音通知 + 系統通知
- **silent** - 靜音模式，僅系統通知，無語音
- **off** - 關閉所有通知

```bash
# 切換模式
python3 .claude-voice/voice_assistant.py mode [full|silent|off]
```

**智慧耳機偵測**：當偵測到藍牙耳機連接時，即使在 silent 模式下也會自動啟用語音通知。

## 🗣️ 自由語音合成功能

除了預設的情境化通知，本工具還支援**完全自訂的語音合成**：

```bash
# 說任何您想要的內容
python3 .claude-voice/voice_assistant.py say "現在是下午三點，該休息一下了"

# Claude Code 也可以用這個功能說出任何訊息
python3 .claude-voice/voice_assistant.py say "程式碼分析完成，共找到 15 個潛在問題"

# 調整語速（可選）
python3 .claude-voice/voice_assistant.py say "這是快速語音測試" --rate 200
```

這個功能讓 Claude Code 可以：

- ✅ 說出任何動態生成的內容
- ✅ 報告具體的數據和結果  
- ✅ 提供詳細的狀態更新
- ✅ 不受限於預設的情緒模板

## 📁 主要檔案

此工具包含以下核心檔案：

- `set_voice.sh` - 主要安裝設置腳本
- `voice_assistant.py` - 語音助理核心模組
- `claude_notify.py` - 語音通知工具
- `claude_notify_direct.py` - 直接語音通知工具
- `register_claude.py` - Claude Code 實例註冊工具
- `hooks/` - Claude Code 鉤子功能

## 🧪 測試語音功能

```bash
# 測試語音功能
python3 .claude-voice/voice_assistant.py test

# 發送測試通知
python3 .claude-voice/claude_notify.py "測試語音通知" "excited"
```

## 🔧 系統需求

- **作業系統**: macOS（必須）
- **Python**: 3.7+
- **系統命令**: `say`（macOS 內建）
- **推薦工具**: terminal-notifier (透過 `brew install terminal-notifier` 安裝，提供更好的通知體驗)

## ⚙️ 系統設定

### 語音權限設定（必要）

首次使用時，macOS 可能會要求授權語音功能：

1. **系統偏好設定** → **安全性與隱私權** → **隱私權**
2. 點選左側的 **輔助使用**
3. 解鎖設定（點擊左下角鎖頭圖示）
4. 勾選 **Terminal** 或您使用的終端機應用程式
5. 如果使用 Claude Code，也需要勾選相關應用程式

### 通知權限設定（建議）

為了收到系統通知：

1. **系統偏好設定** → **通知**
2. 找到 **Terminal** 或 **script editor**
3. 啟用 **允許通知**
4. 選擇通知樣式（橫幅或提醒）

### 測試設定

設定完成後，可執行以下命令測試：

```bash
# 測試語音功能
say "語音測試成功"

# 測試完整工具
python3 .claude-voice/voice_assistant.py test
```

## 💡 重要提醒

**記住：即使對話很長，也要持續使用語音通知！**

Claude Code 必須在以下情況主動使用語音通知：

- ✅ 需要用戶確認任何操作
- ✅ 遇到錯誤或異常
- ✅ 任務完成需要檢視
- ✅ 需要用戶提供更多資訊
- ✅ 執行長時間任務時

語音通知是 Claude Code 與用戶互動的重要橋樑，請務必善用！

## 🎯 使用流程總結

1. **權限設定**: 在系統偏好設定中授權語音和通知權限
2. **安裝工具**: `bash /Users/your_name/Documents/claude-code-voice/set_voice.sh`
3. **測試功能**: `python3 .claude-voice/voice_assistant.py test`
4. **開始使用**: `python3 .claude-voice/claude_notify.py "訊息" "情緒"`
5. **註冊實例**: `python3 ~/Documents/claude-code-voice/register_claude.py`
