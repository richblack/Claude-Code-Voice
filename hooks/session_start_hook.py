#!/usr/bin/env python3
"""
Claude Code會話開始hook
自動註冊實例到語音助理系統
"""
import sys
import os
from pathlib import Path

# 添加語音助理路徑
sys.path.insert(0, str(Path.home() / '.claude-code-tools'))

def handle_session_start():
    """處理會話開始事件"""
    try:
        project_path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
        
        # 切換到專案目錄
        os.chdir(project_path)
        
        # 註冊實例
        from claude_instances import register_current_instance, send_notification_to_daemon
        
        instance_id = register_current_instance()
        
        if instance_id:
            project_name = Path(project_path).name
            send_notification_to_daemon(
                f"Claude Code會話已啟動：{project_name}",
                emotion="gentle", 
                context="session_start"
            )
            
    except Exception as e:
        # 靜默失敗，不影響Claude Code啟動
        pass

if __name__ == "__main__":
    handle_session_start()
