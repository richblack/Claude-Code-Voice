#!/usr/bin/env python3
"""
Claude Code 語音通知工具
讓 Claude Code 實例可以輕鬆發送語音通知給用戶
"""
import sys
import os
from pathlib import Path

# 添加工具路徑 - 使用當前專案目錄
sys.path.insert(0, str(Path(__file__).parent))

def main():
    """主函數"""
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    message = sys.argv[1]
    emotion = sys.argv[2] if len(sys.argv) > 2 else "gentle"
    
    # 檢查是否啟用語音通知
    if not is_voice_enabled():
        print("🔇 語音通知已停用，跳過通知")
        return
    
    # 發送語音通知
    try:
        from claude_instances import send_notification_to_daemon
        send_notification_to_daemon(message, emotion, "claude_code")
        print(f"✅ 語音通知已發送: {message}")
    except Exception as e:
        print(f"❌ 語音通知發送失敗: {e}")
        # 備用：直接使用語音助理
        try:
            from voice_assistant import ClaudeVoiceAssistant
            assistant = ClaudeVoiceAssistant()
            assistant.notify(message, emotion=emotion)
            print(f"✅ 使用備用方式發送語音通知")
        except Exception as e2:
            print(f"❌ 備用方式也失敗: {e2}")

def is_voice_enabled():
    """檢查當前專案是否啟用語音通知"""
    try:
        import json
        project_dir = Path.cwd()
        
        # 檢查專案中的語音設定檔案
        voice_config_file = project_dir / '.claude-voice-config.json'
        if voice_config_file.exists():
            with open(voice_config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get('voice_enabled', True)
        
        # 如果沒有設定檔案，預設啟用
        return True
        
    except Exception as e:
        print(f"⚠️ 檢查語音設定失敗: {e}")
        return True  # 預設啟用

def print_usage():
    """顯示使用方法"""
    print("""
🔊 Claude Code 語音通知工具

用法:
  python3 ~/Documents/claude-code-voice/claude_notify.py "訊息內容" [情緒類型]

範例:
  # 基本通知
  python3 ~/Documents/claude-code-voice/claude_notify.py "需要您的協助"
  
  # 緊急通知
  python3 ~/Documents/claude-code-voice/claude_notify.py "遇到錯誤，請檢查" "urgent"
  
  # 完成通知
  python3 ~/Documents/claude-code-voice/claude_notify.py "任務已完成" "excited"

情緒類型:
  - gentle   (預設) - 一般通知
  - urgent   - 緊急事件
  - excited  - 正面消息  
  - worried  - 問題警告
  - thinking - 需要思考

注意: 如果專案停用了語音通知，此命令將不會發送通知。
    """)

if __name__ == "__main__":
    main()