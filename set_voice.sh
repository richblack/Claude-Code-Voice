#!/bin/bash
# 有組織的語音通知設置 - 集中管理所有檔案

echo "📁 設置有組織的語音通知系統..."

# 取得專案目錄
PROJECT_DIR="${1:-$(pwd)}"
PROJECT_NAME=$(basename "$PROJECT_DIR")
TOOLS_DIR="$HOME/.claude-code-tools"

# 創建語音通知專用資料夾
VOICE_DIR="$PROJECT_DIR/.claude-voice"
echo "📁 創建語音通知資料夾: $VOICE_DIR"
mkdir -p "$VOICE_DIR"

echo "🎯 專案: $PROJECT_NAME"
echo "📁 語音資料夾: $VOICE_DIR"

# 1. 複製所有語音相關工具到專用資料夾
echo "📋 複製語音工具到專用資料夾..."
cp "$TOOLS_DIR/claude_notify_direct.py" "$VOICE_DIR/claude_notify.py"
cp "$TOOLS_DIR/voice_assistant.py" "$VOICE_DIR/"
cp "$TOOLS_DIR/test_voice_simple.py" "$VOICE_DIR/"
cp "$TOOLS_DIR/example_user_confirmation.py" "$VOICE_DIR/" 2>/dev/null

# 設置執行權限
chmod +x "$VOICE_DIR/claude_notify.py"
chmod +x "$VOICE_DIR/test_voice_simple.py"

# 2. 創建設定檔（在專用資料夾內）
echo "⚙️ 創建語音設定檔..."
cat > "$VOICE_DIR/config.json" << EOF
{
  "voice_enabled": true,
  "project_name": "$PROJECT_NAME",
  "setup_time": "$(date '+%Y-%m-%d %H:%M:%S')",
  "mode": "direct",
  "reminder_interval": 1800,
  "tools_location": ".claude-voice"
}
EOF

# 2.5. 創建詳細語音指示檔
echo "📋 創建詳細語音指示檔..."
cat > "$VOICE_DIR/voice_instructions.md" << 'EOF'
# 🔊 語音通知系統詳細指示

**⚠️ 重要：需要用戶互動時請使用語音通知！**

## 🚨 必須使用語音通知的情況

### 1. 需要用戶確認時（最重要！）
當 Claude Code 需要用戶確認任何操作時，必須使用語音通知！
```bash
python3 .claude-voice/claude_notify.py "需要您確認是否執行" "urgent"
```

### 2. 遇到錯誤時
當遇到錯誤、異常或無法繼續執行時：
```bash
python3 .claude-voice/claude_notify.py "發生錯誤需要協助" "worried"
```

### 3. 任務完成時
當重要任務完成需要用戶檢視結果時：
```bash
python3 .claude-voice/claude_notify.py "任務完成請檢視" "excited"
```

### 4. 需要等待時
當執行長時間任務需要用戶等待時：
```bash
python3 .claude-voice/claude_notify.py "任務執行中請稍候" "thinking"
```

### 5. 需要用戶輸入時
當需要用戶提供更多資訊或做出選擇時：
```bash
python3 .claude-voice/claude_notify.py "需要您提供更多資訊" "gentle"
```

## 🎭 情緒參數說明

- `urgent` - 緊急情況，需要立即注意
- `excited` - 興奮/成功，好消息
- `worried` - 擔心/錯誤，有問題需要處理
- `thinking` - 思考中，正在處理
- `gentle` - 溫和提醒，一般通知

## 🛠️ 語音工具位置

所有語音相關檔案都在 `.claude-voice/` 資料夾中：
- `claude_notify.py` - 語音通知工具
- `voice_assistant.py` - 語音助理核心
- `test_voice_simple.py` - 語音功能測試
- `config.json` - 語音設定
- `update_claude_md.py` - CLAUDE.md 管理器
- `memory_keeper.sh` - 記憶守護腳本
- `manage.sh` - 管理工具
- `voice_instructions.md` - 本檔案

## 🔧 管理指令

