from src.core import Agent
from src.tools import add, mul,count_letter_in_string, compare, get_current_datetime, translate

from openai import OpenAI 


if __name__ == "__main__":
    client = OpenAI(
        api_key="sk-38a3841b59f54827985607837f6d91ec",
        base_url="https://api.deepseek.com",
    )

    agent = Agent(
        client=client,
        # model="Qwen/Qwen2.5-32B-Instruct",
        model="deepseek-chat",
        tools=[get_current_datetime, add, mul, compare, count_letter_in_string, translate],
    )

    while True:
        # 使用彩色输出区分用户输入和AI回答
        prompt = input("\033[94mUser: \033[0m")  # 蓝色显示用户输入提示
        if prompt == "exit":
            break
        response = agent.get_completion(prompt)
        print("\033[92mAssistant: \033[0m", response)  # 绿色显示AI助手回答


# D:\ProgramFiles\Python\Python3129\python.exe -u "d:\Code\python-workspace\Agent\demo.py"