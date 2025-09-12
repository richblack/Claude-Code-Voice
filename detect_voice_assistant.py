#!/usr/bin/env python3
"""
專案自動偵測語音助理工具
讓專案可以自動找到並使用全域或本地語音助理
"""
import sys
from pathlib import Path

def detect_voice_assistant():
    """
    自動偵測可用的語音助理
    返回最佳的語音助理路徑和使用方式
    """
    
    # 優先順序：
    # 1. 直接路徑 (~/Documents/claude-code-voice/)
    # 2. 本地語音助理 (./.claude-voice/)
    # 3. 直接路徑 (~/Documents/claude-code-voice/)
    
    home = Path.home()
    current_dir = Path.cwd()
    
    # 1. 檢查全域語音助理
    global_tools = home / '.claude-code-tools'
    if (global_tools / 'claude_notify.py').exists():
        return {
            'type': 'global',
            'path': global_tools / 'claude_notify.py',
            'description': '使用全域語音助理',
            'usage': f'python3 ~/Documents/claude-code-voice/claude_notify.py "訊息" "情緒"'
        }
    
    # 2. 檢查本地語音助理  
    local_voice = current_dir / '.claude-voice'
    if (local_voice / 'claude_notify.py').exists():
        return {
            'type': 'local', 
            'path': local_voice / 'claude_notify.py',
            'description': '使用專案本地語音助理',
            'usage': f'python3 .claude-voice/claude_notify.py "訊息" "情緒"'
        }
    
    # 3. 檢查直接路徑
    direct_path = home / 'Documents' / 'claude-code-voice'
    if (direct_path / 'claude_notify_direct.py').exists():
        return {
            'type': 'direct',
            'path': direct_path / 'claude_notify_direct.py', 
            'description': '使用直接路徑語音助理',
            'usage': f'python3 ~/Documents/claude-code-voice/claude_notify_direct.py "訊息" "情緒"'
        }
    
    # 沒有找到任何語音助理
    return {
        'type': 'none',
        'path': None,
        'description': '未找到語音助理',
        'setup_hint': '請執行: python3 ~/Documents/claude-code-voice/setup_global.py'
    }

def get_voice_notify_command(message, emotion="gentle"):
    """
    取得語音通知的完整命令
    """
    assistant_info = detect_voice_assistant()
    
    if assistant_info['type'] == 'none':
        return None, assistant_info
    
    if assistant_info['type'] == 'global':
        cmd = f'python3 ~/Documents/claude-code-voice/claude_notify.py "{message}" "{emotion}"'
    elif assistant_info['type'] == 'local':
        cmd = f'python3 .claude-voice/claude_notify.py "{message}" "{emotion}"'
    elif assistant_info['type'] == 'direct':
        cmd = f'python3 ~/Documents/claude-code-voice/claude_notify_direct.py "{message}" "{emotion}"'
    else:
        cmd = None
    
    return cmd, assistant_info

def main():
    """主函數 - 顯示偵測結果"""
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        # 測試模式
        message = sys.argv[2] if len(sys.argv) > 2 else "測試語音助理偵測"
        emotion = sys.argv[3] if len(sys.argv) > 3 else "gentle"
        
        cmd, info = get_voice_notify_command(message, emotion)
        if cmd:
            print(f"🔊 執行語音通知: {cmd}")
            import subprocess
            subprocess.run(cmd, shell=True)
        else:
            print(f"❌ {info['description']}")
            if 'setup_hint' in info:
                print(f"💡 建議: {info['setup_hint']}")
    else:
        # 偵測模式
        info = detect_voice_assistant()
        print(f"🔍 語音助理偵測結果:")
        print(f"📍 類型: {info['type']}")
        print(f"📝 描述: {info['description']}")
        if info['path']:
            print(f"📁 路徑: {info['path']}")
            print(f"🚀 使用方式: {info['usage']}")
        elif 'setup_hint' in info:
            print(f"💡 設置建議: {info['setup_hint']}")

if __name__ == "__main__":
    main()