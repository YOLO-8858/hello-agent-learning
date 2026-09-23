from LLM import agent_LLM
from typing import List, Dict, Any, Optional
INITIAL_PROMPT_TEMPLATE = """
你是一位资深的Python程序员。请根据以下要求，编写一个Python函数。
你的代码必须包含完整的函数签名、文档字符串，并遵循PEP 8编码规范。

要求: {task}

请直接输出代码，不要包含任何额外的解释。
"""

REFLECT_PROMPT_TEMPLATE = """
你是一位极其严格的代码评审专家和资深算法工程师，对代码的性能有极致的要求。
你的任务是审查以下Python代码，并专注于找出其在<strong>算法效率</strong>上的主要瓶颈。

# 原始任务:
{task}

# 待审查的代码:
```python
{code}
```

请分析该代码的时间复杂度，并思考是否存在一种<strong>算法上更优</strong>的解决方案来显著提升性能。
如果存在，请清晰地指出当前算法的不足，并提出具体的、可行的改进算法建议（例如，使用筛法替代试除法）。
如果代码在算法层面已经达到最优，才能回答“无需改进”。

请直接输出你的反馈，不要包含任何额外的解释。

"""

REFINE_PROMPT_TEMPLATE = """
你是一位资深的Python程序员。你正在根据一位代码评审专家的反馈来优化你的代码。

# 原始任务:
{task}

# 你上一轮尝试的代码:
{last_code_attempt}
评审员的反馈：
{feedback}

请根据评审员的反馈，生成一个优化后的新版本代码。
你的代码必须包含完整的函数签名、文档字符串，并遵循PEP 8编码规范。
请直接输出优化后的代码，不要包含任何额外的解释。
"""

class Memory:
    def __init__(self,):
        self.records: List[Dict[str, Any]] = []
    def add_record(self,record_type:str,record_content:str):

        record={"type":record_type,"content":record_content}
        self.records.append(record)
        print(f"新增一条记录{record_type}")

    def get_trajectory(self)-> str:
        trajectory = []

        for record in self.record:
            if record['type']=="execute":
                trajectory.append(f"上一轮尝试的代码{record["content"]}")
            if record['type']=="reflection":
                trajectory.append(f"上一轮的反馈{record["content"]}")

        return "\n\n".join(trajectory)

    def get_last_execution(self,)->Optional[str]:

        for record in reversed(self.records):
            if record['type'] =="execute":
                return record['content']
        return None

class MemoryAgent:
    def __init__(self,llm_client:agent_LLM,max_i:int=3):
        self.llm_client=llm_client
        self.max_i=max_i
        self.Memory=Memory()

    def run(self,task:str):
        #初始执行
        initial_prompt=INITIAL_PROMPT_TEMPLATE.format(task=task)
        message=[{"role":"user","content":initial_prompt}]
        initial_code=self.llm_client.think(messages=message)
        self.Memory.add_record("execute",initial_code)
        #迭代循环:反思与优化
        for i in range(self.max_i):
            print(f"第{i+1}次执行迭代循环")
        # a. 反思
            last_code=self.Memory.get_last_execution()
            reflect_prompt=REFLECT_PROMPT_TEMPLATE.format(task=task,code=last_code)
            message=[{"role":"user","content":reflect_prompt}]
            feedback=self.llm_client.think(messages=message)
            self.Memory.add_record("reflection",feedback)

        # b. 检查是否需要停止
            if "无需改进" in feedback:
                print("任务完成")
            break
        # c. 优化
        refine_prompt=REFINE_PROMPT_TEMPLATE.format(task=task,last_code_attempt=last_code,feedback=feedback)

        message=[{"role":"user","content":refine_prompt}]

        refine_code=self.llm_client.think(messages=message)

        self.Memory.add_record("execute",refine_code)

        final_code = self.Memory.get_last_execution()

        return final_code

if __name__ =="__main__":
    llm=agent_LLM()
    
    while True:
        task = input("\n请输入问题（输入 q 退出）：").strip()
        if task.lower() in ("q", "quit", "exit"):
            break
        if not task:
            continue

        agent = MemoryAgent(llm)
        answer = agent.run(task)
        file_name="Memory_output.txt"
        with open(file_name,'w',encoding="utf-8") as file_obj:
            file_obj.write(answer)