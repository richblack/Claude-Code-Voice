#!/usr/bin/env python3
"""
快速設置新 Claude Code 實例的語音通知功能
"""
import sys
import os
import subprocess
import shutil
from pathlib import Path

# 添加工具路徑
sys.path.insert(0, str(Path.home() / '.claude-code-tools'))

def setup_instance_for_voice(project_path=None):
    """為實例設置語音通知功能"""
    
    if project_path:
        project_dir = Path(project_path)
        if not project_dir.exists():
            print(f"❌ 專案目錄不存在: {project_path}")
            return False
        os.chdir(project_path)
    else:
        project_dir = Path.cwd()
    
    project_name = project_dir.name
    print(f"🚀 正在為專案 '{project_name}' 設置語音通知功能...")
    
    # 步驟 1: 註冊實例
    print("📋 步驟 1: 註冊實例到語音助理系統")
    try:
        result = subprocess.run([
            'python3', str(Path.home() / '.claude-code-tools' / 'register_claude.py')
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 實例註冊成功")
            print(result.stdout)
        else:
            print("❌ 實例註冊失敗")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ 註冊實例失敗: {e}")
        return False
    
    # 步驟 2: 複製必要工具
    print("🔧 步驟 2: 複製語音通知工具")
    tools_dir = Path.home() / '.claude-code-tools'
    
    tools_to_copy = [
        'claude_notify.py',
        'voice_assistant.py'
    ]
    
    for tool in tools_to_copy:
        source = tools_dir / tool
        target = project_dir / tool
        
        if source.exists() and not target.exists():
            try:
                shutil.copy2(source, target)
                print(f"📋 已複製 {tool}")
            except Exception as e:
                print(f"⚠️ 複製 {tool} 失敗: {e}")
    
    # 步驟 3: 啟用語音通知
    print("🔊 步驟 3: 啟用語音通知")
    try:
        # 獲取剛註冊的實例 ID
        from claude_instances import ClaudeInstanceManager
        manager = ClaudeInstanceManager()
        
        # 找到對應的實例
        target_instance = None
        for instance_id, info in manager.instances.items():
            if info.get('project_path') == str(project_dir):
                target_instance = instance_id
                break
        
        if target_instance:
            # 使用命令列工具啟用語音
            result = subprocess.run([
                'python3', 
                str(tools_dir / 'manage_instances.py'),
                'enable-voice',
                target_instance[:12]
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ 語音通知已啟用")
                print(result.stdout)
            else:
                print("⚠️ 啟用語音通知時出現問題")
                print(result.stderr)
        else:
            print("⚠️ 找不到對應的實例，請手動啟用語音通知")
    
    except Exception as e:
        print(f"❌ 啟用語音通知失敗: {e}")
    
    # 步驟 4: 設置 hooks (可選)
    print("🔗 步驟 4: 設置 Claude Code hooks (可選)")
    try:
        result = subprocess.run([
            'python3', 
            str(tools_dir / 'setup_hooks.py'),
            '--project', str(project_dir)
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ hooks 設置成功")
        else:
            print("⚠️ hooks 設置失敗，但不影響語音功能")
    except Exception:
        print("⚠️ 跳過 hooks 設置")
    
    # 步驟 5: 測試語音通知
    print("🎤 步驟 5: 測試語音通知")
    try:
        test_script = project_dir / 'claude_notify.py'
        if test_script.exists():
            result = subprocess.run([
                'python3', str(test_script),
                f"語音通知系統已為專案 {project_name} 設置完成！",
                "excited"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ 測試通知已發送")
            else:
                print("⚠️ 測試通知發送失敗")
                print(result.stderr)
    except Exception as e:
        print(f"⚠️ 測試通知失敗: {e}")
    
    print(f"\n🎉 專案 '{project_name}' 語音通知功能設置完成！")
    print("\n📋 現在您可以使用以下命令發送語音通知：")
    print(f"   python3 claude_notify.py \"你的訊息\" \"情緒類型\"")
    print("\n💡 或者使用完整路徑：")
    print(f"   python3 ~/.claude-code-tools/claude_notify.py \"你的訊息\" \"情緒類型\"")
    print("\n🔍 查看所有實例狀態：")
    print(f"   python3 ~/.claude-code-tools/manage_instances.py list")
    
    return True

def main():
    """主函數"""
    import argparse
    
    parser = argparse.ArgumentParser(description='快速設置 Claude Code 實例的語音通知功能')
    parser.add_argument('--path', '-p', help='專案路徑 (預設使用當前目錄)')
    
    args = parser.parse_args()
    
    project_path = None
    if args.path:
        if not os.path.exists(args.path):
            print(f"❌ 路徑不存在: {args.path}")
            sys.exit(1)
        project_path = os.path.abspath(args.path)
    
    success = setup_instance_for_voice(project_path)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()