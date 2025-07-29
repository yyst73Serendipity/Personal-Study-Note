"""
文本分析工具模块
提供文本分析功能
"""

from typing import Dict, Any, List
import re

class TextAnalyzer:
    """文本分析器类"""
    
    def __init__(self):
        self.analysis_types = {
            'letter_count': self.count_letters,
            'word_count': self.word_count,
            'character_count': self.character_count,
            'line_count': self.line_count
        }
    
    def count_letters(self, text: str, letter: str = 'a') -> str:
        """统计字母出现次数"""
        try:
            if not text:
                return "❌ 文本为空"
            
            if not letter or len(letter) != 1:
                return "❌ 字母参数无效"
            
            # 转换为小写进行统计
            text_lower = text.lower()
            letter_lower = letter.lower()
            
            count = text_lower.count(letter_lower)
            
            return f"字母 '{letter}' 在文本中出现了 {count} 次"
        except Exception as e:
            return f"❌ 统计字母失败: {e}"
    
    def word_count(self, text: str) -> str:
        """统计单词数量"""
        try:
            if not text:
                return "❌ 文本为空"
            
            # 分割单词（支持中英文）
            words = re.findall(r'[a-zA-Z\u4e00-\u9fff]+', text)
            word_count = len(words)
            
            return f"文本中共有 {word_count} 个单词"
        except Exception as e:
            return f"❌ 统计单词失败: {e}"
    
    def character_count(self, text: str) -> str:
        """统计字符数量"""
        try:
            if not text:
                return "❌ 文本为空"
            
            char_count = len(text)
            char_count_no_spaces = len(text.replace(' ', ''))
            
            return f"文本共有 {char_count} 个字符（包含空格），{char_count_no_spaces} 个字符（不包含空格）"
        except Exception as e:
            return f"❌ 统计字符失败: {e}"
    
    def line_count(self, text: str) -> str:
        """统计行数"""
        try:
            if not text:
                return "❌ 文本为空"
            
            lines = text.split('\n')
            line_count = len(lines)
            
            return f"文本共有 {line_count} 行"
        except Exception as e:
            return f"❌ 统计行数失败: {e}"
    
    def analyze_text(self, text: str) -> str:
        """全面分析文本"""
        try:
            if not text:
                return "❌ 文本为空"
            
            analysis = {
                'characters': len(text),
                'characters_no_spaces': len(text.replace(' ', '')),
                'words': len(re.findall(r'[a-zA-Z\u4e00-\u9fff]+', text)),
                'lines': len(text.split('\n')),
                'sentences': len(re.split(r'[.!?。！？]', text)),
                'paragraphs': len([p for p in text.split('\n\n') if p.strip()])
            }
            
            result = f"📊 文本分析结果:\n"
            result += f"  - 字符数: {analysis['characters']} (含空格)\n"
            result += f"  - 字符数: {analysis['characters_no_spaces']} (不含空格)\n"
            result += f"  - 单词数: {analysis['words']}\n"
            result += f"  - 行数: {analysis['lines']}\n"
            result += f"  - 句子数: {analysis['sentences']}\n"
            result += f"  - 段落数: {analysis['paragraphs']}"
            
            return result
        except Exception as e:
            return f"❌ 文本分析失败: {e}"
    
    def find_most_common_letters(self, text: str, top_n: int = 5) -> str:
        """查找最常见的字母"""
        try:
            if not text:
                return "❌ 文本为空"
            
            # 只统计英文字母
            letters = re.findall(r'[a-zA-Z]', text.lower())
            
            if not letters:
                return "❌ 文本中没有英文字母"
            
            # 统计字母频率
            letter_count = {}
            for letter in letters:
                letter_count[letter] = letter_count.get(letter, 0) + 1
            
            # 排序
            sorted_letters = sorted(letter_count.items(), key=lambda x: x[1], reverse=True)
            
            result = f"📈 最常见的字母 (前{top_n}个):\n"
            for i, (letter, count) in enumerate(sorted_letters[:top_n], 1):
                result += f"  {i}. '{letter}': {count} 次\n"
            
            return result
        except Exception as e:
            return f"❌ 查找常见字母失败: {e}"
    
    def get_text_statistics(self, text: str) -> Dict[str, Any]:
        """获取文本统计信息"""
        try:
            if not text:
                return {"error": "文本为空"}
            
            stats = {
                'total_characters': len(text),
                'characters_no_spaces': len(text.replace(' ', '')),
                'words': len(re.findall(r'[a-zA-Z\u4e00-\u9fff]+', text)),
                'lines': len(text.split('\n')),
                'sentences': len(re.split(r'[.!?。！？]', text)),
                'paragraphs': len([p for p in text.split('\n\n') if p.strip()]),
                'chinese_chars': len(re.findall(r'[\u4e00-\u9fff]', text)),
                'english_chars': len(re.findall(r'[a-zA-Z]', text)),
                'digits': len(re.findall(r'\d', text)),
                'punctuation': len(re.findall(r'[^\w\s]', text))
            }
            
            return stats
        except Exception as e:
            return {"error": f"统计失败: {e}"}
    
    def validate_text(self, text: str) -> bool:
        """验证文本有效性"""
        return text is not None and len(text.strip()) > 0
    
    def get_supported_analyses(self) -> Dict[str, str]:
        """获取支持的分析类型"""
        return {
            'letter_count': '字母统计',
            'word_count': '单词统计',
            'character_count': '字符统计',
            'line_count': '行数统计',
            'full_analysis': '全面分析',
            'common_letters': '常见字母分析'
        }

# 创建全局文本分析器实例
text_analyzer = TextAnalyzer()

# 工具函数接口
def count_letters(text: str, letter: str = 'a') -> str:
    """统计字母工具函数"""
    return text_analyzer.count_letters(text, letter)

def word_count(text: str) -> str:
    """统计单词工具函数"""
    return text_analyzer.word_count(text)

def analyze_text(text: str) -> str:
    """全面分析文本工具函数"""
    return text_analyzer.analyze_text(text) 