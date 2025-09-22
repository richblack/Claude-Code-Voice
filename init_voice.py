#!/usr/bin/env python3
"""
新專案語音通知初始化腳本 - 純系統級版本
只在專案中添加 CLAUDE.md 說明，不復製任何檔案
完全依賴系統唯一的語音工具：~/Documents/claude-code-voice/
"""
import os
import sys
import json
from pathlib import Path

def find_claude_voice_source():
    """
    檢查系統級語音工具是否存在
    """
    system_path = Path.home() / 'Documents' / 'claude-code-voice'

    print("🔍 檢查系統級語音工具...")
    print(f"  檢查: {system_path}")

    if system_path.exists() and (system_path / 'voice_assistant.py').exists():
        print(f"✅ 找到系統級語音工具: {system_path}")
        return system_path
    else:
        print("❌ 未找到系統級語音工具")
        print("\n請先安裝系統級語音工具：")
        print("git clone https://github.com/richblack/claude-code-voice.git ~/Documents/claude-code-voice")
        return None

def create_claude_md(project_dir: Path):
    """在專案中創建或更新 CLAUDE.md"""
    claude_md_path = project_dir / 'CLAUDE.md'

    claude_md_content = '''# CLAUDE

## 需查看文件

每次開始工作前後要查看及維護 rfp，requirements, kanban，留下記錄。

每個工作階段要留下記憶，以免下次開啓時要從零開始。

## 🔊 語音通知系統 (小西)

### ⚠️ 重要：必須主動使用語音通知

**當需要用戶注意或互動時，請立即使用語音通知。**

### 🔴 最高優先級：第一次需要人工介入必須通知！

**絕對規則：當你第一次遇到需要用戶介入的情況時，必須立即發送語音通知，不要等待或假設用戶在看螢幕。**

例如：
- 第一次需要確認執行某操作時 → 立即通知
- 第一次遇到錯誤需要處理時 → 立即通知
- 第一次完成任務需要測試時 → 立即通知
- 第一次需要用戶選擇時 → 立即通知

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

##### 4. 長時間執行需要等待時

```bash
# 正在執行耗時任務
python3 ~/Documents/claude-code-voice/claude_notify.py "任務執行中，預計需要 X 分鐘" "thinking"

# 下載或安裝進行中
python3 ~/Documents/claude-code-voice/claude_notify.py "正在下載套件，請稍候" "gentle"
```

### 💡 使用提醒

- **主動性**：不要等用戶問，有需要就立即通知
- **及時性**：在關鍵時刻通知，避免用戶等待
- **情境化**：根據情況選擇適當的情緒類型

### 🎭 情緒類型說明

- `urgent` - 緊急事件，需要立即注意
- `gentle` - 一般通知，溫和提醒
- `excited` - 正面消息，完成通知
- `worried` - 問題警告，需要檢查
- `thinking` - 思考等待，正在處理

### 🔧 語音通知架構

純系統級架構 - 所有專案共用同一套語音工具：

```bash
# 統一使用方式（所有專案）
python3 ~/Documents/claude-code-voice/claude_notify.py "訊息" "情緒"

# 測試語音功能
python3 ~/Documents/claude-code-voice/voice_assistant.py test

# 直接語音輸出
python3 ~/Documents/claude-code-voice/voice_assistant.py say "任何內容"
```

## 語音通知使用指引

語音通知已啟用 - 請主動使用以提升用戶體驗
'''

    try:
        with open(claude_md_path, 'w', encoding='utf-8') as f:
            f.write(claude_md_content)
        print(f"✅ 已創建/更新 CLAUDE.md: {claude_md_path}")
        return True
    except Exception as e:
        print(f"❌ 創建 CLAUDE.md 失敗: {e}")
        return False

def create_voice_config(project_dir: Path):
    """創建語音配置檔案（輕量級）"""
    config_path = project_dir / '.claude-voice-config.json'

    config = {
        "voice_enabled": True,
        "system_voice_path": "~/Documents/claude-code-voice/claude_notify.py",
        "project_name": project_dir.name,
        "init_date": "2025-09-22",
        "architecture": "system-level-only"
    }

    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"✅ 已創建語音配置: {config_path}")
        return True
    except Exception as e:
        print(f"❌ 創建語音配置失敗: {e}")
        return False

def main():
    """主函數"""
    print("🔧 新專案語音通知初始化 - 純系統級版本")
    print("=" * 50)

    # 檢查系統級語音工具
    source_path = find_claude_voice_source()
    if not source_path:
        return

    # 當前專案目錄
    project_dir = Path.cwd()
    project_name = project_dir.name

    print(f"\n📁 當前專案: {project_name}")
    print(f"📍 專案路徑: {project_dir}")

    success_count = 0
    total_tasks = 2

    # 1. 創建 CLAUDE.md
    print(f"\n📝 創建 CLAUDE.md...")
    if create_claude_md(project_dir):
        success_count += 1

    # 2. 創建語音配置
    print(f"\n⚙️ 創建語音配置...")
    if create_voice_config(project_dir):
        success_count += 1

    # 總結
    print("\n" + "=" * 50)
    if success_count == total_tasks:
        print("✅ 語音通知初始化完成！")
        print(f"\n🎯 使用方式：")
        print(f"python3 ~/Documents/claude-code-voice/claude_notify.py \"訊息\" \"情緒\"")
        print(f"\n💡 測試：")
        print(f"python3 ~/Documents/claude-code-voice/claude_notify.py \"專案 {project_name} 語音通知已設置\" \"excited\"")
    else:
        print(f"⚠️ 部分任務失敗 ({success_count}/{total_tasks})")

    print("\n🔗 系統級語音工具位置:")
    print(f"  {source_path}")
    print("\n📋 專案配置:")
    print(f"  - CLAUDE.md (使用說明)")
    print(f"  - .claude-voice-config.json (輕量配置)")

if __name__ == "__main__":
    main()