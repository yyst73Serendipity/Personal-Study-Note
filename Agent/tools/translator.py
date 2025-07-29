"""
翻译工具模块
提供文本翻译功能
"""

import requests
import hashlib
import random
from typing import Dict, Any, Optional

class Translator:
    """翻译器类"""
    
    def __init__(self):
        # 百度翻译API配置（需要用户填写）
        self.appid = "20250717002408443"  # TODO: 填写你的appid
        self.secret_key = "mtOUVbligDBfVUehlOQx"  # TODO: 填写你的密钥
        self.api_url = "https://fanyi-api.baidu.com/api/trans/vip/translate"
        
        # 支持的语言
        self.supported_languages = {
            'zh': '中文',
            'en': '英文',
            'ja': '日文',
            'ko': '韩文',
            'fr': '法文',
            'de': '德文',
            'es': '西班牙文',
            'ru': '俄文'
        }
    
    def detect_language(self, text: str) -> str:
        """检测文本语言"""
        # 简单的语言检测
        chinese_chars = len([c for c in text if '\u4e00' <= c <= '\u9fff'])
        english_chars = len([c for c in text if c.isalpha() and ord(c) < 128])
        
        if chinese_chars > english_chars:
            return 'zh'
        elif english_chars > chinese_chars:
            return 'en'
        else:
            return 'unknown'
    
    def translate(self, text: str, from_lang: Optional[str] = None, to_lang: Optional[str] = None) -> str:
        """翻译文本"""
        try:
            if not text:
                return "❌ 翻译文本为空"
            
            # 自动检测语言
            if not from_lang:
                from_lang = self.detect_language(text)
            
            # 确定目标语言
            if not to_lang:
                to_lang = 'en' if from_lang == 'zh' else 'zh'
            
            # 如果语言相同，直接返回
            if from_lang == to_lang:
                return f"源语言和目标语言相同: {text}"
            
            # 调用百度翻译API
            return self._call_baidu_api(text, from_lang, to_lang)
            
        except Exception as e:
            return f"❌ 翻译失败: {e}"
    
    def _call_baidu_api(self, text: str, from_lang: str, to_lang: str) -> str:
        """调用百度翻译API"""
        try:
            # 检查API配置
            if self.appid == "your appid" or self.secret_key == "your secret key":
                return "❌ 请先配置百度翻译API的appid和secret_key"
            
            # 构造请求参数
            salt = str(random.randint(32768, 65536))
            sign = self.appid + text + salt + self.secret_key
            sign = hashlib.md5(sign.encode()).hexdigest()
            
            params = {
                'q': text,
                'from': from_lang,
                'to': to_lang,
                'appid': self.appid,
                'salt': salt,
                'sign': sign
            }
            
            # 发送请求
            response = requests.get(self.api_url, params=params, timeout=5)
            result = response.json()
            
            if 'trans_result' in result:
                translated_text = result['trans_result'][0]['dst']
                return f"翻译结果: {translated_text}"
            else:
                error_msg = result.get('error_msg', '未知错误')
                return f"❌ 翻译API错误: {error_msg}"
                
        except requests.exceptions.RequestException as e:
            return f"❌ 网络请求失败: {e}"
        except Exception as e:
            return f"❌ API调用失败: {e}"
    
    def translate_batch(self, texts: list, from_lang: str = 'auto', to_lang: str = 'zh') -> list:
        """批量翻译"""
        results = []
        for text in texts:
            result = self.translate(text, from_lang, to_lang)
            results.append(result)
        return results
    
    def get_supported_languages(self) -> Dict[str, str]:
        """获取支持的语言"""
        return self.supported_languages
    
    def validate_language_code(self, lang_code: str) -> bool:
        """验证语言代码"""
        return lang_code in self.supported_languages
    
    def get_language_name(self, lang_code: str) -> str:
        """获取语言名称"""
        return self.supported_languages.get(lang_code, '未知语言')
    
    def set_api_credentials(self, appid: str, secret_key: str):
        """设置API凭据"""
        self.appid = appid
        self.secret_key = secret_key
        print("✅ API凭据已设置")
    
    def test_connection(self) -> str:
        """测试API连接"""
        try:
            if self.appid == "your appid" or self.secret_key == "your secret key":
                return "❌ 请先配置API凭据"
            
            # 测试翻译
            result = self.translate("hello", "en", "zh")
            if "翻译结果" in result:
                return "✅ API连接正常"
            else:
                return f"❌ API连接失败: {result}"
                
        except Exception as e:
            return f"❌ 连接测试失败: {e}"

# 创建全局翻译器实例
translator = Translator()

# 工具函数接口
def translate(text: str, from_lang: Optional[str] = None, to_lang: Optional[str] = None) -> str:
    """翻译工具函数"""
    return translator.translate(text, from_lang, to_lang)

def detect_language(text: str) -> str:
    """语言检测工具函数"""
    return translator.detect_language(text) 