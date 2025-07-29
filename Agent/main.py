#!/usr/bin/env python3
"""
从0到1实现的智能Agent系统
具备感知、记忆、推理、规划、工具调用等完整功能
"""

from core.agent import Agent
from utils.config import Config

def main():
    """主函数"""
    print("🤖 智能Agent系统启动中...")
    
    # 初始化Agent
    agent = Agent()
    
    print("✅ Agent初始化完成！")
    print("💡 支持功能：计算、翻译、时间查询、文本分析等")
    print("💡 输入 'exit' 退出系统")
    print("-" * 50)
    
    # 交互循环
    while True:
        try:
            # 获取用户输入
            user_input = input("\033[94m用户: \033[0m")
            
            # 检查退出命令
            if user_input.lower() in ['exit', 'quit', '退出']:
                print("\033[93m👋 感谢使用智能Agent系统！\033[0m")
                break
            
            # 处理用户输入
            if user_input.strip():
                print("\033[92mAgent: \033[0m", end="")
                response = agent.process_input(user_input)
                print(response)
            else:
                print("\033[93m⚠️  请输入有效内容\033[0m")
                
        except KeyboardInterrupt:
            print("\n\033[93m👋 系统已退出\033[0m")
            break
        except Exception as e:
            print(f"\033[91m❌ 系统错误: {e}\033[0m")

if __name__ == "__main__":
    main() 


#   D:\ProgramFiles\Python\Python3129\python.exe -u "d:\Code\python-workspace\Agent\main.py"