```bash
# 測試語音功能
.claude-voice/manage.sh test

# 發送測試通知
.claude-voice/manage.sh notify "測試訊息" "excited"

# 更新 CLAUDE.md 指示
.claude-voice/manage.sh update

# 啟動記憶守護（背景執行）
.claude-voice/manage.sh keeper-start

# 停止記憶守護
.claude-voice/manage.sh keeper-stop

# 檢查記憶守護狀態
.claude-voice/manage.sh keeper-status

# 完全移除語音功能
.claude-voice/manage.sh remove
```

## 🛡️ 記憶守護系統

記憶守護系統確保語音通知指示不會因為 context window 清理而丟失：
- 每30分鐘檢查 CLAUDE.md 是否包含語音指示
- 如果發現指示遺失，自動重新注入
- 發送語音提醒通知 Claude Code 記憶已恢復

## 🗑️ 移除語音功能

如果不需要語音功能：
1. 執行：`.claude-voice/manage.sh remove`
2. 或直接刪除：`rm -rf .claude-voice/`

兩種方法都會完全清理語音功能。

## 💡 重要提醒

**記住：即使對話很長，也要持續使用語音通知！**

Claude Code 必須在以下情況主動使用語音通知：
- ✅ 需要用戶確認任何操作
- ✅ 遇到錯誤或異常
- ✅ 任務完成需要檢視
- ✅ 需要用戶提供更多資訊
- ✅ 執行長時間任務時

語音通知是 Claude Code 與用戶互動的重要橋樑，請務必善用！

## 📢 初次設置時的回應

當用戶設置語音通知系統後，Claude Code 應該立即回應確認：

```bash
python3 .claude-voice/claude_notify.py "好的，我知道了！會在需要時使用語音通知" "gentle"
```

然後明確回覆用戶：「好的，我知道了會用語音通知。當需要您確認、遇到錯誤、任務完成或需要您協助時，我都會主動發送語音通知提醒您。」

## 🔄 Context Window 清理後的恢復

當 Claude Code 的 context window 被清理後，如果用戶提醒語音通知功能，應該：

1. 立即發送確認語音通知
2. 明確回應表示記住了語音通知功能
3. 承諾會在需要時主動使用

範例回應：
```bash
python3 .claude-voice/claude_notify.py "收到！我會記住使用語音通知功能" "excited"
```

然後回覆：「收到！我已經重新記住語音通知功能，會在需要您協助、確認或遇到問題時主動通知您。謝謝提醒！」
EOF

# 3. 創建集中式的 CLAUDE.md 更新腳本
echo "📝 創建 CLAUDE.md 管理腳本..."
cat > "$VOICE_DIR/update_claude_md.py" << 'EOF'
#!/usr/bin/env python3
"""
CLAUDE.md 語音指示管理器
集中管理語音通知相關的文檔內容
"""
import os
import re
import sys
import json
from pathlib import Path
from datetime import datetime

class ClaudeMdManager:
    def __init__(self):
        self.voice_dir = Path(__file__).parent
        self.project_dir = self.voice_dir.parent
        self.claude_md = self.project_dir / 'CLAUDE.md'
        self.config_file = self.voice_dir / 'config.json'
        
    def load_config(self):
        """載入設定"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {}
    
    def get_voice_instructions(self):
        """取得語音指示內容 - 簡潔版本"""
        config = self.load_config()
        project_name = config.get('project_name', self.project_dir.name)
        
        return f"""

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

