from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict
import os 
from tool import ToolExecutor
from search import search
from LLM import agent_LLM
import re

REACT_PROMPT_TEMPLATE = """
请注意，你是一个有能力调用外部工具的耐药菌诊疗智能助手。

可用工具如下:
{tools} #调用serpapi在google上进行搜索
你必须严格按下面的纯文本格式回复，禁止使用任何 XML/JSON/函数调用语法,请严格按照以下格式进行回应:


Thought: 你的思考过程，用于分析问题、拆解任务和规划下一步行动。

Action: 你决定采取的行动，必须是以下格式之一:
- `{{tool_name}}[{{tool_input}}]`:调用一个可用工具。
- `Finish[最终答案]`:当你认为已经获得最终答案时。
- 当你收集到足够的信息，能够回答用户的最终问题时，你必须在Action:字段后使用 Finish[最终答案] 来输出最终答案。

现在，请开始解决以下问题:
Question: {question}
History: {history}
"""

class ReAct:
    def __init__(self, llm_client: agent_LLM, toolexecutor: ToolExecutor, max_step: int = 5):
        self.llm_client = llm_client
        self.toolexecutor = toolexecutor
        self.max_step = max_step

    def run(self, question: str):
        self.history = []
        current_step = 0

        while current_step <= self.max_step:
            current_step += 1
            print(f"执行第{current_step}步")

            # 1. 构造本轮 prompt
            tool_use = self.toolexecutor.getAvailableTools()
            history_new = "\n".join(self.history)

            prompt = REACT_PROMPT_TEMPLATE.format(
                tools=tool_use,
                question=question,
                history=history_new,
            )

            messages = [{"role": "user", "content": prompt}]

            # 2. 调用 LLM
            response_text = self.llm_client.think(messages=messages)
            if not response_text:
                print("LLM没发生响应")
                break

            # 3. 解析 LLM 输出
            thought, action = self._parse_output(response_text)

            if thought:
                print(f"思考: {thought}")

            if not action:
                print("警告:未能解析出有效的Action，流程终止。")
                break

            # 4. 执行 Action
            if action.startswith("Finish"):
                m = re.match(r"Finish\[(.*)\]", action, re.DOTALL)   # ✅ 加 re.DOTALL
                if m:
                    final_answer = m.group(1).strip()
                    print(f"🎉 最终答案: {final_answer}")
                    return final_answer
                else:
                    print("警告：Finish 格式解析失败")
                    break

            tool_name, tool_input = self._parse_action(action)
            if not tool_name or not tool_input:
                # ... 处理无效Action格式 ...
                continue

            print(f"🎬 行动: {tool_name}[{tool_input}]")

            tool_function = self.toolexecutor.getTool(tool_name)
            if not tool_function:
                observation = f"错误:未找到名为 '{tool_name}' 的工具。"
            else:
                observation = tool_function(tool_input)  # 调用真实工具
                print(f"👀 观察: {observation}")

            # 将本轮的Action和Observation添加到历史记录中
            self.history.append(f"Action: {action}")
            self.history.append(f"Observation: {observation}")

        # 循环结束
        print("已达到最大步数，流程终止。")
        return None

    def _parse_output(self, text: str):
        """解析LLM的输出，提取Thought和Action。
        """
        # Thought: 匹配到 Action: 或文本末尾
        thought_match = re.search(r"Thought:\s*(.*?)(?=\nAction:|$)", text, re.DOTALL)
        # Action: 匹配到文本末尾
        action_match = re.search(r"Action:\s*(.*?)$", text, re.DOTALL)
        thought = thought_match.group(1).strip() if thought_match else None
        action = action_match.group(1).strip() if action_match else None
        return thought, action

    def _parse_action(self, action_text: str):
        """解析Action字符串，提取工具名称和输入。
        """
        match = re.match(r"(\w+)\[(.*)\]", action_text, re.DOTALL)
        if match:
            return match.group(1), match.group(2)
        return None, None

if __name__ == "__main__":
    llm = agent_LLM()
    executor = ToolExecutor()

    while True:
        question = input("\n请输入问题（输入 q 退出）：").strip()
        if question.lower() in ("q", "quit", "exit"):
            break
        if not question:
            continue

        agent = ReAct(llm, executor)
        answer = agent.run(question)
        file_name="ReAct_output.txt"
        with open(file_name,'w',encoding="utf-8") as file_obj:
            file_obj.write(answer)
        print(f"\n📝 答案：{answer}")