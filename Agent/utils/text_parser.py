"""
文本解析工具模块
提供文本解析和处理功能
"""

import re
from typing import List, Dict, Any, Tuple

class TextParser:
    """文本解析器"""
    
    def __init__(self):
        # 数字模式
        self.number_pattern = r'(\d+(?:\.\d+)?)'
        
        # 文本模式（引号内的内容）
        self.text_pattern = r'["""]([^"""]+)["""]'
        
        # 操作符模式
        self.operator_pattern = r'([+\-*/=])'
        
        # 关键词模式
        self.keyword_patterns = {
            'calculator': r'\b(计算|加|减|乘|除|等于|add|subtract|multiply|divide|calculate)\b',
            'translator': r'\b(翻译|translate|中译英|英译中)\b',
            'datetime': r'\b(时间|日期|现在|今天|time|date|current)\b',
            'text_analyzer': r'\b(统计|计数|分析|count|analyze|字母|单词)\b'
        }
    
    def extract_numbers(self, text: str) -> List[float]:
        """提取数字"""
        numbers = re.findall(self.number_pattern, text)
        return [float(num) for num in numbers]
    
    def extract_text(self, text: str) -> List[str]:
        """提取引号内的文本"""
        return re.findall(self.text_pattern, text)
    
    def extract_operators(self, text: str) -> List[str]:
        """提取操作符"""
        return re.findall(self.operator_pattern, text)
    
    def extract_keywords(self, text: str) -> Dict[str, List[str]]:
        """提取关键词"""
        keywords = {}
        
        for category, pattern in self.keyword_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                keywords[category] = matches
        
        return keywords
    
    def parse_calculation_expression(self, text: str) -> Dict[str, Any]:
        """解析计算表达式"""
        numbers = self.extract_numbers(text)
        operators = self.extract_operators(text)
        
        if len(numbers) >= 2 and operators:
            return {
                'numbers': numbers[:2],  # 取前两个数字
                'operator': operators[0],  # 取第一个操作符
                'expression': f"{numbers[0]}{operators[0]}{numbers[1]}"
            }
        
        return {}
    
    def parse_translation_request(self, text: str) -> Dict[str, Any]:
        """解析翻译请求"""
        quoted_text = self.extract_text(text)
        
        if quoted_text:
            return {
                'text': quoted_text[0],
                'source': 'quoted'
            }
        
        # 如果没有引号，尝试提取最后一个单词
        words = text.split()
        if len(words) > 1:
            # 跳过翻译关键词
            translation_keywords = ['翻译', 'translate', '中译英', '英译中']
            for word in reversed(words):
                if word.lower() not in [kw.lower() for kw in translation_keywords]:
                    return {
                        'text': word,
                        'source': 'last_word'
                    }
        
        return {}
    
    def parse_datetime_request(self, text: str) -> Dict[str, Any]:
        """解析时间日期请求"""
        text_lower = text.lower()
        
        if any(keyword in text_lower for keyword in ['日期', 'date', '几号', '今天']):
            return {
                'type': 'date',
                'query': 'current_date'
            }
        else:
            return {
                'type': 'time',
                'query': 'current_time'
            }
    
    def parse_text_analysis_request(self, text: str) -> Dict[str, Any]:
        """解析文本分析请求"""
        quoted_text = self.extract_text(text)
        text_lower = text.lower()
        
        result = {}
        
        if quoted_text:
            result['text'] = quoted_text[0]
        
        # 判断分析类型
        if any(keyword in text_lower for keyword in ['字母', 'letter', '字符']):
            result['type'] = 'letter_count'
            # 尝试提取具体字母
            letter_match = re.search(r'字母\s*([a-zA-Z])', text)
            if letter_match:
                result['letter'] = letter_match.group(1)
            else:
                result['letter'] = 'a'  # 默认
        else:
            result['type'] = 'word_count'
        
        return result
    
    def detect_language(self, text: str) -> str:
        """检测文本语言"""
        # 简单的语言检测
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        english_chars = len(re.findall(r'[a-zA-Z]', text))
        
        if chinese_chars > english_chars:
            return 'zh'
        elif english_chars > chinese_chars:
            return 'en'
        else:
            return 'unknown'
    
    def normalize_text(self, text: str) -> str:
        """标准化文本"""
        # 移除多余空格
        text = re.sub(r'\s+', ' ', text.strip())
        
        # 统一标点符号
        text = text.replace('，', ',').replace('。', '.').replace('！', '!').replace('？', '?')
        
        return text
    
    def extract_parameters(self, text: str, intent: str) -> Dict[str, Any]:
        """根据意图提取参数"""
        if intent == 'calculator':
            return self.parse_calculation_expression(text)
        elif intent == 'translator':
            return self.parse_translation_request(text)
        elif intent == 'datetime':
            return self.parse_datetime_request(text)
        elif intent == 'text_analyzer':
            return self.parse_text_analysis_request(text)
        else:
            return {}
    
    def validate_input(self, text: str) -> Tuple[bool, str]:
        """验证输入有效性"""
        if not text or not text.strip():
            return False, "输入不能为空"
        
        if len(text) > 1000:
            return False, "输入文本过长"
        
        # 检查是否包含有效字符
        if not re.search(r'[a-zA-Z\u4e00-\u9fff0-9]', text):
            return False, "输入必须包含有效字符"
        
        return True, "输入有效"
    
    def get_parsing_summary(self, text: str) -> str:
        """获取解析摘要"""
        summary = f"📝 文本解析摘要:\n"
        summary += f"  - 原始文本: {text}\n"
        summary += f"  - 标准化文本: {self.normalize_text(text)}\n"
        summary += f"  - 检测语言: {self.detect_language(text)}\n"
        
        # 提取的信息
        numbers = self.extract_numbers(text)
        if numbers:
            summary += f"  - 提取数字: {numbers}\n"
        
        quoted_text = self.extract_text(text)
        if quoted_text:
            summary += f"  - 引号文本: {quoted_text}\n"
        
        keywords = self.extract_keywords(text)
        if keywords:
            summary += f"  - 识别关键词: {keywords}\n"
        
        return summary 