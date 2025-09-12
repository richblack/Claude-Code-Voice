#!/usr/bin/env python3
"""
新專案語音通知初始化腳本
在新專案中執行此腳本，會自動找到 claude-code-voice 並複製相關內容到專案內
"""
import os
import sys
import shutil
import json
from pathlib import Path

def find_claude_voice_source():
    """
    自動尋找 claude-code-voice 的位置
    按優先順序搜尋可能的位置
    """
    possible_paths = [
        # 1. 標準位置
        Path.home() / 'Documents' / 'claude-code-voice',
        
        # 2. 用戶目錄下
        Path.home() / 'claude-code-voice',
        
        # 3. 當前用戶的 Documents 下所有可能名稱
        Path.home() / 'Documents' / 'claude-code-voice-main',
        Path.home() / 'Documents' / 'claude-voice',
        
        # 4. 全域位置
        Path('/opt/claude-code-voice'),
        Path('/usr/local/claude-code-voice'),
    ]
    
    print("🔍 正在尋找 claude-code-voice 安裝位置...")
    
    for path in possible_paths:
        print(f"  檢查: {path}")
        if path.exists() and (path / 'voice_assistant.py').exists():
            print(f"✅ 找到 claude-code-voice: {path}")
            return path
    
    # 5. 搜尋整個 Documents 目錄
    docs_dir = Path.home() / 'Documents'
    if docs_dir.exists():
        print(f"  搜尋 {docs_dir} 目錄...")
        for item in docs_dir.iterdir():
            if item.is_dir() and 'claude' in item.name.lower() and 'voice' in item.name.lower():
                if (item / 'voice_assistant.py').exists():
                    print(f"✅ 找到 claude-code-voice: {item}")
                    return item
    
    return None

def create_project_voice_structure(source_path, project_path):
    """
    在專案中建立語音通知結構
    """
    project_path = Path(project_path)
    voice_dir = project_path / '.claude-voice'
    
    print(f"📁 在專案中建立語音通知結構: {voice_dir}")
    
    # 建立目錄
    voice_dir.mkdir(exist_ok=True)
    
    # 需要複製的核心檔案
    core_files = [
        'voice_assistant.py',
        'config.json', 
        'claude_notify_direct.py'
    ]
    
    print(f"📦 複製核心檔案...")
    copied_files = []
    
    for file_name in core_files:
        source_file = source_path / file_name
        dest_file = voice_dir / file_name
        
        if source_file.exists():
            shutil.copy2(source_file, dest_file)
            copied_files.append(file_name)
            print(f"  ✅ {file_name}")
        else:
            print(f"  ⚠️  跳過 {file_name} (來源不存在)")
    
    # 建立專案專用的 claude_notify.py
    create_project_notify_script(voice_dir)
    
    # 建立 CLAUDE.md
    create_claude_md(project_path, voice_dir)
    
    # 建立設定檔
    create_voice_config(voice_dir)
    
    return copied_files

