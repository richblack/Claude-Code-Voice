#!/usr/bin/env python3
"""
註冊當前 Claude Code 實例到語音助理系統
這個腳本應該在每個 Claude Code 會話開始時執行
"""
import os
import sys
from pathlib import Path

# 確保能找到 claude_instances 模組
sys.path.insert(0, str(Path(__file__).parent))

try:
    from claude_instances import register_current_instance, ClaudeInstanceManager
    from voice_assistant import ClaudeVoiceAssistant
except ImportError as e:
    print(f"❌ 無法導入模組: {e}")
    sys.exit(1)

def main():
    """主函數"""
    try:
        # 註冊當前實例
        instance_id = register_current_instance()
        
        # 發送註冊成功通知
        assistant = ClaudeVoiceAssistant()
        project_name = Path.cwd().name
        
        print(f"✅ Claude Code 實例已註冊: {instance_id[:8]}...")
        print(f"📁 專案: {project_name}")
        print("🎤 現在可以使用語音助理功能")
        
        # 透過daemon發送語音通知
        from claude_instances import send_notification_to_daemon
        send_notification_to_daemon(
            f"新的 Claude Code 實例已註冊：{project_name}",
            emotion="gentle",
            context="registration"
        )
        
        return instance_id
        
    except Exception as e:
        print(f"❌ 註冊失敗: {e}")
        return None

def show_status():
    """顯示實例狀態"""
    try:
        manager = ClaudeInstanceManager()
        active_instances = manager.get_active_instances()
        
        print("\n🔍 當前活躍的 Claude Code 實例:")
        print("-" * 70)
        
        if active_instances:
            for i, (instance_id, info) in enumerate(active_instances.items(), 1):
                project_name = Path(info.get('project_path', '')).name or '未知專案'
                pid = info.get('pid', 'N/A')
                voice_enabled = info.get('voice_enabled', False)
                daemon_aware = info.get('daemon_aware', False)
                
                # 狀態圖示
                voice_icon = "🔊" if voice_enabled else "🔇"
                daemon_icon = "📡" if daemon_aware else "❌"
                
                print(f"{i}. {project_name}")
                print(f"   ID: {instance_id[:8]}...")
                print(f"   PID: {pid}")
                print(f"   路徑: {info.get('project_path', 'N/A')}")
                print(f"   語音通知: {voice_icon} {'已啟用' if voice_enabled else '未啟用'}")
                print(f"   Daemon 連線: {daemon_icon} {'已連接' if daemon_aware else '未連接'}")
                print()
        else:
            print("沒有找到活躍的實例")
        
        # 檢查daemon狀態
        print("\n📡 Daemon 狀態:")
        print("-" * 70)
        daemon_running = check_daemon_running()
        if daemon_running:
            print("✅ Daemon 正在運行")
            
            # 顯示daemon設定
            try:
                import json
                config_path = Path(__file__).parent / 'config.json'
                if config_path.exists():
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    mode = config.get('mode', 'unknown')
                    mode_names = {
                        "normal": "正常模式 (聲音+通知)",
                        "silent": "靜音模式 (只有通知)", 
                        "sleep": "睡眠模式 (無聲無通知)"
                    }
                    print(f"🔄 當前模式: {mode_names.get(mode, mode)}")
            except Exception as e:
                print(f"⚠️ 無法讀取daemon設定: {e}")
        else:
            print("❌ Daemon 未運行")
            print("💡 使用 'python3 terminal_daemon.py' 啟動")
            
    except Exception as e:
        print(f"❌ 顯示狀態失敗: {e}")

def check_daemon_running():
    """檢查daemon是否正在運行"""
    import subprocess
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        return 'terminal_daemon.py' in result.stdout
    except Exception:
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        show_status()
    else:
        main()