"""
工具管理器
负责工具的注册、管理和调用
"""

from typing import Dict, Any, Optional, List
import inspect
from dataclasses import dataclass

@dataclass
class Tool:
    """工具类"""
    name: str
    description: str
    function: callable
    parameters: Dict[str, Any]
    required_params: List[str]

class ToolManager:
    """工具管理器"""
    
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
        self.tool_categories = {
            'calculator': ['add', 'subtract', 'multiply', 'divide'],
            'translator': ['translate'],
            'datetime': ['get_current_time', 'get_current_date'],
            'text_analyzer': ['count_letters', 'word_count']
        }
    
    def register_tool(self, name: str, description: str, func: callable):
        """注册工具"""
        # 获取函数参数信息
        sig = inspect.signature(func)
        parameters = {}
        required_params = []
        
        for param_name, param in sig.parameters.items():
            param_type = param.annotation if param.annotation != inspect.Parameter.empty else str
            parameters[param_name] = {
                'type': self._get_type_name(param_type),
                'description': f'参数 {param_name}'
            }
            
            if param.default == inspect.Parameter.empty:
                required_params.append(param_name)
        
        tool = Tool(
            name=name,
            description=description,
            function=func,
            parameters=parameters,
            required_params=required_params
        )
        
        self.tools[name] = tool
        print(f"🔧 工具已注册: {name} - {description}")
    
    def _get_type_name(self, type_obj) -> str:
        """获取类型名称"""
        if type_obj == str:
            return "string"
        elif type_obj == int:
            return "integer"
        elif type_obj == float:
            return "number"
        elif type_obj == bool:
            return "boolean"
        else:
            return "string"
    
    def get_tool(self, name: str) -> Optional[Tool]:
        """获取工具"""
        return self.tools.get(name)
    
    def get_available_tools(self) -> List[str]:
        """获取可用工具列表"""
        return list(self.tools.keys())
    
    def execute_tool(self, tool_name: str, params: Dict[str, Any]) -> str:
        """执行工具"""
        tool = self.get_tool(tool_name)
        if not tool:
            return f"❌ 工具 '{tool_name}' 不存在"
        
        try:
            # 检查必需参数
            for required_param in tool.required_params:
                if required_param not in params:
                    return f"❌ 缺少必需参数: {required_param}"
            
            # 执行工具函数
            result = tool.function(**params)
            return str(result)
            
        except Exception as e:
            return f"❌ 工具执行失败: {str(e)}"
    
    def find_tool_by_intent(self, intent: str) -> Optional[Tool]:
        """根据意图查找合适的工具"""
        intent_lower = intent.lower()
        
        # 计算相关意图
        if any(keyword in intent_lower for keyword in ['计算', '加', '减', '乘', '除', 'add', 'subtract', 'multiply', 'divide']):
            if '加' in intent_lower or 'add' in intent_lower:
                return self.get_tool('add')
            elif '减' in intent_lower or 'subtract' in intent_lower:
                return self.get_tool('subtract')
            elif '乘' in intent_lower or 'multiply' in intent_lower:
                return self.get_tool('multiply')
            elif '除' in intent_lower or 'divide' in intent_lower:
                return self.get_tool('divide')
        
        # 翻译相关意图
        elif any(keyword in intent_lower for keyword in ['翻译', 'translate']):
            return self.get_tool('translate')
        
        # 时间相关意图
        elif any(keyword in intent_lower for keyword in ['时间', '日期', 'time', 'date']):
            if '日期' in intent_lower or 'date' in intent_lower:
                return self.get_tool('get_current_date')
            else:
                return self.get_tool('get_current_time')
        
        # 文本分析相关意图
        elif any(keyword in intent_lower for keyword in ['统计', '计数', 'count', 'analyze']):
            if '字母' in intent_lower or 'letter' in intent_lower:
                return self.get_tool('count_letters')
            elif '单词' in intent_lower or 'word' in intent_lower:
                return self.get_tool('word_count')
        
        return None
    
    def get_tool_info(self, tool_name: str) -> str:
        """获取工具信息"""
        tool = self.get_tool(tool_name)
        if not tool:
            return f"工具 '{tool_name}' 不存在"
        
        info = f"工具: {tool.name}\n"
        info += f"描述: {tool.description}\n"
        info += f"参数: {tool.parameters}\n"
        info += f"必需参数: {tool.required_params}"
        
        return info 