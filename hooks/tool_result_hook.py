#!/usr/bin/env python3
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
