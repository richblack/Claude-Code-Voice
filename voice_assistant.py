#!/usr/bin/env python3
"""
Claude Code 語音助理
可作為獨立腳本使用，也可以被導入到其他專案中
"""

import os
import sys
import json
import subprocess
import platform
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, List, Any


class ClaudeVoiceAssistant:
    """Claude Code 語音助理主類別"""
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        初始化語音助理
        
        Args:
            config_path: 設定檔路徑，預設為專案目錄下的 config.json
        """
        self.base_dir = Path(__file__).parent
        self.config_path = config_path or self.base_dir / 'config.json'
        self.config = self.load_config()
        
        # 延遲載入音訊偵測器（避免循環依賴）
        self.audio_detector = None
        
    def load_config(self) -> Dict[str, Any]:
        """載入設定檔"""
        default_config = {
            'assistant_name': '小西',  # 助理的名字
            'mode': 'full',  # 'full', 'silent', 'off'
            'voice_rate': 180,
            'voice_language': 'zh-TW',
            'emotional_prefix': True,
            'auto_detect_audio': True,
            'prefixes': {
                'urgent': '快來看看！',
                'gentle': '嗨，打擾一下，',
                'excited': '太棒了！',
                'worried': '糟糕，',
                'thinking': '嗯...讓我想想，'
            },
            'hotkey_mode': True,  # 使用按鍵啟動模式
            'hotkey': 'F5',  # 預設熱鍵
            'contextual_messages': {
                # 通用訊息
                'blocked': '{name}被阻塞了，需要您的協助',
                'need_help': '{name}需要您的協助',
                'task_completed': '{name}已完成任務',
                'error': '{name}遇到錯誤，需要您檢查',
                
                # 特定情境訊息
                'git_conflict': '發現 Git 衝突，需要您決定如何處理',
                'test_failed': '測試失敗了，需要您檢查錯誤訊息',
                'build_error': '建置過程出錯，可能需要調整設定',
                'dependency_issue': '套件相依性問題，需要您確認版本',
                'permission_denied': '權限不足，需要您授權',
                'file_not_found': '找不到必要的檔案，需要您提供路徑',
                'need_user_input': '需要您提供更多資訊才能繼續',
                'review_required': '程式碼變更完成，請您檢視',
                'deployment_ready': '部署準備就緒，需要您確認',
                'long_running': '任務執行時間較長，請耐心等待'
            }
        }
        
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    # 深度合併設定
                    for key, value in user_config.items():
                        if isinstance(value, dict) and key in default_config:
                            default_config[key].update(value)
                        else:
                            default_config[key] = value
        except Exception as e:
            print(f'載入設定檔失敗: {e}')
        
        # 儲存預設設定（如果檔案不存在）
        if not self.config_path.exists():
            self.save_config(default_config)
        
        return default_config
    
    def save_config(self, config: Optional[Dict] = None):
        """儲存設定檔"""
        config = config or self.config
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f'儲存設定檔失敗: {e}')
    
    def notify(self, message: str = None, context: str = None, 
               emotion: str = None, details: str = None):
        """
        發送通知
        
        Args:
            message: 自訂訊息
            context: 情境類型（對應 contextual_messages 的 key）
            emotion: 情緒類型（對應 prefixes 的 key）
            details: 額外詳情
        """
        if self.config['mode'] == 'off':
            return
        
        # 自動偵測耳機並調整模式
        effective_mode = self.config['mode']
        if self.config['mode'] == 'silent' and self.config.get('auto_detect_audio', True):
            try:
                if self.audio_detector is None:
                    from audio_detector import AudioDeviceDetector
                    # 傳遞統一設定檔給音訊偵測器
                    self.audio_detector = AudioDeviceDetector(self.config_path)
                
                audio_check = self.audio_detector.should_enable_voice()
                if audio_check['enable']:
                    effective_mode = 'full'
                    print(f"🎧 {audio_check['reason']}，自動啟用語音")
            except ImportError:
                # 如果音訊偵測模組不可用，繼續使用原模式
                pass
        
        # 處理訊息
        if not message:
            if context:
                message = self.config['contextual_messages'].get(
                    context, 
                    self.config['contextual_messages']['need_help']
                )
            else:
                message = self.config['contextual_messages']['need_help']
        
        # 替換名字佔位符
        assistant_name = self.config.get('assistant_name', 'Claude Code')
        message = message.format(name=assistant_name)
        
        # 加入情緒化前綴
        if self.config['emotional_prefix'] and emotion:
            prefix = self.config['prefixes'].get(emotion, '')
            if prefix:
                message = f"{prefix}{message}"
        
        # 顯示訊息
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        assistant_name = self.config.get('assistant_name', 'Claude Code')
        print('\n' + '=' * 50)
        print('🔔 Claude Voice Assistant')
        print(f'時間: {timestamp}')
        print(f'訊息: {message}')
        if details:
            print(f'詳情: {details}')
        print('=' * 50 + '\n')
        
        # 系統通知（macOS 通知中心）
        if platform.system() == 'Darwin':
            self._send_system_notification(message, assistant_name, interactive=False)
        
        # 語音通知
        if effective_mode == 'full':
            self.speak(message)
    
    def speak(self, text: str, rate: Optional[int] = None):
        """
        播放語音
        
        Args:
            text: 要說的文字
            rate: 語速（預設使用設定檔的值）
        """
        rate = rate or self.config['voice_rate']
        system = platform.system()
        
        try:
            if system == 'Darwin':  # macOS
                voice = self._get_voice_for_language()
                if voice:
                    cmd = ['say', '-v', voice, '-r', str(rate), text]
                else:
                    cmd = ['say', '-r', str(rate), text]
                subprocess.run(cmd, check=True)
                
            elif system == 'Windows':
                # Windows 使用 PowerShell
                escaped_text = text.replace('"', '`"')
                ps_script = f'''
                Add-Type -AssemblyName System.Speech
                $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer
                $speak.Rate = {rate // 20 - 10}  # 調整範圍到 -10 到 10
                $speak.Speak("{escaped_text}")
                '''
                subprocess.run(['powershell', '-Command', ps_script], check=True)
                
            elif system == 'Linux':
                # Linux 使用 espeak
                try:
                    subprocess.run(['espeak', text, '-s', str(rate)], check=True)
                except FileNotFoundError:
                    print('Linux 系統需要安裝 espeak: sudo apt-get install espeak')
                    
        except Exception as e:
            print(f'語音播放失敗: {e}')
    
    def _get_voice_for_language(self) -> Optional[str]:
        """根據語言設定取得對應的語音"""
        voice_map = {
            'zh-TW': 'Mei-Jia',      # 台灣中文
            'zh-CN': 'Ting-Ting',    # 簡體中文
            'en-US': 'Samantha',     # 美式英文
            'ja-JP': 'Kyoko'         # 日文
        }
        return voice_map.get(self.config['voice_language'])
    
    def set_mode(self, mode: str):
        """設定通知模式"""
        if mode in ['full', 'silent', 'off']:
            self.config['mode'] = mode
            self.save_config()
            print(f'✅ 模式已切換為: {mode}')
        else:
            print('❌ 無效的模式。請使用: full, silent, 或 off')
    
    def quick_notify(self, context: str, emotion: str = None, details: str = None):
        """快速發送情境化通知"""
        self.notify(context=context, emotion=emotion, details=details)
    
    def test_voice(self):
        """測試語音功能"""
        print('🎤 測試語音功能...')
        assistant_name = self.config.get('assistant_name', 'Claude Code')
        self.speak(f'測試語音，我是{assistant_name}語音助理')
    
    def update_config(self, key: str, value):
        """更新設定值"""
        self.config[key] = value
        self.save_config()
        print(f'✅ 已更新 {key} = {value}')
    
    def add_device(self, device_name: str):
        """加入音訊裝置"""
        if device_name not in self.config.get('my_devices', []):
            self.config.setdefault('my_devices', []).append(device_name)
            self.save_config()
            print(f'✅ 已加入裝置: {device_name}')
        else:
            print(f'ℹ️ 裝置已存在: {device_name}')
    
    def remove_device(self, device_name: str):
        """移除音訊裝置"""
        devices = self.config.get('my_devices', [])
        if device_name in devices:
            devices.remove(device_name)
            self.save_config()
            print(f'✅ 已移除裝置: {device_name}')
        else:
            print(f'❌ 找不到裝置: {device_name}')
    
    def say(self, message: str, emotion: str = None, voice_only: bool = False):
        """自由說話功能"""
        # 加入情緒化前綴
        if self.config['emotional_prefix'] and emotion:
            prefix = self.config['prefixes'].get(emotion, '')
            if prefix:
                message = f"{prefix}{message}"
        
        # 顯示訊息（除非是純語音模式或關閉模式）
        if not voice_only and self.config['mode'] != 'off':
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            assistant_name = self.config.get('assistant_name', 'Claude Code')
            print('\n' + '=' * 50)
            print(f'💬 {assistant_name} 說話')
            print(f'時間: {timestamp}')
            print(f'訊息: {message}')
            print('=' * 50 + '\n')
        
        # 語音播放（根據模式決定）
        if self.config['mode'] != 'off':
            # 靜音模式下檢查耳機
            if self.config['mode'] == 'silent' and self.config.get('auto_detect_audio', True):
                try:
                    if self.audio_detector is None:
                        from audio_detector import AudioDeviceDetector
                        self.audio_detector = AudioDeviceDetector(self.config_path)
                    
                    audio_check = self.audio_detector.should_enable_voice()
                    if audio_check['enable']:
                        if not voice_only:
                            print(f"🎧 {audio_check['reason']}，自動啟用語音")
                        self.speak(message)
                except ImportError:
                    pass
            elif self.config['mode'] == 'full':
                self.speak(message)
    
    def listen(self, duration: int = 5, fallback_to_text: bool = True, use_real_speech: bool = True):
        """語音輸入功能"""
        if use_real_speech:
            return self._listen_with_dictation(duration, fallback_to_text)
        else:
            return self._listen_with_dialog(fallback_to_text)
    
    def _listen_with_dictation(self, duration: int, fallback_to_text: bool):
        """使用 macOS 聽寫功能進行真正的語音識別"""
        print(f"🎤 準備開始語音識別...")
        print("💡 這需要您先啟用 macOS 聽寫功能：")
        print("   系統偏好設定 > 鍵盤 > 聽寫 > 開啟")
        print("")
        
        try:
            # 創建臨時檔案來接收聽寫結果
            import tempfile
            import time
            
            with tempfile.NamedTemporaryFile(mode='w+', suffix='.txt', delete=False) as temp_file:
                temp_path = temp_file.name
            
            # 使用 AppleScript 開啟聽寫功能
            applescript = f'''
            tell application "TextEdit"
                activate
                make new document
                tell front document
                    -- 模擬按下聽寫快捷鍵 (通常是 fn+fn 或設定的快捷鍵)
                    tell application "System Events"
                        key code 63 using {{function down}}
                        key code 63 using {{function down}}
                    end tell
                    
                    -- 等待用戶說話
                    delay {duration}
                    
                    -- 取得文字內容
                    set dictatedText to text of front document
                    
                    -- 儲存到臨時檔案
                    set textFile to open for access POSIX file "{temp_path}" with write permission
                    write dictatedText to textFile
                    close access textFile
                    
                    -- 關閉文件
                    close front document without saving
                end tell
                quit
            end tell
            '''
            
            print(f"🎤 開始聆聽 {duration} 秒...")
            print("📢 請對著麥克風說話...")
            
            result = subprocess.run([
                'osascript', '-e', applescript
            ], capture_output=True, text=True, timeout=duration + 10)
            
            # 讀取結果
            try:
                with open(temp_path, 'r', encoding='utf-8') as f:
                    recognized_text = f.read().strip()
                    
                # 清理臨時檔案
                import os
                os.unlink(temp_path)
                
                if recognized_text:
                    print(f"👂 語音識別結果: {recognized_text}")
                    return recognized_text
                else:
                    print("❌ 沒有識別到語音")
                    
            except FileNotFoundError:
                print("⚠️ 聽寫結果檔案未找到")
            except Exception as e:
                print(f"⚠️ 讀取聽寫結果失敗: {e}")
                
        except Exception as e:
            print(f"❌ 聽寫功能失敗: {e}")
            print("💡 可能原因：")
            print("   1. 聽寫功能未啟用")
            print("   2. 麥克風權限未授予")
            print("   3. 網路連接問題（聽寫需要網路）")
        
        # 回退到對話框模式
        if fallback_to_text:
            print("\n🔄 改用對話框輸入...")
            return self._listen_with_dialog(fallback_to_text)
        else:
            return None
    
    def _listen_with_dialog(self, fallback_to_text: bool):
        """使用對話框進行文字輸入"""
        try:
            applescript = '''
            try
                set recognizedText to (display dialog "請說出你想要的內容：" default answer "" with title "語音輸入")
                return text returned of recognizedText
            on error
                return ""
            end try
            '''
            
            result = subprocess.run([
                'osascript', '-e', applescript
            ], capture_output=True, text=True, timeout=30)
            
            if result.stdout.strip():
                recognized_text = result.stdout.strip()
                print(f"💬 收到輸入: {recognized_text}")
                return recognized_text
            else:
                return None
                
        except Exception as e:
            if fallback_to_text:
                print(f"⚠️ 對話框失敗: {e}")
                print("💡 改用命令列輸入")
                try:
                    user_input = input("💬 你想說: ")
                    return user_input.strip() if user_input.strip() else None
                except EOFError:
                    return None
            else:
                return None
    
    def chat(self):
        """語音對話模式"""
        assistant_name = self.config.get('assistant_name', 'Claude Code')
        self.say(f"哈囉！我是{assistant_name}，讓我們開始對話吧！說 '結束' 可以離開對話模式。", emotion='gentle')
        
        while True:
            print("\n" + "="*30 + " 對話模式 " + "="*30)
            user_input = self.listen()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['結束', '結束對話', 'quit', 'exit', '再見']:
                self.say("再見！很高興和你聊天！", emotion='gentle')
                break
                
            # 簡單的對話回應
            if '你好' in user_input or '哈囉' in user_input:
                self.say("你好！很高興見到你！", emotion='excited')
            elif '謝謝' in user_input:
                self.say("不客氣！很開心能幫到你！", emotion='gentle')
            elif '怎麼樣' in user_input or '如何' in user_input:
                self.say("我很好！感謝你的關心！", emotion='gentle')
            elif '天氣' in user_input:
                self.say("我無法查看天氣，但希望今天是美好的一天！", emotion='thinking')
            elif '你是誰' in user_input:
                self.say(f"我是{assistant_name}，你的語音助理！", emotion='excited')
            else:
                self.say(f"你說：{user_input}。這很有趣！", emotion='thinking')
    
    def _send_system_notification(self, message: str, assistant_name: str, interactive: bool = False, 
                                 enable_response: bool = False):
        """發送系統通知"""
        try:
            notification_title = f"{assistant_name}語音助理"
            
            # 方法一：嘗試使用 terminal-notifier（如果已安裝）
            try:
                cmd = [
                    'terminal-notifier',
                    '-title', notification_title,
                    '-message', message,
                    '-sound', 'default'
                ]
                
                if interactive:
                    cmd.extend([
                        '-actions', '好,取消',
                        '-dropdownLabel', '請選擇'
                    ])
                elif enable_response:
                    cmd.extend([
                        '-actions', '語音回覆,打字回覆,忽略',
                        '-dropdownLabel', '如何回應？'
                    ])
                
                result = subprocess.run(cmd, capture_output=True, check=True, text=True)
                
                if (interactive or enable_response) and result.stdout.strip():
                    response = result.stdout.strip()
                    print(f"✅ 使用 terminal-notifier 發送通知，用戶回應: {response}")
                    return response
                else:
                    print("✅ 使用 terminal-notifier 發送通知")
                    return "sent"
                    
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass  # terminal-notifier 不可用，嘗試下一個方法
            
            # 方法二：使用 osascript
            escaped_message = message.replace('"', '\\"').replace("'", "\\'")
            escaped_title = notification_title.replace('"', '\\"').replace("'", "\\'")
            
            if interactive:
                # 使用互動式對話框
                applescript = f'''
                set userResponse to display dialog "{escaped_message}" with title "{escaped_title}" buttons {{"取消", "好"}} default button "好"
                return button returned of userResponse
                '''
            elif enable_response:
                # 回應選項對話框
                applescript = f'''
                set userResponse to display dialog "{escaped_message}" with title "{escaped_title}" buttons {{"忽略", "打字回覆", "語音回覆"}} default button "語音回覆"
                return button returned of userResponse
                '''
            else:
                # 普通通知
                result = subprocess.run([
                    'osascript', '-e',
                    f'display notification "{escaped_message}" with title "{escaped_title}"'
                ], capture_output=True, check=True, text=True)
                
                print("✅ 使用 osascript 發送通知")
                if result.stderr:
                    print(f"⚠️ osascript 警告: {result.stderr}")
                return "sent"
            
            # 執行互動式對話框
            result = subprocess.run([
                'osascript', '-e', applescript
            ], capture_output=True, check=True, text=True)
            
            response = result.stdout.strip()
            print(f"✅ 使用互動式對話框，用戶回應: {response}")
            return response
            
        except subprocess.CalledProcessError as e:
            print(f"⚠️ 系統通知失敗: {e}")
            print(f"⚠️ 錯誤輸出: {e.stderr if e.stderr else '無'}")
            print(f"⚠️ 標準輸出: {e.stdout if e.stdout else '無'}")
            print("💡 提示: 可能需要在系統偏好設定中允許通知權限")
            return "failed"
        except Exception as e:
            print(f"❌ 通知系統錯誤: {e}")
            return "error"
    
    def test_notification(self):
        """測試互動式通知"""
        assistant_name = self.config.get('assistant_name', 'Claude Code')
        print("🧪 發送測試通知...")
        print("📱 請檢查 macOS 通知中心或對話框")
        
        response = self._send_system_notification(
            "這是一個測試通知！如果你看到這個訊息，請點擊「好」按鈕讓我知道通知系統正常工作。",
            assistant_name,
            interactive=True
        )
        
        if response == "好":
            self.say("太棒了！系統通知功能正常工作！", emotion='excited')
            print("🎉 通知系統測試成功！")
        elif response == "取消":
            print("📱 你點擊了取消，但至少證明通知有顯示！")
        elif response == "failed":
            print("❌ 通知發送失敗，可能需要檢查系統權限")
        else:
            print(f"🤔 收到未預期的回應: {response}")
    
    def start_hotkey_listener(self):
        """啟動按鍵監聽模式"""
        assistant_name = self.config.get('assistant_name', '小西')
        
        print(f"🎙️ {assistant_name} 語音助理已啟動")
        print(f"📱 點擊「確定」開始語音輸入")
        print(f"🎤 支援語音輸入和打字輸入")
        print(f"\n等待您的輸入...")
        
        try:
            while True:
                # 直接開始輸入流程
                result = self._handle_voice_input()
                
                if result == "quit":
                    print("\n👋 結束監聽模式")
                    break
                    
        except KeyboardInterrupt:
            print("\n👋 Ctrl+C 結束監聽")
        except Exception as e:
            print(f"❌ 按鍵監聽錯誤: {e}")
    
    def _handle_voice_input(self):
        """處理語音輸入 - 改進版包含聆寫功能"""
        try:
            # 使用 macOS 內建的聆寫功能
            applescript = '''
            set userChoice to display dialog "🎙️ 請選擇輸入方式：" buttons {"結束", "打字輸入", "語音輸入"} default button "語音輸入" with title "小西助理"
            set buttonChoice to button returned of userChoice
            
            if buttonChoice is "結束" then
                return "quit"
            else if buttonChoice is "打字輸入" then
                set textInput to display dialog "請輸入您的訊息：" default answer "" with title "打字輸入"
                return "TEXT:" & (text returned of textInput)
            else if buttonChoice is "語音輸入" then
                -- 開啟語音聆寫（使用系統內建功能）
                try
                    -- 啟動語音聆寫
                    tell application "System Events"
                        -- 使用按鍵啟動聆寫（fn fn）
                        key code 63 using {fn down}  -- fn
                        key code 63 using {fn down}  -- fn
                    end tell
                    
                    -- 等待 1 秒讓聆寫啟動
                    delay 1
                    
                    -- 顯示聆寫狀態對話框
                    set voiceResult to display dialog "🎤 語音聆寫已啟動！\n\n請開始說話，說完後會自動轉換成文字。\n請在下方文字欄位確認或修正結果：" default answer "正在聆寫中...請稍候" with title "語音聆寫" giving up after 30
                    
                    -- 如果對話框沒有被關閉，獲取用戶輸入的文字
                    if gave up of voiceResult then
                        return "TIMEOUT:聆寫超時"
                    else
                        set transcribedText to text returned of voiceResult
                        if transcribedText is "正在聆寫中...請稍候" then
                            return "VOICE:聆寫無內容或失敗"
                        else
                            return "VOICE:" & transcribedText
                        end if
                    end if
                    
                on error errorMsg
                    -- 如果語音聆寫失敗，使用打字輸入
                    set fallbackInput to display dialog "語音聆寫無法啟動 (" & errorMsg & ")\n\n請改用打字輸入：" default answer "" with title "打字輸入"
                    return "TEXT:" & (text returned of fallbackInput)
                end try
            end if
            '''
            
            result = subprocess.run([
                'osascript', '-e', applescript
            ], capture_output=True, text=True, timeout=120)  # 2分鐘超時
            
            if result.returncode == 0 and result.stdout.strip():
                output = result.stdout.strip()
                
                if output == "quit":
                    return "quit"
                    
                # 解析輸入類型和內容
                if output.startswith("TEXT:"):
                    user_input = output[5:]
                    input_type = "打字"
                elif output.startswith("VOICE:"):
                    user_input = output[6:]
                    input_type = "語音"
                elif output.startswith("TIMEOUT:"):
                    print("⏰ 語音聆寫超時")
                    return None
                else:
                    user_input = output
                    input_type = "未知"
                    
                if user_input and not user_input.startswith("聆寫"):
                    print(f"\n💬 收到{input_type}輸入: {user_input}")
                    
                    # 處理輸入內容
                    response = self._process_voice_input(user_input)
                    
                    # 播放回應
                    if response:
                        print(f"🗨️ {self.config.get('assistant_name', '小西')}: {response}")
                        self.say(response, emotion='gentle')
                        
                    return "continue"
                else:
                    print("❌ 無效輸入")
            else:
                print("❌ 輸入失敗")
                
        except subprocess.TimeoutExpired:
            print("⏰ 輸入超時")
        except Exception as e:
            print(f"❌ 處理輸入時發生錯誤: {e}")
            
        return None
    
    def _process_voice_input(self, user_input: str) -> str:
        """處理用戶的語音輸入並產生回應"""
        user_input_lower = user_input.lower()
        assistant_name = self.config.get('assistant_name', '小西')
        
        # 問候回應
        if any(word in user_input for word in ['你好', '哈囉', 'hello', 'hi']):
            return f"你好！我是{assistant_name}，有什麼需要協助的嗎？"
        
        # 狀態查詢
        elif any(word in user_input for word in ['狀態', '怎麼樣', '如何']):
            return "目前一切正常，隨時準備協助您！"
        
        # 時間查詢
        elif any(word in user_input for word in ['時間', '現在幾點']):
            current_time = datetime.now().strftime('%H:%M')
            return f"現在是 {current_time}"
        
        # 幫助請求
        elif any(word in user_input for word in ['幫助', '協助', 'help']):
            return "我可以幫您發送通知、進行語音對話，或是協助 Claude Code 的各種任務。"
        
        # 結束命令
        elif any(word in user_input_lower for word in ['quit', 'exit', '結束', '再見', 'bye']):
            return "好的，再見！隨時可以再呼叫我。"
        
        # 預設回應
        else:
            return f"我收到了您的訊息：{user_input}。\n\n目前這是本地語音助理的測試版本。如果您想與 Claude 真正對話，請在 Claude Code 中使用此訊息。"


def main():
    """CLI 主程式"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Claude Code 語音助理',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
