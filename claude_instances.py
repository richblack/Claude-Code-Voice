#!/usr/bin/env python3
"""
Claude Code 實例管理和協調
"""
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

class ClaudeInstanceManager:
    """管理多個 Claude Code 實例"""
    
    def __init__(self):
        self.base_dir = Path.home() / '.claude-code-tools'
        self.instances_file = self.base_dir / 'claude_instances.json'
        self.instances = self.load_instances()
    
    def load_instances(self):
        """載入實例清單"""
        if self.instances_file.exists():
            try:
                with open(self.instances_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def save_instances(self):
        """保存實例清單"""
        try:
            with open(self.instances_file, 'w', encoding='utf-8') as f:
                json.dump(self.instances, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"保存實例清單失敗: {e}")
    
    def register_instance(self, instance_id, info):
        """註冊新的 Claude Code 實例"""
        self.instances[instance_id] = {
            'pid': info.get('pid'),
            'project_path': info.get('project_path'),
            'terminal': info.get('terminal'),
            'last_active': datetime.now().isoformat(),
            'status': 'active',
            'voice_enabled': info.get('voice_enabled', True),  # 預設啟用語音
            'daemon_aware': info.get('daemon_aware', True)    # 知道daemon存在
        }
        self.save_instances()
        print(f"✅ 註冊實例: {instance_id}")
    
    def unregister_instance(self, instance_id):
        """取消註冊實例"""
        if instance_id in self.instances:
            del self.instances[instance_id]
            self.save_instances()
            print(f"❌ 取消註冊實例: {instance_id}")
    
    def update_instance_activity(self, instance_id):
        """更新實例活動時間"""
        if instance_id in self.instances:
            self.instances[instance_id]['last_active'] = datetime.now().isoformat()
            self.save_instances()
    
    def get_active_instances(self):
        """取得活躍的實例清單"""
        active_instances = {}
        cutoff_time = datetime.now() - timedelta(minutes=30)
        
        for instance_id, info in self.instances.items():
            try:
                last_active = datetime.fromisoformat(info['last_active'])
                if last_active > cutoff_time:
                    # 檢查程序是否還在運行
                    if self.is_process_running(info.get('pid')):
                        active_instances[instance_id] = info
                    else:
                        # 程序已結束，標記為非活躍
                        info['status'] = 'inactive'
            except:
                pass
        
        return active_instances
    
    def is_process_running(self, pid):
        """檢查程序是否還在運行"""
        if not pid:
            return False
        
        try:
            result = subprocess.run(['ps', '-p', str(pid)], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def get_most_recent_instance(self):
        """取得最近活躍的實例"""
        active_instances = self.get_active_instances()
        
        if not active_instances:
            return None
        
        # 依照最後活動時間排序
        sorted_instances = sorted(
            active_instances.items(),
            key=lambda x: x[1]['last_active'],
            reverse=True
        )
        
        return sorted_instances[0] if sorted_instances else None
    
    def choose_instance_interactive(self):
        """互動式選擇實例"""
        active_instances = self.get_active_instances()
        
        if not active_instances:
            return None
        
        if len(active_instances) == 1:
            return list(active_instances.items())[0]
        
        # 多個實例，讓用戶選擇
        print("\n📋 發現多個 Claude Code 實例:")
        print("-" * 50)
        
        instance_list = list(active_instances.items())
        for i, (instance_id, info) in enumerate(instance_list, 1):
            project_name = Path(info.get('project_path', '')).name or '未知專案'
            print(f"{i}. {project_name} ({instance_id[:8]}...)")
        
        try:
            choice = input(f"\n請選擇要對話的實例 (1-{len(instance_list)}): ")
            index = int(choice) - 1
            
            if 0 <= index < len(instance_list):
                return instance_list[index]
            else:
                print("無效選擇，使用最近活躍的實例")
                return self.get_most_recent_instance()
                
        except (ValueError, KeyboardInterrupt):
            print("使用最近活躍的實例")
            return self.get_most_recent_instance()

def register_current_instance():
    """註冊當前 Claude Code 實例"""
    import os
    import socket
    import subprocess
    
    manager = ClaudeInstanceManager()
    
    # 尋找 Claude Code 程序
    claude_pid = find_claude_process()
    if not claude_pid:
        print("❌ 無法找到 Claude Code 程序")
        return None
    
    # 生成唯一 ID
    hostname = socket.gethostname()
    instance_id = f"{hostname}_{claude_pid}_{int(time.time())}"
    
    # 取得專案路徑
    project_path = os.getcwd()
    
    # 註冊實例
    manager.register_instance(instance_id, {
        'pid': claude_pid,  # 使用找到的 Claude 程序 PID
        'project_path': project_path,
        'terminal': os.getenv('TERM_SESSION_ID', 'unknown'),
        'voice_enabled': True,   # 此實例知道可以使用語音
        'daemon_aware': True     # 此實例知道daemon存在
    })
    
    return instance_id

def find_claude_process():
    """尋找 Claude Code 程序"""
    import subprocess
    try:
        # 查找包含 'claude' 的程序，排除當前腳本
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')
        
        for line in lines:
            if 'claude' in line.lower() and 'python' not in line and 'register_claude' not in line:
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        pid = int(parts[1])
                        return pid
                    except ValueError:
                        continue
        return None
    except Exception as e:
        print(f"尋找程序錯誤: {e}")
        return None

def send_notification_to_daemon(message, emotion="gentle", context="general"):
    """向daemon發送通知請求"""
    import os
    import subprocess
    import json
    from pathlib import Path
    
    try:
        # 創建通知請求檔案
        base_dir = Path.home() / '.claude-code-tools'
        request_file = base_dir / 'notification_request.json'
        
        request_data = {
            'message': message,
            'emotion': emotion,
            'context': context,
            'timestamp': time.time(),
            'source_pid': os.getpid()
        }
        
        # 寫入請求檔案
        with open(request_file, 'w', encoding='utf-8') as f:
            json.dump(request_data, f, ensure_ascii=False)
        
        # 通知daemon有新的通知請求（透過檔案變更）
        # daemon會監控這個檔案
        print(f"📤 通知請求已發送給daemon: {message}")
        
    except Exception as e:
        print(f"❌ 發送通知請求失敗: {e}")
        # 備用方案：直接使用本地語音助理
        try:
            from voice_assistant import ClaudeVoiceAssistant
            assistant = ClaudeVoiceAssistant()
            assistant.notify(message, emotion=emotion)
        except Exception as e2:
            print(f"❌ 備用通知也失敗: {e2}")

def send_notification_to_instance(instance_id, message, emotion="gentle"):
    """向特定實例發送通知（舊版相容性）"""
    manager = ClaudeInstanceManager()
    
    # 更新實例活動時間
    manager.update_instance_activity(instance_id)
    
    # 透過daemon發送通知
    send_notification_to_daemon(message, emotion, f"instance_{instance_id}")

if __name__ == "__main__":
    # 測試功能
    manager = ClaudeInstanceManager()
    
    print("🔍 活躍的 Claude Code 實例:")
    active = manager.get_active_instances()
    
    if active:
        for instance_id, info in active.items():
            project = Path(info['project_path']).name
            print(f"  • {project} ({instance_id[:8]}...)")
    else:
        print("  沒有找到活躍實例")
    
    print(f"\n📊 總共管理 {len(manager.instances)} 個實例")