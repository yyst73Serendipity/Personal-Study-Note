#!/usr/bin/env python3
"""
Agent系统测试脚本
"""

from core.agent import Agent

def test_agent():
    """测试Agent功能"""
    print("🧪 开始测试Agent系统...")
    
    # 初始化Agent
    agent = Agent(verbose=True)
    
    # 测试用例
    test_cases = [
        "你好",
        "2+3等于多少？",
        "现在几点了？",
        "今天是几号？",
        "统计'hello world'中字母o的数量",
        "翻译'hello'",
        "exit"
    ]
    
    print("\n📋 测试用例:")
    for i, test_case in enumerate(test_cases, 1):
        print(f"  {i}. {test_case}")
    
    print("\n🚀 开始执行测试...")
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n{'='*50}")
        print(f"测试 {i}: {test_input}")
        print(f"{'='*50}")
        
        if test_input == "exit":
            print("✅ 测试完成")
            break
        
        try:
            response = agent.process_input(test_input)
            print(f"✅ 测试通过: {response}")
        except Exception as e:
            print(f"❌ 测试失败: {e}")
    
    # 显示系统状态
    print(f"\n📊 系统状态:")
    print(agent.get_status())
    
    print(f"\n📚 记忆摘要:")
    print(agent.get_memory_summary())

if __name__ == "__main__":
    test_agent() 