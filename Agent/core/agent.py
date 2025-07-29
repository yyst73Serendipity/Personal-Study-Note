"""
Agent核心类
整合所有模块，实现完整的Agent功能
"""

from typing import Dict, Any, Optional
from .perception import PerceptionModule, ParsedInput
from .memory import MemoryModule, DialogueRecord
from .reasoning import ReasoningModule, ReasoningResult
from .planning import PlanningModule, ExecutionPlan
from .state_manager import StateManager, AgentState
from .tool_manager import ToolManager
from datetime import datetime

# 导入工具函数
from tools.calculator import add, subtract, multiply, divide
from tools.translator import translate
from tools.datetime_tool import get_current_time, get_current_date
from tools.text_analyzer import count_letters, word_count

class Agent:
    """智能Agent核心类"""
    
    def __init__(self, verbose: bool = True):
        """初始化Agent"""
        self.verbose = verbose
        
        # 初始化各个模块
        self.perception = PerceptionModule()
        self.memory = MemoryModule()
        self.reasoning = ReasoningModule()
        self.planning = PlanningModule()
        self.state_manager = StateManager()
        self.tool_manager = ToolManager()
        
        # 注册工具
        self._register_tools()
        
        if self.verbose:
            print("🤖 Agent初始化完成")
            print(f"📊 状态: {self.state_manager.get_state_summary()}")
    
    def _register_tools(self):
        """注册工具函数"""
        # 注册计算工具
        self.tool_manager.register_tool("add", "加法运算", add)
        self.tool_manager.register_tool("subtract", "减法运算", subtract)
        self.tool_manager.register_tool("multiply", "乘法运算", multiply)
        self.tool_manager.register_tool("divide", "除法运算", divide)
        
        # 注册翻译工具
        self.tool_manager.register_tool("translate", "文本翻译", translate)
        
        # 注册时间工具
        self.tool_manager.register_tool("get_current_time", "获取当前时间", get_current_time)
        self.tool_manager.register_tool("get_current_date", "获取当前日期", get_current_date)
        
        # 注册文本分析工具
        self.tool_manager.register_tool("count_letters", "统计字母", count_letters)
        self.tool_manager.register_tool("word_count", "统计单词", word_count)
        
        if self.verbose:
            print(f"🔧 已注册 {len(self.tool_manager.get_available_tools())} 个工具")
    
    def process_input(self, user_input: str) -> str:
        """处理用户输入的主方法"""
        try:
            # 更新状态为处理中
            self.state_manager.update_state(AgentState.PROCESSING)
            
            if self.verbose:
                print(f"\n🔄 开始处理用户输入: {user_input}")
            
            # 1. 感知阶段：解析用户输入
            parsed_input = self.perception.parse_input(user_input)
            
            if self.verbose:
                print(f"📝 感知结果:")
                print(f"  - 意图: {parsed_input.intent}")
                print(f"  - 置信度: {parsed_input.confidence:.2f}")
                print(f"  - 参数: {parsed_input.parameters}")
            
            # 2. 记忆阶段：获取相关历史
            recent_history = self.memory.get_recent_dialogues(5)
            
            if self.verbose:
                print(f"📚 获取到 {len(recent_history)} 条相关历史")
            
            # 3. 推理阶段：进行决策推理
            reasoning_result = self.reasoning.reason(parsed_input, recent_history)
            
            if self.verbose:
                print(f"🧠 推理结果:")
                print(f"  - 最终意图: {reasoning_result.intent}")
                print(f"  - 选择工具: {reasoning_result.selected_tool}")
                print(f"  - 工具参数: {reasoning_result.tool_parameters}")
            
            # 4. 规划阶段：制定执行计划
            execution_plan = self.planning.create_plan(reasoning_result)
            
            if self.verbose:
                print(f"📋 执行计划:")
                print(f"  - 步骤数: {len(execution_plan.steps)}")
                print(f"  - 预计时间: {execution_plan.total_estimated_time:.2f}秒")
            
            # 5. 执行阶段：执行计划
            response = self._execute_plan(execution_plan, reasoning_result)
            
            # 6. 记忆阶段：记录对话
            self._record_dialogue(user_input, parsed_input, reasoning_result, response)
            
            # 7. 更新状态
            self.state_manager.increment_interaction(success=True)
            self.state_manager.set_last_intent(reasoning_result.intent)
            self.state_manager.update_state(AgentState.IDLE)
            
            if self.verbose:
                print(f"✅ 处理完成")
            
            return response
            
        except Exception as e:
            # 错误处理
            error_msg = f"❌ 处理失败: {str(e)}"
            self.state_manager.increment_interaction(success=False)
            self.state_manager.update_state(AgentState.ERROR)
            
            if self.verbose:
                print(f"❌ 错误: {e}")
            
            return error_msg
    
    def _execute_plan(self, plan: ExecutionPlan, reasoning_result: ReasoningResult) -> str:
        """执行计划"""
        if self.verbose:
            print(f"\n⚙️  开始执行计划...")
        
        try:
            # 执行每个步骤
            for step in plan.steps:
                if self.verbose:
                    print(f"  📌 执行步骤 {step.step_id}: {step.description}")
                
                if step.action == "validate":
                    # 验证推理结果
                    if not self.reasoning.validate_reasoning(reasoning_result):
                        return "❌ 推理结果验证失败"
                
                elif step.action == "execute_tool":
                    # 执行工具
                    tool_name = step.parameters["tool_name"]
                    tool_params = step.parameters["parameters"]
                    
                    self.state_manager.set_current_tool(tool_name)
                    
                    if self.verbose:
                        print(f"    🔧 执行工具: {tool_name}")
                        print(f"    📝 参数: {tool_params}")
                    
                    tool_result = self.tool_manager.execute_tool(tool_name, tool_params)
                    
                    if self.verbose:
                        print(f"    ✅ 工具结果: {tool_result}")
                    
                    # 更新推理结果
                    reasoning_result.tool_parameters = tool_params
                    reasoning_result.suggested_response = tool_result
                
                elif step.action == "generate_response":
                    # 生成回复
                    if reasoning_result.selected_tool:
                        response = reasoning_result.suggested_response
                    else:
                        response = reasoning_result.suggested_response
                    
                    if self.verbose:
                        print(f"    💬 生成回复: {response}")
                    
                    return response
                
                elif step.action == "clarify":
                    # 请求用户澄清
                    return "🤔 我没有完全理解你的意思，请重新描述一下你的需求。"
            
            return "✅ 执行完成"
            
        except Exception as e:
            if self.verbose:
                print(f"❌ 执行失败: {e}")
            return f"❌ 执行失败: {str(e)}"
    
    def _record_dialogue(self, user_input: str, parsed_input: ParsedInput, 
                        reasoning_result: ReasoningResult, response: str):
        """记录对话"""
        record = DialogueRecord(
            timestamp=datetime.now().isoformat(),
            user_input=user_input,
            intent=reasoning_result.intent,
            confidence=reasoning_result.confidence,
            parameters=reasoning_result.tool_parameters,
            tool_used=reasoning_result.selected_tool,
            tool_result=response if reasoning_result.selected_tool else None,
            response=response,
            session_id=self.state_manager.status.session_id
        )
        
        self.memory.add_dialogue(record)
    
    def get_status(self) -> str:
        """获取Agent状态"""
        return self.state_manager.get_state_summary()
    
    def get_performance(self) -> Dict[str, Any]:
        """获取性能指标"""
        return self.state_manager.get_performance_metrics()
    
    def get_memory_summary(self) -> str:
        """获取记忆摘要"""
        context = self.memory.get_context_summary()
        return f"📚 记忆摘要:\n" \
               f"  - 总对话数: {context['total_dialogues']}\n" \
               f"  - 会话ID: {context['session_id']}\n" \
               f"  - 最近意图: {context['recent_intents']}\n" \
               f"  - 常用工具: {context['frequently_used_tools']}"
    
    def get_reasoning_explanation(self, user_input: str) -> str:
        """获取推理过程解释"""
        # 重新执行推理过程以获取解释
        parsed_input = self.perception.parse_input(user_input)
        recent_history = self.memory.get_recent_dialogues(5)
        reasoning_result = self.reasoning.reason(parsed_input, recent_history)
        
        return self.reasoning.get_reasoning_explanation(reasoning_result)
    
    def reset(self):
        """重置Agent"""
        self.state_manager.reset_session()
        self.memory.clear_history()
        
        if self.verbose:
            print("🔄 Agent已重置")
    
    def get_available_tools(self) -> list:
        """获取可用工具列表"""
        return self.tool_manager.get_available_tools()
    
    def get_tool_info(self, tool_name: str) -> str:
        """获取工具信息"""
        return self.tool_manager.get_tool_info(tool_name)
    
    def export_data(self) -> Dict[str, Any]:
        """导出Agent数据"""
        return {
            'state': self.state_manager.export_state(),
            'memory': self.memory.get_statistics(),
            'performance': self.get_performance()
        } 