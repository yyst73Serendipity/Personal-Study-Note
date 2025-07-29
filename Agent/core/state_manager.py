"""
状态管理器
负责管理Agent的全局状态
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from enum import Enum

class AgentState(Enum):
    """Agent状态枚举"""
    IDLE = "idle"
    PROCESSING = "processing"
    EXECUTING_TOOL = "executing_tool"
    ERROR = "error"
    WAITING_INPUT = "waiting_input"

@dataclass
class AgentStatus:
    """Agent状态信息"""
    current_state: AgentState
    session_id: str
    start_time: str
    total_interactions: int
    successful_interactions: int
    failed_interactions: int
    current_tool: Optional[str]
    last_intent: Optional[str]
    error_count: int

class StateManager:
    """状态管理器"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.status = AgentStatus(
            current_state=AgentState.IDLE,
            session_id=self._generate_session_id(),
            start_time=datetime.now().isoformat(),
            total_interactions=0,
            successful_interactions=0,
            failed_interactions=0,
            current_tool=None,
            last_intent=None,
            error_count=0
        )
        
        # 确保数据目录存在
        os.makedirs(data_dir, exist_ok=True)
        
        # 加载历史状态
        self._load_state()
    
    def _generate_session_id(self) -> str:
        """生成会话ID"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def update_state(self, new_state: AgentState, **kwargs):
        """更新状态"""
        self.status.current_state = new_state
        
        # 更新其他属性
        for key, value in kwargs.items():
            if hasattr(self.status, key):
                setattr(self.status, key, value)
        
        # 保存状态
        self._save_state()
    
    def get_current_state(self) -> AgentState:
        """获取当前状态"""
        return self.status.current_state
    
    def is_processing(self) -> bool:
        """检查是否正在处理"""
        return self.status.current_state == AgentState.PROCESSING
    
    def is_executing_tool(self) -> bool:
        """检查是否正在执行工具"""
        return self.status.current_state == AgentState.EXECUTING_TOOL
    
    def is_error_state(self) -> bool:
        """检查是否处于错误状态"""
        return self.status.current_state == AgentState.ERROR
    
    def increment_interaction(self, success: bool = True):
        """增加交互计数"""
        self.status.total_interactions += 1
        
        if success:
            self.status.successful_interactions += 1
        else:
            self.status.failed_interactions += 1
            self.status.error_count += 1
        
        self._save_state()
    
    def set_current_tool(self, tool_name: Optional[str]):
        """设置当前工具"""
        self.status.current_tool = tool_name
        if tool_name:
            self.update_state(AgentState.EXECUTING_TOOL)
        else:
            self.update_state(AgentState.IDLE)
    
    def set_last_intent(self, intent: str):
        """设置最后识别的意图"""
        self.status.last_intent = intent
    
    def get_session_info(self) -> Dict[str, Any]:
        """获取会话信息"""
        return {
            'session_id': self.status.session_id,
            'start_time': self.status.start_time,
            'current_state': self.status.current_state.value,
            'total_interactions': self.status.total_interactions,
            'success_rate': self._calculate_success_rate(),
            'current_tool': self.status.current_tool,
            'last_intent': self.status.last_intent,
            'error_count': self.status.error_count
        }
    
    def _calculate_success_rate(self) -> float:
        """计算成功率"""
        if self.status.total_interactions == 0:
            return 0.0
        return self.status.successful_interactions / self.status.total_interactions
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """获取性能指标"""
        session_duration = self._calculate_session_duration()
        
        return {
            'total_interactions': self.status.total_interactions,
            'successful_interactions': self.status.successful_interactions,
            'failed_interactions': self.status.failed_interactions,
            'success_rate': self._calculate_success_rate(),
            'error_rate': self.status.error_count / max(self.status.total_interactions, 1),
            'session_duration_minutes': session_duration,
            'interactions_per_minute': self.status.total_interactions / max(session_duration, 1)
        }
    
    def _calculate_session_duration(self) -> float:
        """计算会话持续时间（分钟）"""
        try:
            start_time = datetime.fromisoformat(self.status.start_time)
            current_time = datetime.now()
            duration = current_time - start_time
            return duration.total_seconds() / 60
        except:
            return 0.0
    
    def reset_session(self):
        """重置会话"""
        self.status = AgentStatus(
            current_state=AgentState.IDLE,
            session_id=self._generate_session_id(),
            start_time=datetime.now().isoformat(),
            total_interactions=0,
            successful_interactions=0,
            failed_interactions=0,
            current_tool=None,
            last_intent=None,
            error_count=0
        )
        self._save_state()
    
    def get_state_summary(self) -> str:
        """获取状态摘要"""
        summary = f"🤖 Agent状态摘要:\n"
        summary += f"  - 当前状态: {self.status.current_state.value}\n"
        summary += f"  - 会话ID: {self.status.session_id}\n"
        summary += f"  - 总交互: {self.status.total_interactions}\n"
        summary += f"  - 成功率: {self._calculate_success_rate():.2%}\n"
        summary += f"  - 当前工具: {self.status.current_tool or '无'}\n"
        summary += f"  - 最后意图: {self.status.last_intent or '无'}\n"
        summary += f"  - 错误次数: {self.status.error_count}\n"
        
        return summary
    
    def _save_state(self):
        """保存状态到文件"""
        try:
            # 创建可序列化的状态数据
            state_data = {
                'current_state': self.status.current_state.value,
                'session_id': self.status.session_id,
                'start_time': self.status.start_time,
                'total_interactions': self.status.total_interactions,
                'successful_interactions': self.status.successful_interactions,
                'failed_interactions': self.status.failed_interactions,
                'current_tool': self.status.current_tool,
                'last_intent': self.status.last_intent,
                'error_count': self.status.error_count
            }
            
            file_path = os.path.join(self.data_dir, "agent_state.json")
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(state_data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"⚠️  保存状态失败: {e}")
    
    def _load_state(self):
        """从文件加载状态"""
        try:
            file_path = os.path.join(self.data_dir, "agent_state.json")
            
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    state_data = json.load(f)
                
                # 恢复状态
                for key, value in state_data.items():
                    if key == 'current_state':
                        setattr(self.status, key, AgentState(value))
                    elif hasattr(self.status, key):
                        setattr(self.status, key, value)
                
                print(f"📊 已加载Agent状态")
                
        except Exception as e:
            print(f"⚠️  加载状态失败: {e}")
    
    def export_state(self) -> Dict[str, Any]:
        """导出状态数据"""
        return {
            'status': {
                'current_state': self.status.current_state.value,
                'session_id': self.status.session_id,
                'start_time': self.status.start_time,
                'total_interactions': self.status.total_interactions,
                'successful_interactions': self.status.successful_interactions,
                'failed_interactions': self.status.failed_interactions,
                'current_tool': self.status.current_tool,
                'last_intent': self.status.last_intent,
                'error_count': self.status.error_count
            },
            'performance_metrics': self.get_performance_metrics(),
            'session_info': self.get_session_info()
        }
    
    def import_state(self, state_data: Dict[str, Any]):
        """导入状态数据"""
        try:
            if 'status' in state_data:
                status_data = state_data['status']
                for key, value in status_data.items():
                    if key == 'current_state':
                        setattr(self.status, key, AgentState(value))
                    elif hasattr(self.status, key):
                        setattr(self.status, key, value)
                
                self._save_state()
                print("✅ 状态导入成功")
            
        except Exception as e:
            print(f"❌ 状态导入失败: {e}") 