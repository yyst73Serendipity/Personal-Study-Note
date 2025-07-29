"""
计算器工具模块
提供数学计算功能
"""

from typing import Union, Dict, Any

class Calculator:
    """计算器类"""
    
    def __init__(self):
        self.supported_operations = {
            'add': self.add,
            'subtract': self.subtract,
            'multiply': self.multiply,
            'divide': self.divide
        }
    
    def add(self, a: Union[int, float], b: Union[int, float]) -> str:
        """加法运算"""
        try:
            result = float(a) + float(b)
            return f"{a} + {b} = {result}"
        except (ValueError, TypeError) as e:
            return f"❌ 加法计算失败: {e}"
    
    def subtract(self, a: Union[int, float], b: Union[int, float]) -> str:
        """减法运算"""
        try:
            result = float(a) - float(b)
            return f"{a} - {b} = {result}"
        except (ValueError, TypeError) as e:
            return f"❌ 减法计算失败: {e}"
    
    def multiply(self, a: Union[int, float], b: Union[int, float]) -> str:
        """乘法运算"""
        try:
            result = float(a) * float(b)
            return f"{a} × {b} = {result}"
        except (ValueError, TypeError) as e:
            return f"❌ 乘法计算失败: {e}"
    
    def divide(self, a: Union[int, float], b: Union[int, float]) -> str:
        """除法运算"""
        try:
            if float(b) == 0:
                return "❌ 除数不能为零"
            result = float(a) / float(b)
            return f"{a} ÷ {b} = {result}"
        except (ValueError, TypeError) as e:
            return f"❌ 除法计算失败: {e}"
    
    def calculate(self, expression: str) -> str:
        """计算表达式"""
        try:
            # 简单的表达式解析
            expression = expression.replace('×', '*').replace('÷', '/')
            result = eval(expression)
            return f"{expression} = {result}"
        except Exception as e:
            return f"❌ 表达式计算失败: {e}"
    
    def get_supported_operations(self) -> Dict[str, str]:
        """获取支持的操作"""
        return {
            'add': '加法运算',
            'subtract': '减法运算', 
            'multiply': '乘法运算',
            'divide': '除法运算'
        }
    
    def validate_parameters(self, operation: str, params: Dict[str, Any]) -> bool:
        """验证参数"""
        if operation not in self.supported_operations:
            return False
        
        required_params = ['a', 'b']
        for param in required_params:
            if param not in params:
                return False
            
            try:
                float(params[param])
            except (ValueError, TypeError):
                return False
        
        return True
    
    def execute(self, operation: str, params: Dict[str, Any]) -> str:
        """执行计算操作"""
        if not self.validate_parameters(operation, params):
            return "❌ 参数验证失败"
        
        if operation in self.supported_operations:
            return self.supported_operations[operation](params['a'], params['b'])
        else:
            return f"❌ 不支持的操作: {operation}"

# 创建全局计算器实例
calculator = Calculator()

# 工具函数接口
def add(a: Union[int, float], b: Union[int, float]) -> str:
    """加法工具函数"""
    return calculator.add(a, b)

def subtract(a: Union[int, float], b: Union[int, float]) -> str:
    """减法工具函数"""
    return calculator.subtract(a, b)

def multiply(a: Union[int, float], b: Union[int, float]) -> str:
    """乘法工具函数"""
    return calculator.multiply(a, b)

def divide(a: Union[int, float], b: Union[int, float]) -> str:
    """除法工具函数"""
    return calculator.divide(a, b) 