#!/usr/bin/env python3
"""
設置Claude Code hooks以與語音助理daemon整合
"""
import json
import os
from pathlib import Path

def setup_claude_code_hooks(project_dir=None):
    """為Claude Code設置語音助理hooks"""
    
    if project_dir:
        project_path = Path(project_dir)
    else:
        project_path = Path.cwd()
    
    print(f"🔗 為專案設置語音助理hooks: {project_path.name}")
    
    # Claude Code hooks設定檔路徑
    hooks_config_file = project_path / '.claude' / 'hooks.json'
    
    # 確保.claude目錄存在
    claude_dir = project_path / '.claude'
    claude_dir.mkdir(exist_ok=True)
    
    # 現有的hooks設定
    existing_hooks = {}
    if hooks_config_file.exists():
        try:
            with open(hooks_config_file, 'r', encoding='utf-8') as f:
                existing_hooks = json.load(f)
        except Exception as e:
            print(f"⚠️ 讀取現有hooks設定失敗: {e}")
    
    # 語音助理相關的hooks
    voice_hooks = {
        # 工具調用後的hook - 檢查是否需要語音通知
        "tool-result": {
            "command": f"python3 ~/Documents/claude-code-voice/hooks/tool_result_hook.py",
            "description": "檢查工具執行結果是否需要語音通知"
        },
        
        # 用戶提交問題後的hook - 自動註冊實例
        "user-prompt-submit": {
            "command": f"python3 ~/Documents/claude-code-voice/hooks/user_submit_hook.py",
            "description": "用戶提交新問題時自動註冊實例"
        },
        
        # Claude Code啟動後的hook
        "session-start": {
            "command": f"python3 ~/Documents/claude-code-voice/hooks/session_start_hook.py '{project_path}'",
            "description": "Claude Code會話開始時自動註冊到語音助理"
        }
    }
    
    # 合併hooks設定
    for hook_name, hook_config in voice_hooks.items():
        existing_hooks[hook_name] = hook_config
    
    # 寫入hooks設定
    try:
        with open(hooks_config_file, 'w', encoding='utf-8') as f:
            json.dump(existing_hooks, f, indent=2, ensure_ascii=False)
        
        print(f"✅ hooks設定已更新: {hooks_config_file}")
        
        # 創建hooks腳本
        create_hook_scripts()
        
        return True
        
    except Exception as e:
        print(f"❌ 設定hooks失敗: {e}")
        return False

def create_hook_scripts():
    """創建hooks執行腳本"""
    
    hooks_dir = Path.home() / '.claude-code-tools' / 'hooks'
    hooks_dir.mkdir(exist_ok=True)
    
    # 1. 工具結果檢查hook
    tool_result_hook = hooks_dir / 'tool_result_hook.py'
    tool_result_content = '''#!/usr/bin/env python3
"""
工具執行結果檢查hook
檢查是否有錯誤或需要用戶注意的結果
"""
import sys
import os
import json
from pathlib import Path

# 添加語音助理路徑
sys.path.insert(0, str(Path.home() / '.claude-code-tools'))

def check_tool_result():
    """檢查工具執行結果"""
    try:
        # 從環境變數或標準輸入讀取工具結果
        tool_data = os.getenv('CLAUDE_TOOL_RESULT', '')
        
        if not tool_data:
            return
        
        # 檢查是否有錯誤關鍵字
        error_keywords = ['error', 'failed', 'exception', 'timeout', '❌', '失敗']
        help_keywords = ['需要', 'help', 'assist', '協助', '檢查']
        
        should_notify = False
        emotion = "gentle"
        
        tool_lower = tool_data.lower()
        
        for keyword in error_keywords:
            if keyword in tool_lower:
                should_notify = True
                emotion = "urgent"
                break
        
        if not should_notify:
            for keyword in help_keywords:
                if keyword in tool_lower:
                    should_notify = True
                    emotion = "gentle"
                    break
        
        if should_notify:
            from claude_instances import send_notification_to_daemon
            
            # 截取前100字符作為通知訊息
            message = tool_data[:100] + "..." if len(tool_data) > 100 else tool_data
            
            send_notification_to_daemon(
                f"工具執行需要注意: {message}",
                emotion=emotion,
                context="tool_result"
            )
            
    except Exception as e:
        # 靜默失敗，不影響正常流程
        pass

if __name__ == "__main__":
    check_tool_result()
'''
    
    with open(tool_result_hook, 'w', encoding='utf-8') as f:
        f.write(tool_result_content)
    os.chmod(tool_result_hook, 0o755)
    
    # 2. 用戶提交hook
    user_submit_hook = hooks_dir / 'user_submit_hook.py'
    user_submit_content = '''#!/usr/bin/env python3
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
'''
    
    with open(user_submit_hook, 'w', encoding='utf-8') as f:
        f.write(user_submit_content)
    os.chmod(user_submit_hook, 0o755)
    
    # 3. 會話開始hook
    session_start_hook = hooks_dir / 'session_start_hook.py'
    session_start_content = '''#!/usr/bin/env python3
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
'''
    
    with open(session_start_hook, 'w', encoding='utf-8') as f:
        f.write(session_start_content)
    os.chmod(session_start_hook, 0o755)
    
    print("✅ 已創建所有hook腳本")

def main():
    """主函數"""
    import argparse
    
    parser = argparse.ArgumentParser(description='設置Claude Code語音助理hooks')
    parser.add_argument('--project', '-p', help='專案目錄路徑')
    
    args = parser.parse_args()
    
    project_dir = args.project if args.project else None
    
    success = setup_claude_code_hooks(project_dir)
    
    if success:
        print("\n🎉 語音助理hooks設置完成！")
        print("\n📋 已設置的hooks:")
        print("  • session-start: 會話開始時自動註冊")
        print("  • user-prompt-submit: 用戶提交問題時更新活動狀態") 
        print("  • tool-result: 工具執行結果智能通知")
        print("\n💡 現在Claude Code會自動與語音助理daemon協作！")
    else:
        print("❌ hooks設置失敗")

if __name__ == "__main__":
    main()