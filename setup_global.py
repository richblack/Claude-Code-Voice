#!/usr/bin/env python3
"""
設置全域語音助理系統
在 ~/.claude-code-tools 建立符號連結指向主要語音助理
"""
import os
import shutil
from pathlib import Path

def setup_global_voice():
    """設置全域語音助理"""
    home = Path.home()
    
    # 主要語音助理目錄
    source_dir = home / 'Documents' / 'claude-code-voice'
    
    # 全域工具目錄
    global_dir = home / '.claude-code-tools'
    
    print(f"🔧 設置全域語音助理...")
    print(f"📁 來源目錄: {source_dir}")
    print(f"🌐 全域目錄: {global_dir}")
    
    # 建立全域目錄
    if global_dir.exists():
        print(f"⚠️  全域目錄已存在，將先備份")
        backup_dir = global_dir.with_name('.claude-code-tools.backup')
        if backup_dir.exists():
            shutil.rmtree(backup_dir)
        shutil.move(str(global_dir), str(backup_dir))
        print(f"📦 舊版本已備份至: {backup_dir}")
    
    # 建立符號連結
    try:
        os.symlink(str(source_dir), str(global_dir))
        print(f"✅ 成功建立符號連結")
    except Exception as e:
        # 如果符號連結失敗，複製檔案
        print(f"⚠️  符號連結失敗 ({e})，改為複製檔案")
        shutil.copytree(str(source_dir), str(global_dir))
        print(f"✅ 成功複製檔案")
    
    # 建立全域執行檔
    create_global_executables(global_dir)
    
    print(f"")
    print(f"🎉 全域語音助理設置完成！")
    print(f"")
    print(f"現在可以在任何地方使用:")
    print(f"  python3 ~/.claude-code-tools/claude_notify.py \"訊息\" \"情緒\"")
    print(f"  python3 ~/.claude-code-tools/voice_assistant.py")

def create_global_executables(global_dir):
    """建立全域可執行檔"""
    
    # 建立簡化的 claude_notify.py
    notify_script = global_dir / 'claude_notify.py'
    with open(notify_script, 'w', encoding='utf-8') as f:
        f.write('''#!/usr/bin/env python3
"""
全域 Claude Code 語音通知工具
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
    print(f"✅ 建立全域通知腳本: {notify_script}")

if __name__ == "__main__":
    setup_global_voice()