範例:
  %(prog)s notify "需要確認" --emotion urgent --details "資料庫連線失敗"
  %(prog)s test-failed "5 個單元測試失敗"
  %(prog)s mode silent
  %(prog)s blocked --emotion urgent

在其他專案中使用:
  from voice_assistant import ClaudeVoiceAssistant
  assistant = ClaudeVoiceAssistant()
  assistant.notify('需要您的協助', emotion='urgent')
        '''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # notify 命令
    notify_parser = subparsers.add_parser('notify', help='發送自訂通知')
    notify_parser.add_argument('message', nargs='?', help='通知訊息')
    notify_parser.add_argument('--emotion', choices=['urgent', 'gentle', 'excited', 'worried', 'thinking'],
                              help='情緒前綴')
    notify_parser.add_argument('--details', help='詳細資訊')
    
    # 按鍵監聽命令
    subparsers.add_parser('hotkey', help='啟動按鍵監聽模式（F5 語音輸入）')
    notify_parser.add_argument('--context', help='情境類型')
    
    # 快速命令
    for cmd in ['blocked', 'help', 'completed', 'error', 'git-conflict', 
                'test-failed', 'build-error', 'review']:
        cmd_parser = subparsers.add_parser(cmd, help=f'{cmd} 通知')
        if cmd in ['blocked', 'help']:
            cmd_parser.add_argument('emotion', nargs='?', 
                                   choices=['urgent', 'gentle', 'excited', 'worried', 'thinking'],
                                   help='情緒前綴')
        if cmd in ['error', 'test-failed']:
            cmd_parser.add_argument('details', nargs='?', help='詳細資訊')
    
    # say 命令 - 自由說話
    say_parser = subparsers.add_parser('say', help='自由說話（不限制內容）')
    say_parser.add_argument('message', nargs='+', help='要說的話')
    say_parser.add_argument('--emotion', choices=['urgent', 'gentle', 'excited', 'worried', 'thinking'],
                           help='情緒前綴')
    say_parser.add_argument('--voice-only', action='store_true', help='只有語音，不顯示訊息')
    
    # talk 命令 - 模擬你跟我說話
    talk_parser = subparsers.add_parser('talk', help='模擬你跟我說話（我會回應）')
    talk_parser.add_argument('message', nargs='+', help='你想說的話')
    
    # 其他命令
    subparsers.add_parser('test', help='測試語音功能')
    subparsers.add_parser('test-notification', help='測試互動式通知')
    subparsers.add_parser('chat', help='語音對話模式')
    
    # 聆聽命令
    listen_parser = subparsers.add_parser('listen', help='聆聽語音輸入')
    listen_parser.add_argument('--dialog-only', action='store_true', help='只使用對話框，不使用語音識別')
    listen_parser.add_argument('--duration', type=int, default=5, help='聆聽時間（秒）')
    listen_parser.add_argument('message', nargs='*', help='直接提供訊息（供測試用）')
    listen_parser.add_argument('--hotkey-mode', action='store_true', help='啟動按鍵監聽模式')
    
    mode_parser = subparsers.add_parser('mode', help='設定通知模式')
    mode_parser.add_argument('mode', nargs='?', choices=['full', 'silent', 'off'],
                           help='通知模式')
    
    # config 命令
    config_parser = subparsers.add_parser('config', help='設定管理')
    config_parser.add_argument('--show', action='store_true', help='顯示目前設定')
    config_parser.add_argument('--set', nargs=2, metavar=('KEY', 'VALUE'), help='設定單一項目')
    config_parser.add_argument('--add-device', metavar='DEVICE', help='加入音訊裝置')
    config_parser.add_argument('--remove-device', metavar='DEVICE', help='移除音訊裝置')
    
    args = parser.parse_args()
    
    # 初始化助理
    assistant = ClaudeVoiceAssistant()
    
    # 處理命令
    if args.command == 'notify':
        assistant.notify(
            message=args.message,
            emotion=args.emotion,
            details=args.details,
            context=args.context
        )
    
    elif args.command == 'blocked':
        assistant.quick_notify('blocked', args.emotion if hasattr(args, 'emotion') else None)
    
    elif args.command == 'help':
        assistant.quick_notify('need_help', args.emotion if hasattr(args, 'emotion') else None)
    
    elif args.command == 'completed':
        assistant.quick_notify('task_completed', 'excited')
    
    elif args.command == 'error':
        assistant.quick_notify('error', 'worried', args.details if hasattr(args, 'details') else None)
    
    elif args.command == 'git-conflict':
        assistant.quick_notify('git_conflict', 'urgent')
    
    elif args.command == 'test-failed':
        assistant.quick_notify('test_failed', 'worried', args.details if hasattr(args, 'details') else None)
    
    elif args.command == 'build-error':
        assistant.quick_notify('build_error', 'worried')
    
    elif args.command == 'review':
        assistant.quick_notify('review_required', 'gentle')
    
    elif args.command == 'say':
        message = ' '.join(args.message)
        assistant.say(message, args.emotion, args.voice_only)
    
    elif args.command == 'talk':
        # 模擬你跟我說話，我會智能回應
        user_message = ' '.join(args.message)
        print(f"👤 你說: {user_message}")
        
        # 簡單的智能回應
        if '你好' in user_message or '哈囉' in user_message:
            assistant.say("你好！很高興聽到你的聲音！", emotion='excited')
        elif '測試' in user_message:
            assistant.say("測試進行中！語音功能正常運作！", emotion='gentle')
        elif '謝謝' in user_message:
            assistant.say("不客氣！很開心能幫到你！", emotion='gentle')
        elif '再見' in user_message:
            assistant.say("再見！期待下次和你聊天！", emotion='gentle')
        else:
            assistant.say(f"我聽到你說：{user_message}。很有趣的想法！", emotion='thinking')
    
    elif args.command == 'test':
        assistant.test_voice()
    
    elif args.command == 'test-notification':
        assistant.test_notification()
    
    elif args.command == 'chat':
        assistant.chat()
    
    elif args.command == 'listen':
        # 檢查是否啟用按鍵模式
        if hasattr(args, 'hotkey_mode') and args.hotkey_mode:
            assistant.start_hotkey_listener()
        # 如果提供了直接訊息，使用它
        elif args.message:
            result = ' '.join(args.message)
            print(f"📝 收到訊息: {result}")
            print(f"✅ 識別結果: {result}")
        else:
            use_speech = not args.dialog_only
            result = assistant.listen(duration=args.duration, use_real_speech=use_speech)
            if result:
                print(f"✅ 識別結果: {result}")
            else:
                print("❌ 沒有識別到任何內容")
    
    elif args.command == 'config':
        if args.show or not any([args.set, args.add_device, args.remove_device]):
            print('目前設定:')
            print(json.dumps(assistant.config, ensure_ascii=False, indent=2))
        
        if args.set:
            key, value = args.set
            # 嘗試轉換數值
            try:
                if value.lower() == 'true':
                    value = True
                elif value.lower() == 'false':
                    value = False
                elif value.isdigit():
                    value = int(value)
            except:
                pass
            assistant.update_config(key, value)
        
        if args.add_device:
            assistant.add_device(args.add_device)
        
        if args.remove_device:
            assistant.remove_device(args.remove_device)
    
    elif args.command == 'hotkey':
        assistant.start_hotkey_listener()
    
    elif args.command == 'mode':
        if args.mode:
            assistant.set_mode(args.mode)
        else:
            print(f"目前模式: {assistant.config['mode']}")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()