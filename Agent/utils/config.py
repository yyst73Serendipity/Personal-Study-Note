"""
配置管理模块
负责管理Agent的配置参数
"""

import json
import os
from typing import Dict, Any, Optional

class Config:
    """配置管理类"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self._load_default_config()
        self._load_config()
    
    def _load_default_config(self) -> Dict[str, Any]:
        """加载默认配置"""
        return {
            "agent": {
                "name": "智能助手",
                "version": "1.0.0",
                "verbose": True,
                "max_history": 50
            },
            "memory": {
                "max_dialogues": 100,
                "data_dir": "data"
            },
            "tools": {
                "enable_calculator": True,
                "enable_translator": True,
                "enable_datetime": True,
                "enable_text_analyzer": True
            },
            "reasoning": {
                "confidence_threshold": 0.3,
                "max_reasoning_steps": 5
            },
            "planning": {
                "max_plan_steps": 10,
                "timeout_seconds": 30
            },
            "logging": {
                "level": "INFO",
                "file": "agent.log"
            }
        }
    
    def _load_config(self):
        """加载配置文件"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                
                # 递归合并配置
                self._merge_config(self.config, user_config)
                print(f"✅ 已加载配置文件: {self.config_file}")
            else:
                # 创建默认配置文件
                self.save_config()
                print(f"📝 已创建默认配置文件: {self.config_file}")
                
        except Exception as e:
            print(f"⚠️  加载配置文件失败: {e}")
    
    def _merge_config(self, base: Dict[str, Any], update: Dict[str, Any]):
        """递归合并配置"""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any):
        """设置配置值"""
        keys = key.split('.')
        config = self.config
        
        # 导航到父级
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # 设置值
        config[keys[-1]] = value
    
    def save_config(self):
        """保存配置到文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            print(f"✅ 配置已保存到: {self.config_file}")
        except Exception as e:
            print(f"❌ 保存配置失败: {e}")
    
    def get_agent_config(self) -> Dict[str, Any]:
        """获取Agent配置"""
        return self.config.get("agent", {})
    
    def get_memory_config(self) -> Dict[str, Any]:
        """获取记忆模块配置"""
        return self.config.get("memory", {})
    
    def get_tools_config(self) -> Dict[str, Any]:
        """获取工具配置"""
        return self.config.get("tools", {})
    
    def get_reasoning_config(self) -> Dict[str, Any]:
        """获取推理模块配置"""
        return self.config.get("reasoning", {})
    
    def get_planning_config(self) -> Dict[str, Any]:
        """获取规划模块配置"""
        return self.config.get("planning", {})
    
    def get_logging_config(self) -> Dict[str, Any]:
        """获取日志配置"""
        return self.config.get("logging", {})
    
    def is_tool_enabled(self, tool_name: str) -> bool:
        """检查工具是否启用"""
        tools_config = self.get_tools_config()
        return tools_config.get(f"enable_{tool_name}", True)
    
    def get_config_summary(self) -> str:
        """获取配置摘要"""
        summary = "⚙️  配置摘要:\n"
        
        # Agent配置
        agent_config = self.get_agent_config()
        summary += f"  🤖 Agent: {agent_config.get('name', 'Unknown')} v{agent_config.get('version', 'Unknown')}\n"
        summary += f"  📊 详细模式: {'开启' if agent_config.get('verbose', True) else '关闭'}\n"
        
        # 工具配置
        tools_config = self.get_tools_config()
        enabled_tools = [tool for tool, enabled in tools_config.items() if enabled and tool.startswith('enable_')]
        summary += f"  🛠️  启用工具: {len(enabled_tools)} 个\n"
        
        # 记忆配置
        memory_config = self.get_memory_config()
        summary += f"  📚 最大对话数: {memory_config.get('max_dialogues', 100)}\n"
        
        # 推理配置
        reasoning_config = self.get_reasoning_config()
        summary += f"  🧠 置信度阈值: {reasoning_config.get('confidence_threshold', 0.3)}\n"
        
        return summary
    
    def validate_config(self) -> bool:
        """验证配置有效性"""
        try:
            # 检查必需配置
            required_sections = ['agent', 'memory', 'tools', 'reasoning', 'planning']
            for section in required_sections:
                if section not in self.config:
                    print(f"❌ 缺少配置节: {section}")
                    return False
            
            # 检查Agent配置
            agent_config = self.get_agent_config()
            if 'name' not in agent_config:
                print("❌ 缺少Agent名称配置")
                return False
            
            # 检查记忆配置
            memory_config = self.get_memory_config()
            if memory_config.get('max_dialogues', 0) <= 0:
                print("❌ 最大对话数必须大于0")
                return False
            
            # 检查推理配置
            reasoning_config = self.get_reasoning_config()
            confidence = reasoning_config.get('confidence_threshold', 0.3)
            if not 0 <= confidence <= 1:
                print("❌ 置信度阈值必须在0-1之间")
                return False
            
            print("✅ 配置验证通过")
            return True
            
        except Exception as e:
            print(f"❌ 配置验证失败: {e}")
            return False 