def create_project_notify_script(voice_dir):
    """建立專案專用的語音通知腳本"""
    
    notify_script = voice_dir / 'claude_notify.py'
    
    script_content = '''#!/usr/bin/env python3
"""
專案語音通知工具
自動偵測並使用最佳的語音助理
"""
import sys
import subprocess
from pathlib import Path

def main():
    """主函數 - 智慧選擇語音助理"""
    if len(sys.argv) < 2:
        print("用法: python3 .claude-voice/claude_notify.py \"訊息\" [情緒]")
        return
    
    message = sys.argv[1]
    emotion = sys.argv[2] if len(sys.argv) > 2 else "gentle"
    
    # 優先順序：
    # 1. 全域語音助理
    # 2. 本地語音助理 
    # 3. 直接路徑
    
    commands_to_try = [
        # 全域語音助理
        ['python3', '~/Documents/claude-code-voice/claude_notify.py', message, emotion],
        
        # 本地語音助理
        ['python3', str(Path(__file__).parent / 'claude_notify_direct.py'), message, emotion],
        
        # 直接路徑
        ['python3', str(Path.home() / 'Documents' / 'claude-code-voice' / 'claude_notify_direct.py'), message, emotion]
    ]
    
    for cmd in commands_to_try:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"🔊 語音通知已發送: {message}")
                if result.stdout:
                    print(result.stdout)
                return True
        except Exception as e:
            continue
    
    # 所有方法都失敗
    print(f"❌ 語音通知發送失敗")
    print(f"💡 請檢查語音助理是否已安裝: ~/Documents/claude-code-voice/")
    return False

if __name__ == "__main__":
    main()
'''
    
    with open(notify_script, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    os.chmod(notify_script, 0o755)
    print(f"  ✅ claude_notify.py (智慧路由)")

def create_claude_md(project_path, voice_dir):
    """建立或更新 CLAUDE.md"""
    
    claude_md = project_path / 'CLAUDE.md'
    
    voice_instructions = '''
# 🔊 語音通知系統

## ⚠️ 重要：請主動使用語音通知！

**在需要用戶注意時，請立即使用語音通知功能。**

### 🚨 必須使用語音通知的情況

#### 1. 需要用戶確認時（最重要！）
```bash
python3 .claude-voice/claude_notify.py "需要您確認是否執行" "urgent"
```

#### 2. 遇到錯誤時
```bash
python3 .claude-voice/claude_notify.py "遇到錯誤需要檢查" "urgent"
```

#### 3. 任務完成時
```bash
python3 .claude-voice/claude_notify.py "任務完成，請檢視結果" "excited"
```

#### 4. 需要等待時
```bash
python3 .claude-voice/claude_notify.py "任務執行中，請稍候" "thinking"
```

## 🎭 情緒類型
- `urgent` - 緊急事件
- `gentle` - 一般通知  
- `excited` - 完成通知
- `worried` - 錯誤警告
- `thinking` - 等待提示

## 💡 使用原則
- **主動性**: 不要等用戶問，需要時立即通知
- **及時性**: 關鍵時刻提醒，提升用戶體驗
- **適當性**: 根據情況選擇合適的情緒類型

---
*語音通知已啟用 - 記得主動使用！*
'''
    
    if claude_md.exists():
        # 檢查是否已包含語音通知說明
        try:
            with open(claude_md, 'r', encoding='utf-8') as f:
                content = f.read()
                if '語音通知' in content and 'claude_notify.py' in content:
                    print(f"  ✅ CLAUDE.md 已包含語音通知說明")
                    return
        except Exception:
            pass
        
        # 追加語音通知說明
        try:
            with open(claude_md, 'a', encoding='utf-8') as f:
                f.write(f"\n\n{'='*60}\n")
                f.write(voice_instructions)
            print(f"  ✅ CLAUDE.md 已更新（追加語音通知說明）")
        except Exception as e:
            print(f"  ❌ 更新 CLAUDE.md 失敗: {e}")
    else:
        # 建立新的 CLAUDE.md
        try:
            with open(claude_md, 'w', encoding='utf-8') as f:
                f.write(voice_instructions)
            print(f"  ✅ CLAUDE.md 已建立")
        except Exception as e:
            print(f"  ❌ 建立 CLAUDE.md 失敗: {e}")

def create_voice_config(voice_dir):
    """建立語音設定檔"""
    
    config_file = voice_dir / '.claude-voice-config.json'
    
    config = {
        'voice_enabled': True,
        'setup_date': str(Path.cwd()),
        'voice_type': 'project_local',
        'description': '專案內建語音通知系統',
        'auto_fallback': True,
        'fallback_order': [
            'global (~/Documents/claude-code-voice/)',
            'local (./.claude-voice/)', 
            'direct (~/Documents/claude-code-voice/)'
        ]
    }
    
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        print(f"  ✅ 語音設定檔已建立")
    except Exception as e:
        print(f"  ❌ 建立設定檔失敗: {e}")

def show_usage_instructions(project_path):
    """顯示使用說明"""
    
    print(f"\n🎉 語音通知系統設置完成！")
    print(f"📁 專案路徑: {project_path}")
    print(f"")
    print(f"🚀 現在可以使用:")
    print(f"  python3 .claude-voice/claude_notify.py \"需要您的協助\" \"urgent\"")
    print(f"")
    print(f"📋 重要提醒:")
    print(f"  • Claude Code 會在需要用戶確認時主動語音通知")
    print(f"  • 遇到錯誤或任務完成時也會語音提醒")
    print(f"  • CLAUDE.md 中有完整的使用說明")
    print(f"")
    print(f"🔊 測試語音通知:")
    print(f"  python3 .claude-voice/claude_notify.py \"專案設置完成\" \"excited\"")

def main():
    """主函數"""
    
    print("🚀 Claude Code 語音通知初始化")
    print("="*50)
    
    current_project = Path.cwd()
    print(f"📁 當前專案: {current_project.name}")
    print(f"📍 專案路徑: {current_project}")
    
    # 檢查是否已經設置過
    voice_dir = current_project / '.claude-voice'
    if voice_dir.exists() and (voice_dir / 'claude_notify.py').exists():
        print(f"⚠️  語音通知系統已存在")
        response = input("是否要重新設置? (y/N): ").lower().strip()
        if response not in ['y', 'yes']:
            print("❌ 取消設置")
            return
    
    # 尋找 claude-code-voice 源碼
    source_path = find_claude_voice_source()
    
    if not source_path:
        print("❌ 找不到 claude-code-voice 安裝位置")
        print("💡 請先安裝:")
        print("   git clone https://github.com/youlinhsieh/claude-code-voice.git ~/Documents/claude-code-voice")
        return
    
    # 建立專案語音通知結構
    try:
        copied_files = create_project_voice_structure(source_path, current_project)
        
        if copied_files:
            show_usage_instructions(current_project)
        else:
            print("❌ 沒有成功複製任何檔案")
            
    except Exception as e:
        print(f"❌ 設置失敗: {e}")

if __name__ == "__main__":
    main()