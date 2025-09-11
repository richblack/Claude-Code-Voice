#!/usr/bin/env python3
"""
語音通知定時提醒系統
定期提醒 Claude Code 使用語音通知功能，防止遺忘
"""
import sys
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
import threading

class VoiceReminder:
    """語音通知提醒器"""
    
    def __init__(self, project_path=None):
        self.project_path = Path(project_path) if project_path else Path.cwd()
        self.reminder_file = self.project_path / '.claude_voice_reminder.json'
        self.config = self.load_reminder_config()
        
    def load_reminder_config(self):
        """載入提醒設定"""
        default_config = {
            'enabled': True,
            'interval_minutes': 30,  # 30分鐘提醒一次
            'last_reminder': None,
            'reminder_count': 0,
            'auto_remind_on_start': True,
            'messages': [
                "記得使用語音通知功能！如需用戶確認時請用: python3 ~/.claude-code-tools/claude_notify.py \"訊息\" \"urgent\"",
                "提醒：遇到錯誤或任務完成時，請主動使用語音通知提醒用戶",
                "語音通知小提醒：python3 ~/.claude-code-tools/claude_notify.py \"任務完成\" \"excited\"",
                "記得在需要用戶互動時使用語音通知，提升用戶體驗",
                "定時提醒：使用 claude_notify.py 讓用戶知道任務狀態"
            ]
        }
        
        if self.reminder_file.exists():
            try:
                with open(self.reminder_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception as e:
                print(f"載入提醒設定失敗: {e}")
        
        return default_config
    
    def save_reminder_config(self):
        """儲存提醒設定"""
        try:
            with open(self.reminder_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"儲存提醒設定失敗: {e}")
    
    def should_remind(self):
        """檢查是否應該提醒"""
        if not self.config['enabled']:
            return False
        
        last_reminder = self.config.get('last_reminder')
        if not last_reminder:
            return True
        
        last_time = datetime.fromisoformat(last_reminder)
        interval = timedelta(minutes=self.config['interval_minutes'])
        
        return datetime.now() - last_time > interval
    
    def send_reminder(self, message=None):
        """發送提醒訊息"""
        if message is None:
            # 輪流使用不同的提醒訊息
            messages = self.config['messages']
            index = self.config['reminder_count'] % len(messages)
            message = messages[index]
        
        # 更新提醒記錄
        self.config['last_reminder'] = datetime.now().isoformat()
        self.config['reminder_count'] += 1
        self.save_reminder_config()
        
        # 發送語音提醒（如果語音助理可用）
        try:
            import subprocess
            cmd = ['python3', '~/.claude-code-tools/claude_notify.py', 
                   f"定時提醒 #{self.config['reminder_count']}: {message}", 'gentle']
            subprocess.run(cmd, check=False, capture_output=True)
        except Exception:
            pass
        
        # 輸出到終端
        print(f"\n🔔 語音通知提醒 #{self.config['reminder_count']}")
        print(f"📝 {message}")
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        return True
    
    def start_background_reminder(self):
        """啟動背景提醒"""
        def reminder_loop():
            while self.config['enabled']:
                time.sleep(60)  # 每分鐘檢查一次
                if self.should_remind():
                    self.send_reminder()
        
        reminder_thread = threading.Thread(target=reminder_loop, daemon=True)
        reminder_thread.start()
        print(f"🔔 語音通知提醒已啟動（每 {self.config['interval_minutes']} 分鐘提醒一次）")
        return reminder_thread
    
    def check_and_remind(self):
        """檢查並提醒（單次）"""
        if self.should_remind():
            return self.send_reminder()
        else:
            next_reminder = datetime.fromisoformat(self.config['last_reminder']) + \
                          timedelta(minutes=self.config['interval_minutes'])
            minutes_left = (next_reminder - datetime.now()).total_seconds() / 60
            
            if minutes_left > 0:
                print(f"⏳ 下次提醒時間: {int(minutes_left)} 分鐘後")
            else:
                print(f"🔔 即將提醒...")
        
        return False
    
    def configure(self, **kwargs):
        """設定提醒參數"""
        for key, value in kwargs.items():
            if key in self.config:
                self.config[key] = value
                print(f"✅ 設定 {key} = {value}")
        
        self.save_reminder_config()
    
    def status(self):
        """顯示提醒狀態"""
        print(f"📊 語音通知提醒狀態")
        print(f"  專案路徑: {self.project_path}")
        print(f"  提醒啟用: {'✅ 是' if self.config['enabled'] else '❌ 否'}")
        print(f"  提醒間隔: {self.config['interval_minutes']} 分鐘")
        print(f"  提醒次數: {self.config['reminder_count']}")
        
        if self.config.get('last_reminder'):
            last_time = datetime.fromisoformat(self.config['last_reminder'])
            print(f"  最後提醒: {last_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            next_time = last_time + timedelta(minutes=self.config['interval_minutes'])
            print(f"  下次提醒: {next_time.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(f"  最後提醒: 無")

def main():
    """主函數"""
    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 voice_reminder.py check        # 檢查並提醒")
        print("  python3 voice_reminder.py start        # 啟動背景提醒")
        print("  python3 voice_reminder.py status       # 查看狀態")
        print("  python3 voice_reminder.py remind       # 立即提醒")
        print("  python3 voice_reminder.py disable      # 停用提醒")
        print("  python3 voice_reminder.py enable       # 啟用提醒")
        print("  python3 voice_reminder.py interval 45  # 設定間隔為45分鐘")
        return
    
    command = sys.argv[1].lower()
    project_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    reminder = VoiceReminder(project_path)
    
    if command == 'check':
        reminder.check_and_remind()
    
    elif command == 'start':
        thread = reminder.start_background_reminder()
        try:
            # 保持程式運行
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 語音提醒已停止")
    
    elif command == 'status':
        reminder.status()
    
    elif command == 'remind':
        reminder.send_reminder()
    
    elif command == 'disable':
        reminder.configure(enabled=False)
        print("🔇 語音提醒已停用")
    
    elif command == 'enable':
        reminder.configure(enabled=True)
        print("🔔 語音提醒已啟用")
    
    elif command == 'interval':
        if len(sys.argv) > 2:
            try:
                interval = int(sys.argv[2])
                reminder.configure(interval_minutes=interval)
                print(f"⏰ 提醒間隔已設定為 {interval} 分鐘")
            except ValueError:
                print("❌ 間隔時間必須是數字")
        else:
            print("❌ 請提供間隔時間（分鐘）")
    
    else:
        print(f"❌ 未知命令: {command}")

if __name__ == "__main__":
    main()