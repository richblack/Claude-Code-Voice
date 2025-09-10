#!/usr/bin/env python3
"""
用戶問題提交hook
自動註冊和更新實例狀態
"""
import sys
import os
from pathlib import Path

# 添加語音助理路徑
sys.path.insert(0, str(Path.home() / '.claude-code-tools'))

def handle_user_submit():
    """處理用戶提交事件"""
    try:
        # 更新實例活動時間
        from claude_instances import ClaudeInstanceManager
        
        manager = ClaudeInstanceManager()
        current_dir = os.getcwd()
        
        # 找到對應的實例並更新活動時間
        for instance_id, info in manager.instances.items():
            if info.get('project_path') == current_dir:
                manager.update_instance_activity(instance_id)
                break
        else:
            # 如果沒找到，嘗試註冊新實例
            try:
                from claude_instances import register_current_instance
                register_current_instance()
            except Exception:
                pass
                
    except Exception as e:
        # 靜默失敗
        pass

if __name__ == "__main__":
    handle_user_submit()
