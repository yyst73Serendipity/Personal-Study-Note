"""
记忆模块
负责管理对话历史和上下文状态
"""

import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
import os

@dataclass
class DialogueRecord:
    """对话记录"""
    timestamp: str
    user_input: str
    intent: str
    confidence: float
    parameters: Dict[str, Any]
    tool_used: Optional[str]
    tool_result: Optional[str]
    response: str
    session_id: str

class MemoryModule:
    """记忆模块"""
    
    def __init__(self, max_history: int = 50, data_dir: str = "data"):
        self.max_history = max_history
        self.data_dir = data_dir
        self.dialogue_history: List[DialogueRecord] = []
        self.current_session_id = self._generate_session_id()
        
        # 确保数据目录存在
        os.makedirs(data_dir, exist_ok=True)
        
        # 加载历史对话
        self._load_history()
    
    def _generate_session_id(self) -> str:
        """生成会话ID"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def add_dialogue(self, record: DialogueRecord):
        """添加对话记录"""
        self.dialogue_history.append(record)
        
        # 保持历史记录在限制范围内
        if len(self.dialogue_history) > self.max_history:
            self.dialogue_history = self.dialogue_history[-self.max_history:]
        
        # 保存到文件
        self._save_history()
    
    def get_recent_dialogues(self, count: int = 5) -> List[DialogueRecord]:
        """获取最近的对话记录"""
        return self.dialogue_history[-count:] if self.dialogue_history else []
    
    def get_dialogues_by_intent(self, intent: str) -> List[DialogueRecord]:
        """根据意图获取对话记录"""
        return [record for record in self.dialogue_history if record.intent == intent]
    
    def get_dialogues_by_tool(self, tool_name: str) -> List[DialogueRecord]:
        """根据工具获取对话记录"""
        return [record for record in self.dialogue_history if record.tool_used == tool_name]
    
    def get_context_summary(self) -> Dict[str, Any]:
        """获取上下文摘要"""
        if not self.dialogue_history:
            return {
                'total_dialogues': 0,
                'session_id': self.current_session_id,
                'recent_intents': [],
                'frequently_used_tools': []
            }
        
        # 统计最近的意图
        recent_intents = [record.intent for record in self.dialogue_history[-10:]]
        
        # 统计常用工具
        tool_usage = {}
        for record in self.dialogue_history:
            if record.tool_used:
                tool_usage[record.tool_used] = tool_usage.get(record.tool_used, 0) + 1
        
        frequently_used_tools = sorted(tool_usage.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'total_dialogues': len(self.dialogue_history),
            'session_id': self.current_session_id,
            'recent_intents': recent_intents,
            'frequently_used_tools': frequently_used_tools
        }
    
    def find_similar_dialogues(self, current_input: str, limit: int = 3) -> List[DialogueRecord]:
        """查找相似对话"""
        similar_records = []
        
        for record in reversed(self.dialogue_history):
            # 简单的相似度计算（基于关键词匹配）
            similarity = self._calculate_similarity(current_input, record.user_input)
            if similarity > 0.3:  # 相似度阈值
                similar_records.append(record)
                if len(similar_records) >= limit:
                    break
        
        return similar_records
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """计算文本相似度（简单实现）"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    def get_user_preferences(self) -> Dict[str, Any]:
        """获取用户偏好"""
        preferences = {
            'favorite_intents': [],
            'favorite_tools': [],
            'common_parameters': {}
        }
        
        if not self.dialogue_history:
            return preferences
        
        # 统计意图偏好
        intent_count = {}
        tool_count = {}
        param_patterns = {}
        
        for record in self.dialogue_history:
            # 统计意图
            intent_count[record.intent] = intent_count.get(record.intent, 0) + 1
            
            # 统计工具使用
            if record.tool_used:
                tool_count[record.tool_used] = tool_count.get(record.tool_used, 0) + 1
            
            # 统计参数模式
            if record.parameters:
                for key, value in record.parameters.items():
                    if key not in param_patterns:
                        param_patterns[key] = []
                    param_patterns[key].append(value)
        
        # 获取最常用的意图和工具
        preferences['favorite_intents'] = sorted(intent_count.items(), key=lambda x: x[1], reverse=True)[:3]
        preferences['favorite_tools'] = sorted(tool_count.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # 获取常用参数模式
        for key, values in param_patterns.items():
            if len(values) > 1:
                preferences['common_parameters'][key] = list(set(values))[:3]
        
        return preferences
    
    def clear_history(self):
        """清空对话历史"""
        self.dialogue_history.clear()
        self._save_history()
    
    def _save_history(self):
        """保存对话历史到文件"""
        try:
            history_data = [asdict(record) for record in self.dialogue_history]
            file_path = os.path.join(self.data_dir, "dialogue_history.json")
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(history_data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"⚠️  保存对话历史失败: {e}")
    
    def _load_history(self):
        """从文件加载对话历史"""
        try:
            file_path = os.path.join(self.data_dir, "dialogue_history.json")
            
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    history_data = json.load(f)
                
                self.dialogue_history = []
                for record_data in history_data:
                    record = DialogueRecord(**record_data)
                    self.dialogue_history.append(record)
                
                print(f"📚 已加载 {len(self.dialogue_history)} 条对话历史")
                
        except Exception as e:
            print(f"⚠️  加载对话历史失败: {e}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        if not self.dialogue_history:
            return {
                'total_dialogues': 0,
                'session_count': 0,
                'intent_distribution': {},
                'tool_usage': {},
                'average_confidence': 0.0
            }
        
        # 统计意图分布
        intent_distribution = {}
        tool_usage = {}
        total_confidence = 0.0
        
        for record in self.dialogue_history:
            intent_distribution[record.intent] = intent_distribution.get(record.intent, 0) + 1
            if record.tool_used:
                tool_usage[record.tool_used] = tool_usage.get(record.tool_used, 0) + 1
            total_confidence += record.confidence
        
        return {
            'total_dialogues': len(self.dialogue_history),
            'session_count': len(set(record.session_id for record in self.dialogue_history)),
            'intent_distribution': intent_distribution,
            'tool_usage': tool_usage,
            'average_confidence': total_confidence / len(self.dialogue_history)
        } 