#!/usr/bin/env python3
"""
命令列實例管理工具 - 替代托盤圖標的功能
"""
import sys
import os
import json
from pathlib import Path

# 添加工具路徑
sys.path.insert(0, str(Path.home() / '.claude-code-tools'))

from claude_instances import ClaudeInstanceManager

def show_instances():
    """顯示所有實例"""
    manager = ClaudeInstanceManager()
    active_instances = manager.get_active_instances()
    
    if not active_instances:
        print("❌ 沒有找到活躍的實例")
        return
    
    print("📋 活躍的 Claude Code 實例:")
    print("=" * 60)
    
    for i, (instance_id, info) in enumerate(active_instances.items(), 1):
        project_path = info.get('project_path', '')
        project_name = Path(project_path).name if project_path else '未知專案'
        voice_enabled = info.get('voice_enabled', False)
        pid = info.get('pid', 'N/A')
        
        voice_icon = "🔊 已啟用" if voice_enabled else "🔇 已停用"
        
        print(f"{i}. {project_name}")
        print(f"   ID: {instance_id[:12]}...")
        print(f"   PID: {pid}")
        print(f"   路徑: {project_path}")
        print(f"   語音通知: {voice_icon}")
        print()

def toggle_voice(instance_id, enable):
    """切換實例語音設定"""
    manager = ClaudeInstanceManager()
    
    if instance_id not in manager.instances:
        print(f"❌ 找不到實例: {instance_id}")
        return False
    
    # 更新設定
    manager.instances[instance_id]['voice_enabled'] = enable
    manager.save_instances()
    
    project_path = manager.instances[instance_id].get('project_path', '')
    project_name = Path(project_path).name if project_path else '未知專案'
    
    # 通知實例
    success = notify_instance_voice_setting(project_path, enable)
    
    action = "啟用" if enable else "停用"
    status = "成功" if success else "失敗"
    print(f"✅ 實例 {project_name} 的語音通知{action}{status}")
    
    return success

