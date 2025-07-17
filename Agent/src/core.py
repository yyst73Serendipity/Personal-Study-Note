from openai import OpenAI
import json
from typing import List, Dict, Any
from src.utils import function_to_json
from src.tools import get_current_datetime, mul, add, compare, count_letter_in_string, translate

import pprint

SYSREM_PROMPT = """
你是一个叫“一定会幸运的”的人工智能助手。你的输出应该与用户的语言保持一致。
当用户的问题需要调用工具时，你可以从提供的工具列表中调用适当的工具函数。
"""

class Agent:
    def __init__(self, client: OpenAI, model: str = "deepseek-chat", tools: List=[], verbose : bool = True):
        self.client = client
        self.tools = tools
        self.model = model
        self.messages = [
            {"role": "system", "content": SYSREM_PROMPT},
        ]
        self.verbose = verbose

    def get_tool_schema(self) -> List[Dict[str, Any]]:
        # 获取所有工具的 JSON 模式
        return [function_to_json(tool) for tool in self.tools]

    def handle_tool_call(self, tool_call):
        # 处理工具调用
        function_name = tool_call.function.name
        function_args = tool_call.function.arguments
        function_id = tool_call.id

        # 解析参数字符串为字典
        args_dict = json.loads(function_args)
        # 动态调用函数
        function_call_content = eval(f"{function_name}(**args_dict)")

        return {
            "role": "tool",
            "content": str(function_call_content),
            "tool_call_id": function_id,
        }

    def get_completion(self, prompt) -> str:
        self.messages.append({"role": "user", "content": prompt})

        # 第一次请求模型，可能会返回 tool_calls
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            tools=self.get_tool_schema(),
            stream=False,
        )
        message = response.choices[0].message

        # 如果 assistant 需要调用工具
        if message.tool_calls:
            # 先把 assistant 消息（带 tool_calls）加入历史
            assistant_message = {
                "role": "assistant",
                "content": message.content,
                "tool_calls": message.tool_calls,
            }
            self.messages.append(assistant_message)

            # 依次处理每个工具调用，加入 tool 消息
            for tool_call in message.tool_calls:
                tool_result = self.handle_tool_call(tool_call)
                self.messages.append(tool_result)

            if self.verbose:
                tool_list = [[tc.function.name, tc.function.arguments] for tc in message.tool_calls]
                print("调用工具：", message.content, tool_list)

            # 再次请求 assistant，获取最终回复
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                tools=self.get_tool_schema(),
                stream=False,
            )
            message = response.choices[0].message
            self.messages.append({"role": "assistant", "content": message.content})
            return message.content
        else:
            # 没有工具调用，直接返回
            self.messages.append({"role": "assistant", "content": message.content})
            return message.content


    