[語音通知已啟用 - {project_name}]
"""
    
    def inject_instructions(self):
        """注入語音指示到 CLAUDE.md"""
        voice_section = self.get_voice_instructions()
        
        # 讀取現有內容
        content = ""
        if self.claude_md.exists():
            with open(self.claude_md, 'r', encoding='utf-8') as f:
                content = f.read()
        
        # 移除舊的語音章節
        content = re.sub(
            r'\n## 語音通知設置.*?\[語音通知已啟用 - [^\]]+\]',
            '',
            content,
            flags=re.DOTALL
        )
        
        # 加入新章節
        updated_content = content.rstrip() + voice_section
        
        # 寫入更新的內容
        with open(self.claude_md, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print("✅ CLAUDE.md 語音指示已更新")
        return True
    
    def remove_instructions(self):
        """移除語音指示"""
        if not self.claude_md.exists():
            return
        
        with open(self.claude_md, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 移除語音章節
        updated_content = re.sub(
            r'\n## 語音通知設置.*?\[語音通知已啟用 - [^\]]+\]',
            '',
            content,
            flags=re.DOTALL
        )
        
        if updated_content != content:
            with open(self.claude_md, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print("✅ 已從 CLAUDE.md 移除語音指示")

if __name__ == "__main__":
    manager = ClaudeMdManager()
    
    if len(sys.argv) > 1 and sys.argv[1] == "remove":
        manager.remove_instructions()
    else:
        manager.inject_instructions()
EOF

chmod +x "$VOICE_DIR/update_claude_md.py"

# 4. 創建記憶守護腳本（在專用資料夾內）
echo "🛡️ 創建集中式記憶守護腳本..."
cat > "$VOICE_DIR/memory_keeper.sh" << 'EOF'
#!/bin/bash
# 語音記憶守護者 - 專案專用版本

VOICE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$VOICE_DIR")"

echo "🛡️ 語音記憶守護者啟動"
echo "📁 專案: $(basename "$PROJECT_DIR")"
echo "📁 語音資料夾: $VOICE_DIR"

# 創建狀態檔案
STATE_FILE="$VOICE_DIR/keeper_state.json"

while true; do
    # 檢查 CLAUDE.md 是否包含語音指示
    if ! grep -q "語音通知設置" "$PROJECT_DIR/CLAUDE.md" 2>/dev/null; then
        echo "🔄 [$(date '+%H:%M:%S')] 重新注入語音指示..."
        cd "$PROJECT_DIR"
        python3 "$VOICE_DIR/update_claude_md.py"
        
        # 發送語音提醒
        python3 "$VOICE_DIR/claude_notify.py" \
            "語音通知記憶已恢復，請記得在需要用戶互動時使用" "gentle" 2>/dev/null
    else
        echo "✓ [$(date '+%H:%M:%S')] 語音指示正常"
    fi
    
    # 記錄狀態
    echo "{\"last_check\": \"$(date)\", \"status\": \"running\"}" > "$STATE_FILE"
    
    # 每30分鐘檢查一次
    sleep 1800
done
EOF

chmod +x "$VOICE_DIR/memory_keeper.sh"

# 5. 創建管理腳本
echo "🛠️ 創建語音管理腳本..."
cat > "$VOICE_DIR/manage.sh" << 'EOF'
#!/bin/bash
# 語音通知管理腳本

VOICE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$VOICE_DIR")"

case "$1" in
    test)
        echo "🎤 測試語音功能..."
        cd "$PROJECT_DIR"
        python3 "$VOICE_DIR/test_voice_simple.py"
        ;;
    update)
        echo "📝 更新 CLAUDE.md 語音指示..."
        cd "$PROJECT_DIR"
        python3 "$VOICE_DIR/update_claude_md.py"
        ;;
    notify)
        echo "📢 發送測試語音通知..."
        cd "$PROJECT_DIR"
        python3 "$VOICE_DIR/claude_notify.py" "${2:-測試語音通知}" "${3:-excited}"
        ;;
    keeper-start)
        echo "🛡️ 啟動記憶守護（背景執行）..."
        cd "$PROJECT_DIR"
        nohup "$VOICE_DIR/memory_keeper.sh" > "$VOICE_DIR/keeper.log" 2>&1 &
        echo $! > "$VOICE_DIR/keeper.pid"
        echo "✅ 記憶守護已在背景啟動"
        ;;
    keeper-stop)
        echo "🛑 停止記憶守護..."
        if [ -f "$VOICE_DIR/keeper.pid" ]; then
            kill $(cat "$VOICE_DIR/keeper.pid") 2>/dev/null
            rm -f "$VOICE_DIR/keeper.pid"
            echo "✅ 記憶守護已停止"
        else
            echo "⚠️ 記憶守護未在運行"
        fi
        ;;
    keeper-status)
        echo "📊 記憶守護狀態..."
        if [ -f "$VOICE_DIR/keeper.pid" ] && kill -0 $(cat "$VOICE_DIR/keeper.pid") 2>/dev/null; then
            echo "✅ 記憶守護正在運行"
            echo "📋 PID: $(cat "$VOICE_DIR/keeper.pid")"
        else
            echo "❌ 記憶守護未運行"
        fi
        ;;
    remove)
        echo "🗑️ 移除語音功能..."
        cd "$PROJECT_DIR"
        # 停止守護
        "$0" keeper-stop
        # 從 CLAUDE.md 移除指示
        python3 "$VOICE_DIR/update_claude_md.py" remove
        # 刪除整個資料夾
        cd ..
        rm -rf "$VOICE_DIR"
        echo "✅ 語音功能已完全移除"
        ;;
    *)
        echo "🛠️ 語音通知管理工具"
        echo ""
        echo "用法: $0 {command}"
        echo ""
        echo "指令："
        echo "  test          測試語音功能"
        echo "  update        更新 CLAUDE.md 指示"
        echo "  notify [msg]  發送測試通知"
        echo "  keeper-start  啟動記憶守護"
        echo "  keeper-stop   停止記憶守護"
        echo "  keeper-status 檢查守護狀態"
        echo "  remove        完全移除語音功能"
        echo ""
        echo "範例："
        echo "  $0 test"
        echo "  $0 notify '需要確認' 'urgent'"
        echo "  $0 keeper-start"
        ;;
esac
EOF

chmod +x "$VOICE_DIR/manage.sh"

# 6. 創建快速使用腳本（放在專案根目錄）
echo "🚀 創建根目錄快速使用腳本..."
cat > "$PROJECT_DIR/claude-voice" << 'EOF'
#!/bin/bash
# 快速語音通知腳本
exec .claude-voice/claude_notify.py "$@"
EOF

chmod +x "$PROJECT_DIR/claude-voice"

# 7. 更新 CLAUDE.md
echo "📝 更新 CLAUDE.md..."
cd "$PROJECT_DIR"
python3 "$VOICE_DIR/update_claude_md.py"

# 8. 測試語音功能
echo "🎤 測試語音功能..."
python3 "$VOICE_DIR/claude_notify.py" "語音通知系統設置完成！專案：$PROJECT_NAME" "excited"

# 9. AI 自動回應確認
echo "🤖 發送 AI 確認語音通知..."
python3 "$VOICE_DIR/claude_notify.py" "好的，我知道了！會在需要時使用語音通知" "gentle"

echo ""
echo "🎉 有組織的語音通知系統設置完成！"
echo ""
echo "📁 所有語音相關檔案都在: .claude-voice/"
echo "📋 檔案結構:"
echo "  $PROJECT_DIR/"
echo "  ├── claude-voice                    # 快速語音通知腳本"
echo "  ├── CLAUDE.md                       # 包含語音指示"
echo "  └── .claude-voice/                  # 語音通知資料夾"
echo "      ├── claude_notify.py            # 語音通知工具"
echo "      ├── voice_assistant.py          # 語音助理核心"
echo "      ├── test_voice_simple.py        # 語音測試工具"
echo "      ├── config.json                 # 語音設定"
echo "      ├── update_claude_md.py         # CLAUDE.md 管理器"
echo "      ├── memory_keeper.sh            # 記憶守護腳本"
echo "      └── manage.sh                   # 管理工具"
echo ""
echo "🎯 使用方法："
echo "# 快速語音通知"
echo "./claude-voice '需要確認' 'urgent'"
echo ""
echo "# 管理語音功能"
echo ".claude-voice/manage.sh test"
echo ".claude-voice/manage.sh keeper-start"
echo ""
echo "# 完全移除語音功能"
echo ".claude-voice/manage.sh remove"
echo ""
echo "🗑️ 要移除語音功能時，只需刪除 .claude-voice/ 資料夾即可！"