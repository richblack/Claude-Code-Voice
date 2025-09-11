#!/usr/bin/env python3
"""
自動設置專案 CLAUDE.md 的語音通知說明
讓每個專案都知道如何使用語音通知功能
"""
import os
import shutil
from pathlib import Path
import argparse

def setup_claude_md(project_path=None, force=False):
    """為專案設置 CLAUDE.md 語音通知說明"""
    
    if project_path:
        project_dir = Path(project_path).resolve()
    else:
        project_dir = Path.cwd()
    
    if not project_dir.exists() or not project_dir.is_dir():
        print(f"❌ 專案目錄不存在: {project_dir}")
        return False
    
    claude_md = project_dir / 'CLAUDE.md'
    template_path = Path(__file__).parent / 'claude_md_template.md'
    
    print(f"🚀 設置專案語音通知說明")
    print(f"📁 專案目錄: {project_dir}")
    print(f"📄 CLAUDE.md: {claude_md}")
    
    # 檢查是否已存在 CLAUDE.md
    if claude_md.exists() and not force:
        print(f"⚠️  CLAUDE.md 已存在")
        
        # 檢查是否已包含語音通知說明
        try:
            with open(claude_md, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'claude_notify.py' in content or '語音通知' in content:
                    print(f"✅ CLAUDE.md 已包含語音通知說明")
                    return True
                else:
                    print(f"📝 CLAUDE.md 缺少語音通知說明，需要更新")
                    return append_voice_instructions(claude_md, template_path)
        except Exception as e:
            print(f"❌ 讀取 CLAUDE.md 失敗: {e}")
            return False
    
    # 複製模板
    try:
        if not template_path.exists():
            print(f"❌ 模板檔案不存在: {template_path}")
            return False
        
        if claude_md.exists():
            # 備份原有檔案
            backup_path = claude_md.with_suffix('.md.backup')
            shutil.copy2(claude_md, backup_path)
            print(f"📦 原有 CLAUDE.md 已備份至: {backup_path}")
        
        # 複製模板
        shutil.copy2(template_path, claude_md)
        print(f"✅ CLAUDE.md 語音通知說明設置完成")
        
        # 顯示使用提示
        show_usage_instructions()
        
        return True
        
    except Exception as e:
        print(f"❌ 設置失敗: {e}")
        return False

def append_voice_instructions(claude_md, template_path):
    """在現有 CLAUDE.md 中追加語音通知說明"""
    
    try:
        # 讀取模板內容
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # 讀取現有內容
        with open(claude_md, 'r', encoding='utf-8') as f:
            existing_content = f.read()
        
        # 在現有內容後追加語音通知說明
        separator = "\n\n" + "="*80 + "\n"
        separator += "# 🔊 語音通知系統設定\n"
        separator += "="*80 + "\n\n"
        
        combined_content = existing_content + separator + template_content
        
        # 寫入檔案
        with open(claude_md, 'w', encoding='utf-8') as f:
            f.write(combined_content)
        
        print(f"✅ 語音通知說明已追加至現有 CLAUDE.md")
        return True
        
    except Exception as e:
        print(f"❌ 追加語音通知說明失敗: {e}")
        return False

def show_usage_instructions():
    """顯示使用說明"""
    print(f"")
    print(f"🎉 設置完成！Claude Code 現在知道如何使用語音通知了")
    print(f"")
    print(f"📋 關鍵提醒:")
    print(f"  • Claude Code 會在需要用戶確認時主動語音通知")
    print(f"  • 遇到錯誤或任務完成時也會語音提醒")
    print(f"  • 這些說明會持續提醒 Claude Code 使用語音功能")
    print(f"")
    print(f"🔊 測試語音通知:")
    print(f"  python3 ~/.claude-code-tools/claude_notify.py \"專案設置完成\" \"excited\"")

def setup_all_projects(base_path=None):
    """批量設置多個專案的 CLAUDE.md"""
    
    if base_path:
        base_dir = Path(base_path)
    else:
        base_dir = Path.home() / 'Documents'
    
    if not base_dir.exists():
        print(f"❌ 基礎目錄不存在: {base_dir}")
        return
    
    print(f"🔍 搜尋 {base_dir} 下的專案...")
    
    # 尋找包含 .git 的目錄（可能是專案）
    projects_found = []
    for item in base_dir.iterdir():
        if item.is_dir() and (item / '.git').exists():
            projects_found.append(item)
    
    if not projects_found:
        print(f"❌ 在 {base_dir} 下沒有找到 Git 專案")
        return
    
    print(f"📁 找到 {len(projects_found)} 個專案:")
    for i, project in enumerate(projects_found, 1):
        print(f"  {i}. {project.name}")
    
    # 詢問是否批量設置
    response = input(f"\n是否為所有專案設置語音通知說明? (y/N): ").lower().strip()
    
    if response in ['y', 'yes']:
        success_count = 0
        for project in projects_found:
            print(f"\n📂 處理專案: {project.name}")
            if setup_claude_md(project):
                success_count += 1
        
        print(f"\n🎉 批量設置完成！成功設置 {success_count}/{len(projects_found)} 個專案")
    else:
        print(f"❌ 取消批量設置")

def main():
    """主函數"""
    parser = argparse.ArgumentParser(description='為專案設置 Claude Code 語音通知說明')
    
    parser.add_argument('project_path', nargs='?', 
                       help='專案路徑（預設為當前目錄）')
    parser.add_argument('--force', '-f', action='store_true',
                       help='強制覆蓋現有 CLAUDE.md')
    parser.add_argument('--batch', '-b', 
                       help='批量設置指定目錄下的所有專案')
    
    args = parser.parse_args()
    
    if args.batch:
        setup_all_projects(args.batch)
    else:
        setup_claude_md(args.project_path, args.force)

if __name__ == "__main__":
    main()