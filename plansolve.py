
from LLM import agent_LLM
import re
import ast

PLANNER_PROMPT_TEMPLATE = """
你是一个顶级的AI规划专家。你的任务是将用户提出的复杂问题分解成一个由多个简单步骤组成的行动计划。
请确保计划中的每个步骤都是一个独立的、可执行的子任务，并且严格按照逻辑顺序排列。
你的输出必须是一个Python列表，其中每个元素都是一个描述子任务的字符串。

问题: {question}

请严格按照以下格式输出你的计划,```python与```作为前后缀是必要的:
```python
["步骤1", "步骤2", "步骤3", ...]
```
"""

EXECUTOR_PROMPT_TEMPLATE = """
你是一位顶级的AI执行专家。你的任务是严格按照给定的计划，一步步地解决问题。
你将收到原始问题、完整的计划、以及到目前为止已经完成的步骤和结果。
请你专注于解决“当前步骤”，并仅输出该步骤的最终答案，不要输出任何额外的解释或对话。

# 原始问题:
{question}

# 完整计划:
{plan}

# 历史步骤与结果:
{history}

# 当前步骤:
{current_step}

请仅输出针对“当前步骤”的回答:
"""

class plan_and_solve():
    def __init__(self,llm_client:agent_LLM):
        self.llm_client=llm_client



    def plan(self,question:str):
        #1:构造提示词
        prompt=PLANNER_PROMPT_TEMPLATE.format(question=question)
        messages = [{"role": "user", "content": prompt}]
        #2：调用LLM
        response_text=self.llm_client.think(messages=messages) or ""
        plan_str=self._parse_plan_output(response_text)
        print(f"解析后的内容{plan_str}")
        return plan_str

    def _parse_plan_output(self, response_text: str):
        match =re.search(r"```python\s*(.*?)```", response_text, re.DOTALL)
        if not match:
            return []
        plan_str= match.group(1).strip() if match else None
        try:
            plan = ast.literal_eval(plan_str)
        except(SyntaxError,ValueError):
            return []
        return plan_str,plan if isinstance(plan, list) else []

    def solve(self,question,plan):
        history=""
        for i,step in enumerate(plan):
        #1 :构造提示词
            prompt=EXECUTOR_PROMPT_TEMPLATE.format(question=question,
                                               plan=plan,
                                               history=history,
                                               current_step=step)

            messages = [{"role": "user", "content": prompt}]
        #2:调用大模型
            response_text = self.llm_client.think(messages=messages) or ""
            history += f"当前第{i+1}:{step}\n结果:{response_text}\n\n"
        final_answer = response_text
        return final_answer

class plan_and_solve_agent():
    def __init__(self,llm_client:agent_LLM,):
        self.llm_client = llm_client
        self.plan_and_solve =plan_and_solve(llm_client)

    def run(self,question:str):
        #1:调用plan规划器
        plan=self.plan_and_solve.plan(question)
        #检查计划是否正确生成
        if not plan:
            print("计划未正确生成")
            return []
        #调用执行求解器进行方案输出
        execute=self.plan_and_solve.solve(question,plan)
        print(f"最终答案{execute}")
        return execute
if __name__ == "__main__":
    llm=agent_LLM()
    agent=plan_and_solve_agent(llm)  
    while True:
        question = input("\n请输入问题（输入 q 退出）：").strip()
        if question.lower() in ("q", "quit", "exit"):
            break
        if not question:
            continue

        answer = agent.run(question)

        file_name="plan_and_solve_output.txt"
        with open(file_name,'a',encoding="utf-8") as file_obj:
            file_obj.write(f"问题：{question}\n"
                            f"回答：{answer}\n\n")
        




        