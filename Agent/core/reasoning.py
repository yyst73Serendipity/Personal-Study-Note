"""
推理模块
负责基于用户输入和历史进行推理，实现决策逻辑
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from .perception import ParsedInput
from .memory import DialogueRecord

@dataclass
class ReasoningResult:
    """推理结果"""
    intent: str
    confidence: float
    selected_tool: Optional[str]
    tool_parameters: Dict[str, Any]
    reasoning_chain: List[str]
    suggested_response: str

class ReasoningModule:
    """推理模块"""
    
    def __init__(self):
        # 意图权重配置
        self.intent_weights = {
            'calculator': 0.9,
            'translator': 0.8,
            'datetime': 0.7,
            'text_analyzer': 0.6,
            'greeting': 0.5,
            'help': 0.4,
            'farewell': 0.3,
            'unknown': 0.1
        }
        
        # 工具选择规则
        self.tool_selection_rules = {
            'calculator': {
                'add': ['加', 'add', '加法', 'plus'],
                'subtract': ['减', 'subtract', '减法', 'minus'],
                'multiply': ['乘', 'multiply', '乘法', 'times'],
                'divide': ['除', 'divide', '除法', 'divided']
            },
            'translator': {
                'translate': ['翻译', 'translate', '中译英', '英译中']
            },
            'datetime': {
                'get_current_time': ['时间', 'time', '几点', '现在'],
                'get_current_date': ['日期', 'date', '今天', '几号']
            },
            'text_analyzer': {
                'count_letters': ['字母', 'letter', '字符'],
                'word_count': ['单词', 'word', '词数']
            }
        }
    
    def reason(self, parsed_input: ParsedInput, recent_history: List[DialogueRecord]) -> ReasoningResult:
        """主推理方法"""
        reasoning_chain = []
        
        # 1. 基础意图分析
        base_intent = parsed_input.intent
        base_confidence = parsed_input.confidence
        reasoning_chain.append(f"识别到基础意图: {base_intent} (置信度: {base_confidence:.2f})")
        
        # 2. 历史上下文增强
        enhanced_intent, enhanced_confidence = self._enhance_with_history(
            base_intent, base_confidence, recent_history
        )
        reasoning_chain.append(f"历史上下文增强后意图: {enhanced_intent} (置信度: {enhanced_confidence:.2f})")
        
        # 3. 工具选择
        selected_tool, tool_params = self._select_tool(enhanced_intent, parsed_input.parameters)
        reasoning_chain.append(f"选择工具: {selected_tool or '无'}")
        
        # 4. 参数推理
        final_params = self._infer_parameters(selected_tool, parsed_input.parameters, recent_history)
        reasoning_chain.append(f"推理参数: {final_params}")
        
        # 5. 生成回复建议
        suggested_response = self._generate_response_suggestion(
            enhanced_intent, selected_tool, final_params, recent_history
        )
        
        return ReasoningResult(
            intent=enhanced_intent,
            confidence=enhanced_confidence,
            selected_tool=selected_tool,
            tool_parameters=final_params,
            reasoning_chain=reasoning_chain,
            suggested_response=suggested_response
        )
    
    def _enhance_with_history(self, base_intent: str, base_confidence: float, 
                             history: List[DialogueRecord]) -> Tuple[str, float]:
        """基于历史增强意图识别"""
        if not history:
            return base_intent, base_confidence
        
        # 分析最近的对话模式
        recent_intents = [record.intent for record in history[-3:]]
        
        # 如果最近有相似意图，提高置信度
        if base_intent in recent_intents:
            enhanced_confidence = min(base_confidence * 1.2, 1.0)
            return base_intent, enhanced_confidence
        
        # 如果最近有工具使用模式，可能影响当前意图
        recent_tools = [record.tool_used for record in history[-3:] if record.tool_used]
        if recent_tools:
            # 根据工具使用模式调整意图
            tool_intent_map = {
                'add': 'calculator', 'subtract': 'calculator', 'multiply': 'calculator', 'divide': 'calculator',
                'translate': 'translator',
                'get_current_time': 'datetime', 'get_current_date': 'datetime',
                'count_letters': 'text_analyzer', 'word_count': 'text_analyzer'
            }
            
            for tool in recent_tools:
                if tool in tool_intent_map and tool_intent_map[tool] == base_intent:
                    enhanced_confidence = min(base_confidence * 1.1, 1.0)
                    return base_intent, enhanced_confidence
        
        return base_intent, base_confidence
    
    def _select_tool(self, intent: str, parameters: Dict[str, Any]) -> Tuple[Optional[str], Dict[str, Any]]:
        """选择工具"""
        if intent not in self.tool_selection_rules:
            return None, parameters
        
        # 根据参数和意图选择最合适的工具
        available_tools = self.tool_selection_rules[intent]
        
        # 对于计算器，根据参数选择具体操作
        if intent == 'calculator':
            if 'a' in parameters and 'b' in parameters:
                # 根据关键词选择操作
                if any(keyword in parameters.get('operation', '').lower() for keyword in ['加', 'add', 'plus']):
                    return 'add', parameters
                elif any(keyword in parameters.get('operation', '').lower() for keyword in ['减', 'subtract', 'minus']):
                    return 'subtract', parameters
                elif any(keyword in parameters.get('operation', '').lower() for keyword in ['乘', 'multiply', 'times']):
                    return 'multiply', parameters
                elif any(keyword in parameters.get('operation', '').lower() for keyword in ['除', 'divide']):
                    return 'divide', parameters
                else:
                    # 默认加法
                    return 'add', parameters
        
        # 对于翻译器
        elif intent == 'translator':
            if 'text' in parameters:
                return 'translate', parameters
        
        # 对于时间日期
        elif intent == 'datetime':
            if any(keyword in parameters.get('query', '').lower() for keyword in ['日期', 'date', '几号']):
                return 'get_current_date', parameters
            else:
                return 'get_current_time', parameters
        
        # 对于文本分析
        elif intent == 'text_analyzer':
            if 'text' in parameters:
                if 'letter' in parameters or any(keyword in parameters.get('query', '').lower() for keyword in ['字母', 'letter']):
                    return 'count_letters', parameters
                else:
                    return 'word_count', parameters
            elif 'letter' in parameters:
                # 如果有字母参数但没有文本，尝试从历史中获取文本
                return 'count_letters', parameters
        
        return None, parameters
    
    def _infer_parameters(self, tool: Optional[str], base_params: Dict[str, Any], 
                         history: List[DialogueRecord]) -> Dict[str, Any]:
        """推理参数"""
        inferred_params = base_params.copy()
        
        if not tool or not history:
            return inferred_params
        
        # 根据历史对话推理缺失参数
        recent_records = history[-5:]  # 最近5条记录
        
        for record in recent_records:
            if record.tool_used == tool and record.parameters:
                # 如果当前参数缺失，使用历史参数作为默认值
                for key, value in record.parameters.items():
                    if key not in inferred_params:
                        inferred_params[key] = value
        
        # 特殊参数推理
        if tool == 'count_letters' and 'text' in inferred_params and 'letter' not in inferred_params:
            # 如果没有指定字母，使用默认值
            inferred_params['letter'] = 'a'
        
        return inferred_params
    
    def _generate_response_suggestion(self, intent: str, tool: Optional[str], 
                                    parameters: Dict[str, Any], history: List[DialogueRecord]) -> str:
        """生成回复建议"""
        if intent == 'greeting':
            return "你好！我是智能助手，有什么可以帮助你的吗？"
        
        elif intent == 'farewell':
            return "再见！欢迎下次使用！"
        
        elif intent == 'help':
            return "我可以帮你进行数学计算、文本翻译、时间查询、文本分析等。请告诉我你需要什么帮助！"
        
        elif intent == 'unknown':
            return "抱歉，我没有理解你的意思。你可以尝试说：计算2+3、翻译'hello'、现在几点了等。"
        
        elif tool:
            # 根据工具和参数生成回复建议
            if tool == 'add':
                return f"我来帮你计算 {parameters.get('a', 0)} + {parameters.get('b', 0)}"
            elif tool == 'translate':
                return f"我来帮你翻译 '{parameters.get('text', '')}'"
            elif tool == 'get_current_time':
                return "我来查询当前时间"
            elif tool == 'get_current_date':
                return "我来查询当前日期"
            elif tool == 'count_letters':
                return f"我来统计文本中字母 '{parameters.get('letter', 'a')}' 的出现次数"
            else:
                return f"我来执行 {tool} 操作"
        
        else:
            return "我理解你的意图，但暂时没有合适的工具来处理这个请求。"
    
    def get_reasoning_explanation(self, result: ReasoningResult) -> str:
        """获取推理过程解释"""
        explanation = "🧠 推理过程:\n"
        
        for i, step in enumerate(result.reasoning_chain, 1):
            explanation += f"  {i}. {step}\n"
        
        explanation += f"\n📊 最终决策:\n"
        explanation += f"  - 意图: {result.intent} (置信度: {result.confidence:.2f})\n"
        explanation += f"  - 工具: {result.selected_tool or '无'}\n"
        explanation += f"  - 参数: {result.tool_parameters}\n"
        
        return explanation
    
    def validate_reasoning(self, result: ReasoningResult) -> bool:
        """验证推理结果的有效性"""
        # 检查置信度
        if result.confidence < 0.3:
            return False
        
        # 检查工具和参数的匹配
        if result.selected_tool:
            required_params = {
                'add': ['a', 'b'],
                'subtract': ['a', 'b'],
                'multiply': ['a', 'b'],
                'divide': ['a', 'b'],
                'translate': ['text'],
                'get_current_time': [],
                'get_current_date': [],
                'count_letters': ['text', 'letter'],
                'word_count': ['text']
            }
            
            if result.selected_tool in required_params:
                required = required_params[result.selected_tool]
                for param in required:
                    if param not in result.tool_parameters:
                        return False
        
        return True 