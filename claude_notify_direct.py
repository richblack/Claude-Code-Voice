#!/usr/bin/env python3
"""
Claude Code 直接語音通知工具 (不依賴 daemon)
用於當 daemon 無法使用時的純手動語音通知
"""
import sys
import os
from pathlib import Path

# 添加工具路徑
sys.path.insert(0, str(Path.home() / '.claude-code-tools'))

def main():
    """主函數"""
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    message = sys.argv[1]
    emotion = sys.argv[2] if len(sys.argv) > 2 else "gentle"
    
    print(f"🔊 發送語音通知: {message}")
    print(f"😊 情緒類型: {emotion}")
    
    # 檢查是否啟用語音通知
    if not is_voice_enabled():
        print("🔇 語音通知已停用，跳過通知")
        return
    
    # 直接使用語音助理，不通過 daemon
    try:
        from voice_assistant import ClaudeVoiceAssistant
        assistant = ClaudeVoiceAssistant()
        
        # 確保語音模式正確設置
        original_mode = assistant.config.get('mode', 'normal')
        if original_mode in ['normal', 'silent']:
            # 臨時設置為 full 模式以確保語音播放
            assistant.config['mode'] = 'full'
        
        print(f"🔊 使用語音模式: {assistant.config['mode']}")
        
        # 發送語音通知
        assistant.notify(message, emotion=emotion)
        print(f"✅ 語音通知成功發送")
        
        # 恢復原始模式
        if original_mode in ['normal', 'silent']:
            assistant.config['mode'] = original_mode
        
        # 同時發送系統通知
        send_system_notification(message)
        
    except Exception as e:
        print(f"❌ 語音通知發送失敗: {e}")
        # 至少嘗試發送系統通知
        send_system_notification(message)

def send_system_notification(message):
    """發送 macOS 系統通知"""
    try:
        import subprocess
        subprocess.run([
            'terminal-notifier',
            '-title', '小西 Claude Code',
            '-message', message,
            '-sound', 'default'
        ], check=False)
        print("✅ 系統通知已發送")
    except Exception:
        # 如果 terminal-notifier 不可用，使用 osascript
        try:
            import subprocess
            applescript = f'''
            display notification "{message}" with title "小西 Claude Code"
            '''
            subprocess.run(['osascript', '-e', applescript], check=False)
            print("✅ 系統通知已發送 (AppleScript)")
        except Exception as e:
            print(f"⚠️ 系統通知發送失敗: {e}")

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
                enabled = config.get('voice_enabled', True)
                print(f"📋 從設定檔讀取: 語音通知{'已啟用' if enabled else '已停用'}")
                return enabled
        
        # 如果沒有設定檔案，預設啟用
        print("📋 沒有找到設定檔，預設啟用語音通知")
        return True
        
    except Exception as e:
        print(f"⚠️ 檢查語音設定失敗: {e}")
        print("📋 預設啟用語音通知")
        return True

def print_usage():
    """顯示使用方法"""
    print("""
🔊 Claude Code 直接語音通知工具

用法:
  python3 claude_notify_direct.py "訊息內容" [情緒類型]

範例:
  # 基本通知
  python3 claude_notify_direct.py "需要您的協助"
  
  # 緊急通知
  python3 claude_notify_direct.py "遇到錯誤，請檢查" "urgent"
  
  # 完成通知
  python3 claude_notify_direct.py "任務已完成" "excited"

情緒類型:
  - gentle   (預設) - 嗨，打擾一下，
  - urgent   - 快來看看！
  - excited  - 太棒了！
  - worried  - 糟糕，
  - thinking - 嗯...讓我想想，

這個工具直接使用語音助理，不依賴 daemon 系統。
    """)

if __name__ == "__main__":
    main()