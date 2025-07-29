"""
感知模块
负责解析用户输入，提取意图和参数
"""

import re
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass

@dataclass
class ParsedInput:
    """解析后的输入"""
    original_text: str
    intent: str
    confidence: float
    parameters: Dict[str, Any]
    keywords: List[str]

class PerceptionModule:
    """感知模块"""
    
    def __init__(self):
        # 意图关键词映射
        self.intent_keywords = {
            'calculator': ['计算', '加', '减', '乘', '除', '等于', 'add', 'subtract', 'multiply', 'divide', 'calculate'],
            'translator': ['翻译', 'translate', '中译英', '英译中'],
            'datetime': ['时间', '日期', '现在几点', '今天', 'time', 'date', 'current'],
            'text_analyzer': ['统计', '计数', '分析', 'count', 'analyze', '字母', '单词'],
            'greeting': ['你好', 'hello', 'hi', '您好'],
            'farewell': ['再见', 'bye', 'goodbye', '退出', 'exit'],
            'help': ['帮助', 'help', '功能', '能做什么']
        }
        
        # 数字提取模式
        self.number_pattern = r'(\d+(?:\.\d+)?)'
        
        # 文本提取模式（引号内的内容）
        self.text_pattern = r'["""]([^"""]+)["""]'
        
    def parse_input(self, user_input: str) -> ParsedInput:
        """解析用户输入"""
        original_text = user_input.strip()
        
        # 提取关键词
        keywords = self._extract_keywords(original_text)
        
        # 识别意图
        intent, confidence = self._identify_intent(original_text, keywords)
        
        # 提取参数
        parameters = self._extract_parameters(original_text, intent)
        
        return ParsedInput(
            original_text=original_text,
            intent=intent,
            confidence=confidence,
            parameters=parameters,
            keywords=keywords
        )
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        keywords = []
        text_lower = text.lower()
        
        for intent, intent_keywords in self.intent_keywords.items():
            for keyword in intent_keywords:
                if keyword.lower() in text_lower:
                    keywords.append(keyword)
        
        return keywords
    
    def _identify_intent(self, text: str, keywords: List[str]) -> Tuple[str, float]:
        """识别意图"""
        text_lower = text.lower()
        
        # 计算每个意图的匹配分数
        intent_scores = {}
        
        for intent, intent_keywords in self.intent_keywords.items():
            score = 0
            for keyword in intent_keywords:
                if keyword.lower() in text_lower:
                    score += 1
            
            if score > 0:
                intent_scores[intent] = score
        
        if not intent_scores:
            return 'unknown', 0.0
        
        # 选择得分最高的意图
        best_intent = max(intent_scores.items(), key=lambda x: x[1])
        confidence = min(best_intent[1] / len(keywords) if keywords else 1, 1.0)
        
        return best_intent[0], confidence
    
    def _extract_parameters(self, text: str, intent: str) -> Dict[str, Any]:
        """提取参数"""
        parameters = {}
        
        if intent == 'calculator':
            # 提取数字
            numbers = re.findall(self.number_pattern, text)
            if len(numbers) >= 2:
                parameters['a'] = float(numbers[0])
                parameters['b'] = float(numbers[1])
            elif len(numbers) == 1:
                parameters['a'] = float(numbers[0])
        
        elif intent == 'translator':
            # 支持中英文引号和单引号
            quoted_text = re.findall(r'[\"“”\']([^\"“”\']+)[\"””\']', text)
            if quoted_text:
                parameters['text'] = quoted_text[0]
            else:
                # 如果没有引号，尝试提取最后一个单词或短语
                words = text.split()
                if len(words) > 1:
                    intent_keywords = self.intent_keywords.get('translator', [])
                    for i, word in enumerate(words):
                        if word.lower() not in [kw.lower() for kw in intent_keywords]:
                            parameters['text'] = word
                            break
        
        elif intent == 'text_analyzer':
            # 支持中英文引号
            quoted_text = re.findall(r'[\"“”\']([^\"“”\']+)[\"””\']', text)
            if quoted_text:
                parameters['text'] = quoted_text[0]
            # 提取要统计的字符
            if '字母' in text or 'letter' in text.lower():
                # 尝试提取具体的字母
                letter_match = re.search(r'字母\s*([a-zA-Z])', text)
                if letter_match:
                    parameters['letter'] = letter_match.group(1)
                else:
                    # 如果没有明确指定字母，尝试从文本中提取
                    letter_match = re.search(r'([a-zA-Z])\s*的数量', text)
                    if letter_match:
                        parameters['letter'] = letter_match.group(1)
                    else:
                        parameters['letter'] = 'a'  # 默认统计字母a
        
        return parameters
    
    def get_intent_description(self, intent: str) -> str:
        """获取意图描述"""
        intent_descriptions = {
            'calculator': '数学计算',
            'translator': '文本翻译',
            'datetime': '时间日期查询',
            'text_analyzer': '文本分析',
            'greeting': '问候',
            'farewell': '告别',
            'help': '帮助',
            'unknown': '未知意图'
        }
        
        return intent_descriptions.get(intent, '未知意图')
    
    def is_valid_input(self, text: str) -> bool:
        """检查输入是否有效"""
        return bool(text.strip())
    
    def get_suggestions(self, text: str) -> List[str]:
        """获取输入建议"""
        suggestions = []
        
        if not text.strip():
            suggestions.append("请输入您的问题或指令")
            return suggestions
        
        # 根据当前输入提供建议
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['计算', '加', '减', '乘', '除']):
            suggestions.append("例如：计算 2+3")
            suggestions.append("例如：5乘以8等于多少")
        
        elif any(word in text_lower for word in ['翻译', 'translate']):
            suggestions.append("例如：翻译 'hello'")
            suggestions.append("例如：把'你好'翻译成英文")
        
        elif any(word in text_lower for word in ['时间', '日期']):
            suggestions.append("例如：现在几点了")
            suggestions.append("例如：今天是几号")
        
        else:
            suggestions.append("您可以尝试：计算、翻译、查询时间等")
        
        return suggestions 