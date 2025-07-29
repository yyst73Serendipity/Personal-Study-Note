"""
规划模块
负责制定执行计划和任务分解
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from .reasoning import ReasoningResult

@dataclass
class ExecutionStep:
    """执行步骤"""
    step_id: int
    description: str
    action: str
    parameters: Dict[str, Any]
    dependencies: List[int]
    estimated_time: float

@dataclass
class ExecutionPlan:
    """执行计划"""
    steps: List[ExecutionStep]
    total_estimated_time: float
    priority: str
    fallback_plan: Optional['ExecutionPlan']

class PlanningModule:
    """规划模块"""
    
    def __init__(self):
        # 任务复杂度评估
        self.complexity_thresholds = {
            'simple': 1,      # 单个工具调用
            'medium': 2,      # 2-3个工具调用
            'complex': 3      # 3个以上工具调用
        }
        
        # 工具执行时间估算
        self.tool_execution_times = {
            'add': 0.1,
            'subtract': 0.1,
            'multiply': 0.1,
            'divide': 0.1,
            'translate': 1.0,
            'get_current_time': 0.05,
            'get_current_date': 0.05,
            'count_letters': 0.2,
            'word_count': 0.2
        }
    
    def create_plan(self, reasoning_result: ReasoningResult) -> ExecutionPlan:
        """创建执行计划"""
        steps = []
        
        # 1. 验证推理结果
        validation_step = ExecutionStep(
            step_id=1,
            description="验证推理结果",
            action="validate",
            parameters={"reasoning_result": reasoning_result},
            dependencies=[],
            estimated_time=0.05
        )
        steps.append(validation_step)
        
        # 2. 准备工具执行
        if reasoning_result.selected_tool:
            tool_step = ExecutionStep(
                step_id=2,
                description=f"执行工具: {reasoning_result.selected_tool}",
                action="execute_tool",
                parameters={
                    "tool_name": reasoning_result.selected_tool,
                    "parameters": reasoning_result.tool_parameters
                },
                dependencies=[1],
                estimated_time=self.tool_execution_times.get(reasoning_result.selected_tool, 0.5)
            )
            steps.append(tool_step)
        
        # 3. 生成回复
        response_step = ExecutionStep(
            step_id=3,
            description="生成回复",
            action="generate_response",
            parameters={
                "intent": reasoning_result.intent,
                "tool_result": None,  # 将在执行时填充
                "suggested_response": reasoning_result.suggested_response
            },
            dependencies=[2] if reasoning_result.selected_tool else [1],
            estimated_time=0.1
        )
        steps.append(response_step)
        
        # 计算总时间
        total_time = sum(step.estimated_time for step in steps)
        
        # 确定优先级
        priority = self._determine_priority(reasoning_result)
        
        # 创建备用计划
        fallback_plan = self._create_fallback_plan(reasoning_result)
        
        return ExecutionPlan(
            steps=steps,
            total_estimated_time=total_time,
            priority=priority,
            fallback_plan=fallback_plan
        )
    
    def _determine_priority(self, reasoning_result: ReasoningResult) -> str:
        """确定执行优先级"""
        confidence = reasoning_result.confidence
        
        if confidence >= 0.8:
            return "high"
        elif confidence >= 0.5:
            return "medium"
        else:
            return "low"
    
    def _create_fallback_plan(self, reasoning_result: ReasoningResult) -> Optional[ExecutionPlan]:
        """创建备用计划"""
        # 如果置信度较低，创建备用计划
        if reasoning_result.confidence < 0.5:
            fallback_steps = [
                ExecutionStep(
                    step_id=1,
                    description="请求用户澄清",
                    action="clarify",
                    parameters={
                        "original_intent": reasoning_result.intent,
                        "confidence": reasoning_result.confidence
                    },
                    dependencies=[],
                    estimated_time=0.1
                )
            ]
            
            return ExecutionPlan(
                steps=fallback_steps,
                total_estimated_time=0.1,
                priority="low",
                fallback_plan=None
            )
        
        return None
    
    def decompose_complex_task(self, reasoning_result: ReasoningResult) -> List[ExecutionPlan]:
        """分解复杂任务"""
        plans = []
        
        # 如果任务需要多个工具，分解为子计划
        if reasoning_result.intent == 'calculator' and 'operation' in reasoning_result.tool_parameters:
            operation = reasoning_result.tool_parameters['operation']
            
            # 检查是否需要多步计算
            if '+' in operation and '*' in operation:
                # 先乘法后加法
                plans.append(self._create_calculation_plan(reasoning_result, ['multiply', 'add']))
            elif '-' in operation and '/' in operation:
                # 先除法后减法
                plans.append(self._create_calculation_plan(reasoning_result, ['divide', 'subtract']))
        
        return plans
    
    def _create_calculation_plan(self, reasoning_result: ReasoningResult, operations: List[str]) -> ExecutionPlan:
        """创建计算计划"""
        steps = []
        step_id = 1
        
        for i, operation in enumerate(operations):
            step = ExecutionStep(
                step_id=step_id,
                description=f"执行{operation}操作",
                action=f"execute_{operation}",
                parameters={
                    "operation": operation,
                    "parameters": reasoning_result.tool_parameters
                },
                dependencies=[step_id - 1] if i > 0 else [],
                estimated_time=self.tool_execution_times.get(operation, 0.1)
            )
            steps.append(step)
            step_id += 1
        
        total_time = sum(step.estimated_time for step in steps)
        
        return ExecutionPlan(
            steps=steps,
            total_estimated_time=total_time,
            priority="medium",
            fallback_plan=None
        )
    
    def optimize_plan(self, plan: ExecutionPlan) -> ExecutionPlan:
        """优化执行计划"""
        # 并行化独立步骤
        optimized_steps = []
        step_id_map = {}
        
        for step in plan.steps:
            # 如果没有依赖，可以并行执行
            if not step.dependencies:
                optimized_steps.append(step)
                step_id_map[step.step_id] = len(optimized_steps)
            else:
                # 更新依赖关系
                new_dependencies = [step_id_map.get(dep, dep) for dep in step.dependencies]
                step.dependencies = new_dependencies
                optimized_steps.append(step)
                step_id_map[step.step_id] = len(optimized_steps)
        
        # 重新计算总时间（考虑并行执行）
        max_parallel_time = 0
        current_parallel_time = 0
        
        for step in optimized_steps:
            if not step.dependencies:
                current_parallel_time += step.estimated_time
            else:
                max_parallel_time = max(max_parallel_time, current_parallel_time)
                current_parallel_time = step.estimated_time
        
        max_parallel_time = max(max_parallel_time, current_parallel_time)
        
        return ExecutionPlan(
            steps=optimized_steps,
            total_estimated_time=max_parallel_time,
            priority=plan.priority,
            fallback_plan=plan.fallback_plan
        )
    
    def get_plan_summary(self, plan: ExecutionPlan) -> str:
        """获取计划摘要"""
        summary = f"📋 执行计划:\n"
        summary += f"  - 步骤数: {len(plan.steps)}\n"
        summary += f"  - 预计时间: {plan.total_estimated_time:.2f}秒\n"
        summary += f"  - 优先级: {plan.priority}\n"
        
        summary += f"\n📝 执行步骤:\n"
        for step in plan.steps:
            summary += f"  {step.step_id}. {step.description} ({step.estimated_time:.2f}s)\n"
        
        if plan.fallback_plan:
            summary += f"\n🔄 备用计划: 已准备\n"
        
        return summary
    
    def validate_plan(self, plan: ExecutionPlan) -> bool:
        """验证计划的有效性"""
        # 检查步骤依赖关系
        step_ids = {step.step_id for step in plan.steps}
        
        for step in plan.steps:
            for dep in step.dependencies:
                if dep not in step_ids:
                    return False
        
        # 检查是否有循环依赖
        visited = set()
        rec_stack = set()
        
        def has_cycle(step_id):
            visited.add(step_id)
            rec_stack.add(step_id)
            
            step = next((s for s in plan.steps if s.step_id == step_id), None)
            if step:
                for dep in step.dependencies:
                    if dep not in visited:
                        if has_cycle(dep):
                            return True
                    elif dep in rec_stack:
                        return True
            
            rec_stack.remove(step_id)
            return False
        
        for step in plan.steps:
            if step.step_id not in visited:
                if has_cycle(step.step_id):
                    return False
        
        return True 