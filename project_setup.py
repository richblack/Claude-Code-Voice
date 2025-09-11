#!/usr/bin/env python3
"""
專案快速設定語音助理腳本
為新的 Claude Code 專案快速設置語音通知功能
"""
import os
import sys
import json
import shutil
from pathlib import Path

def setup_project_voice(project_path=None):
    """為專案設置語音助理功能"""
    
    if project_path:
        project_dir = Path(project_path).resolve()
    else:
        project_dir = Path.cwd()
    
    print(f"🚀 為專案設置語音通知功能")
    print(f"📁 專案目錄: {project_dir}")
    
    # 檢查是否已有全域語音助理
    global_tools = Path.home() / '.claude-code-tools'
    if global_tools.exists():
        print(f"✅ 發現全域語音助理，建議直接使用")
        print(f"🔊 使用方式: python3 ~/.claude-code-tools/claude_notify.py \"訊息\" \"情緒\"")
        
        # 建立專案設定檔指向全域助理
        create_project_config(project_dir, 'global')
        return
    
    # 如果沒有全域助理，建立本地副本
    print(f"⚠️  未發現全域語音助理，建立本地副本")
    
    # 複製語音助理到專案
    source_dir = Path.home() / 'Documents' / 'claude-code-voice'
    local_voice_dir = project_dir / '.claude-voice'
    
    if not source_dir.exists():
        print(f"❌ 未找到語音助理源碼於: {source_dir}")
        print(f"💡 請先下載: git clone https://github.com/youlinhsieh/claude-code-voice.git ~/Documents/claude-code-voice")
        return False
    
    # 複製必要檔案到專案
    copy_voice_files_to_project(source_dir, local_voice_dir)
    
    # 建立專案設定檔
    create_project_config(project_dir, 'local')
    
    print(f"✅ 專案語音通知設置完成！")
    print(f"🔊 使用方式: python3 .claude-voice/claude_notify.py \"訊息\" \"情緒\"")

def copy_voice_files_to_project(source_dir, local_voice_dir):
    """複製語音助理檔案到專案"""
    
    # 建立目錄
    local_voice_dir.mkdir(exist_ok=True)
    
    # 需要複製的核心檔案
    core_files = [
        'claude_notify_direct.py',
        'voice_assistant.py', 
        'config.json'
    ]
    
    print(f"📦 複製語音助理檔案...")
    
    for file_name in core_files:
        source_file = source_dir / file_name
        dest_file = local_voice_dir / file_name
        
        if source_file.exists():
            shutil.copy2(source_file, dest_file)
            print(f"  ✅ {file_name}")
        else:
            print(f"  ⚠️  跳過 {file_name} (不存在)")
    
    # 建立簡化的 claude_notify.py
    create_local_notify_script(local_voice_dir)

def create_local_notify_script(local_voice_dir):
    """建立本地語音通知腳本"""
    
    notify_script = local_voice_dir / 'claude_notify.py'
    
    with open(notify_script, 'w', encoding='utf-8') as f:
        f.write('''#!/usr/bin/env python3
"""
專案本地語音通知工具
"""
import sys
from pathlib import Path

# 添加當前目錄到路徑
sys.path.insert(0, str(Path(__file__).parent))

from claude_notify_direct import main

if __name__ == "__main__":
    main()
''')
    
    os.chmod(notify_script, 0o755)
    print(f"  ✅ claude_notify.py (本地入口)")

def create_project_config(project_dir, voice_type):
    """建立專案語音設定檔"""
    
    config_file = project_dir / '.claude-voice-config.json'
    
    config = {
        'voice_enabled': True,
        'voice_type': voice_type,  # 'global' 或 'local'
        'setup_date': str(Path().cwd()),
        'description': {
            'global': '使用全域語音助理 (~/.claude-code-tools/)',
            'local': '使用專案本地語音助理 (./.claude-voice/)'
        }.get(voice_type, '未知類型')
    }
    
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print(f"📋 建立專案設定檔: {config_file}")

def detect_and_setup():
    """自動偵測並設置最佳的語音助理配置"""
    
    print(f"🔍 偵測語音助理配置...")
    
    # 檢查全域助理
    global_tools = Path.home() / '.claude-code-tools'
    if global_tools.exists():
        print(f"✅ 全域語音助理已設置")
        return 'global'
    
    # 檢查是否可以設置全域助理
    source_dir = Path.home() / 'Documents' / 'claude-code-voice'
    if source_dir.exists():
        print(f"💡 建議設置全域語音助理（一次設置，全部專案可用）")
        response = input(f"是否要設置全域語音助理? (y/N): ").lower().strip()
        
        if response in ['y', 'yes']:
            import subprocess
            result = subprocess.run([
                sys.executable, 
                str(source_dir / 'setup_global.py')
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ 全域語音助理設置成功")
                return 'global'
            else:
                print(f"❌ 全域設置失敗: {result.stderr}")
    
    # 回到專案設置
    print(f"🔄 改用專案本地設置")
    setup_project_voice()
    return 'local'

def main():
    """主函數"""
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'detect':
            detect_and_setup()
        else:
            # 指定專案路徑
            setup_project_voice(sys.argv[1])
    else:
        # 當前目錄設置
        setup_project_voice()

if __name__ == "__main__":
    main()