def notify_instance_voice_setting(project_path, enable):
    """通知實例語音設定變更"""
    try:
        import time
        
        project_dir = Path(project_path)
        if not project_dir.exists():
            print(f"❌ 專案目錄不存在: {project_path}")
            return False
        
        # 創建語音設定檔案
        voice_config_file = project_dir / '.claude-voice-config.json'
        
        config_data = {
            'voice_enabled': enable,
            'daemon_endpoint': str(Path.home() / '.claude-code-tools'),
            'last_updated': time.time(),
            'instructions': {
                'enabled_message': '✅ 語音通知已啟用 - 當需要用戶協助時，請使用語音通知',
                'usage_examples': [
                    'python3 ~/.claude-code-tools/claude_notify.py "需要您的協助" "gentle"',
                    'python3 ~/.claude-code-tools/claude_notify.py "遇到錯誤，需要檢查" "urgent"',
                    'python3 ~/.claude-code-tools/claude_notify.py "任務完成，請檢視結果" "excited"'
                ],
                'disabled_message': '🔇 語音通知已停用'
            }
        }
        
        # 寫入設定檔案
        with open(voice_config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
        
        # 更新 CLAUDE.md
        update_claude_md(project_dir, enable)
        
        return True
        
    except Exception as e:
        print(f"❌ 通知實例語音設定失敗: {e}")
        return False

def update_claude_md(project_dir, enable):
    """更新專案的 CLAUDE.md 檔案"""
    try:
        claude_md_file = project_dir / 'CLAUDE.md'
        
        # 語音指引內容
        voice_section = """

# 🔊 語音通知系統

此專案已連接小西語音助理系統。當你需要通知使用者時，請使用：

## 基本用法
```bash
python3 ~/.claude-code-tools/claude_notify.py "訊息內容" "情緒類型"
```

## 常用範例
```bash
# 需要用戶協助
python3 ~/.claude-code-tools/claude_notify.py "需要您的協助解決問題" "gentle"

# 遇到錯誤
python3 ~/.claude-code-tools/claude_notify.py "程式執行出錯，請檢查" "urgent"  

# 任務完成
python3 ~/.claude-code-tools/claude_notify.py "任務已完成，請檢視結果" "excited"

# 等待輸入
python3 ~/.claude-code-tools/claude_notify.py "請提供更多資訊以繼續" "thinking"
```

## 情緒類型
- `urgent` - 緊急事件
- `gentle` - 一般通知
- `excited` - 正面消息
- `worried` - 問題警告
- `thinking` - 需要思考

**重要**: 請在需要用戶注意或協助時主動使用語音通知，這樣可以及時提醒用戶處理。
""" if enable else """

# 🔇 語音通知已停用

此專案的語音通知功能已停用，請勿使用語音通知命令。
"""

        current_content = ""
        if claude_md_file.exists():
            with open(claude_md_file, 'r', encoding='utf-8') as f:
                current_content = f.read()
        
        # 移除舊的語音章節
        import re
        current_content = re.sub(
            r'\n# 🔊 語音通知系統.*?(?=\n# [^🔊]|\Z)', 
            '', 
            current_content, 
            flags=re.DOTALL
        )
        current_content = re.sub(
            r'\n# 🔇 語音通知已停用.*?(?=\n# [^🔇]|\Z)', 
            '', 
            current_content, 
            flags=re.DOTALL
        )
        
        # 添加新的語音章節
        updated_content = current_content.rstrip() + voice_section
        
        # 寫入更新的內容
        with open(claude_md_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
            
        print(f"✅ 已更新 CLAUDE.md 語音指引")
        
    except Exception as e:
        print(f"❌ 更新 CLAUDE.md 失敗: {e}")

def set_daemon_mode(mode):
    """設定 daemon 模式"""
    config_file = Path.home() / '.claude-code-tools' / 'config.json'
    
    try:
        config = {"mode": "normal", "assistant_name": "小西"}
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
        
        if mode in ['normal', 'silent', 'sleep']:
            config['mode'] = mode
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            mode_names = {
                'normal': '正常模式 (語音+通知)',
                'silent': '靜音模式 (僅通知)',
                'sleep': '睡眠模式 (無通知)'
            }
            print(f"✅ 模式已設定為: {mode_names[mode]}")
            return True
        else:
            print("❌ 無效模式，請使用: normal, silent, sleep")
            return False
            
    except Exception as e:
        print(f"❌ 設定模式失敗: {e}")
        return False

def refresh_instances():
    """重新整理實例列表"""
    try:
        import subprocess
        
        print("🔄 正在重新整理實例列表...")
        result = subprocess.run([
            'python3', 
            str(Path.home() / '.claude-code-tools' / 'manual_refresh.py')
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ 重新整理失敗: {e}")
        return False

def main():
    """主函數"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Claude Code 實例管理工具')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # list 命令
    subparsers.add_parser('list', help='顯示所有實例')
    
    # enable-voice 命令
    enable_parser = subparsers.add_parser('enable-voice', help='啟用實例語音通知')
    enable_parser.add_argument('instance_id', help='實例 ID (前12碼即可)')
    
    # disable-voice 命令  
    disable_parser = subparsers.add_parser('disable-voice', help='停用實例語音通知')
    disable_parser.add_argument('instance_id', help='實例 ID (前12碼即可)')
    
    # mode 命令
    mode_parser = subparsers.add_parser('mode', help='設定 daemon 模式')
    mode_parser.add_argument('mode', choices=['normal', 'silent', 'sleep'], help='模式')
    
    # refresh 命令
    subparsers.add_parser('refresh', help='重新整理實例列表')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'list':
        show_instances()
    elif args.command == 'enable-voice':
        # 找到匹配的完整實例 ID
        manager = ClaudeInstanceManager()
        matching_ids = [iid for iid in manager.instances.keys() if iid.startswith(args.instance_id)]
        
        if len(matching_ids) == 1:
            toggle_voice(matching_ids[0], True)
        elif len(matching_ids) > 1:
            print(f"❌ 找到多個匹配的實例: {matching_ids}")
        else:
            print(f"❌ 找不到匹配的實例: {args.instance_id}")
    elif args.command == 'disable-voice':
        # 找到匹配的完整實例 ID
        manager = ClaudeInstanceManager()
        matching_ids = [iid for iid in manager.instances.keys() if iid.startswith(args.instance_id)]
        
        if len(matching_ids) == 1:
            toggle_voice(matching_ids[0], False)
        elif len(matching_ids) > 1:
            print(f"❌ 找到多個匹配的實例: {matching_ids}")
        else:
            print(f"❌ 找不到匹配的實例: {args.instance_id}")
    elif args.command == 'mode':
        set_daemon_mode(args.mode)
    elif args.command == 'refresh':
        refresh_instances()

if __name__ == "__main__":
    main()