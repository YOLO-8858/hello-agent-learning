1.封装LLM的函数，没用过流式输出，重新手搓了一遍示例中给的LLM的封装，代码如下
# LLM流式输出封装代码
```python
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict
import os 

load_dotenv()

class agent_LLM():
    def __init__(self,model:str=None,apikey:str=None,baseurl:str=None,timeout:int=None):
        self.model=model or os.getenv("LLM_MODEL_ID")
        self.apikey = apikey or os.getenv("LLM_API_KEY")
        self.baseurl = baseurl or os.getenv("LLM_BASE_URL")
        self.timeout = timeout or int(os.getenv("TIMEOUT"))

        if not all([self.model,self.apikey,self.baseurl]):
            raise ValueError("模型ID，api_key和调用地址必须提供在.env文件中")

        self.client=OpenAI(api_key=self.apikey,base_url=self.baseurl,timeout=self.timeout)

    def think(self, messages: List[Dict[str, str]], temperature: float = 0) -> str:
        try:
            response=self.client.chat.completions.create(model=self.model,messages=messages,
                                                         temperature=temperature,stream=True)
            print("LLM响应成功")
            collect_content=[]
            for chunk in response:
                if not chunk.choices:
                    continue
                content=chunk.choices[0].delta.content or""
                print(content,end="",flush=True)
                collect_content.append(content)
            print()
            return "".join(collect_content)
        except Exception as e:
            print(f"LLMapi调用失败发生错误{e}")
            return
        
if __name__ =='__main__':
    try:
        llmClient = agent_LLM()
        examplemessage=[{"role": "system", "content": "You are a helpful assistant who can written python code"},
        {"role": "user", "content": "帮我完成一个简易的计算器代码"},]

        responseText = llmClient.think(examplemessage)
        if responseText:
            print(responseText)

    except Exception as e:
        print(e)
# output - task4.output.txt

(agent) PS D:\hello-agents-main> & "C:/Users/Changbiao Xie/.conda/envs/agent/python.exe" d:/hello-agents-main/task/LLM.py
LLM响应成功
这是一个可直接运行的简易计算器 Python 代码，支持四则运算，并包含基本的错误提示。
```python
def calculate(num1, op, num2):
    """执行四则运算"""
    if op == '+':
        return num1 + num2
    elif op == '-':
        return num1 - num2
    elif op == '*':
        return num1 * num2
    elif op == '/':
        if num2 == 0:
            raise ZeroDivisionError("除数不能为 0")
        return num1 / num2
    else:
        raise ValueError(f"不支持的运算符：{op}")


def main():
    print("===== 简易计算器 =====")
    print("支持的运算：+  -  *  /")
    print("输入格式：数字 运算符 数字（例如 3 + 5）")
    print("输入 q 退出程序\n")

    while True:
        expr = input("请输入表达式：").strip()

        if expr.lower() in ('q', 'quit', 'exit'):
            print("已退出，再见！")
            break
        if not expr:
            continue

        try:
            parts = expr.split()
            if len(parts) != 3:
                print("格式错误！请按“数字 运算符 数字”输入，例如：3 + 5\n")
                continue

            num1 = float(parts[0])
            op = parts[1]
            num2 = float(parts[2])

            result = calculate(num1, op, num2)
            print(f"结果：{result:g}\n")

        except ValueError:
            print("输入有误！请确保输入的是合法数字和运算符。\n")
        except ZeroDivisionError as e:
            print(f"错误：{e}\n")


if __name__ == '__main__':
    main()
```
### 操作方式与错误处理

运行后，您只需按“数字 运算符 数字”的格式输入，就可以快速完成运算。

- **交互流程**：程序启动后会显示支持的运算符和输入示例，然后进入循环等待输入。输入 `q`、`quit` 或 `exit` 即可退出。
- **输入校验**：代码会检查输入是否由三部分组成（数字、运算符、数字），如果格式不正确会提示重新输入。
- **运算逻辑**：`calculate` 函数分别处理加、减、乘、除四种运算，其中除法会检查除数是否为 0。
- **错误处理**：除了除零错误，输入非数字或非法运算符时也会给出友好提示，不会让程序崩溃。
---

**优化建议：** 目前仅支持两个数字和一个运算符，如果您希望支持像“3 + 5 * 2”这样的连续表达式，可以再扩展输入解析部分。
这是一个可直接运行的简易计算器 Python 代码，支持四则运算，并包含基本的错误提示。
```python
def calculate(num1, op, num2):
    """执行四则运算"""
    if op == '+':
        return num1 + num2
    elif op == '-':
        return num1 - num2
    elif op == '*':
        return num1 * num2
    elif op == '/':
        if num2 == 0:
            raise ZeroDivisionError("除数不能为 0")
        return num1 / num2
    else:
        raise ValueError(f"不支持的运算符：{op}")


def main():
    print("===== 简易计算器 =====")
    print("支持的运算：+  -  *  /")
    print("输入格式：数字 运算符 数字（例如 3 + 5）")
    print("输入 q 退出程序\n")

    while True:
        expr = input("请输入表达式：").strip()

        if expr.lower() in ('q', 'quit', 'exit'):
            print("已退出，再见！")
            break
        if not expr:
            continue

        try:
            parts = expr.split()
            if len(parts) != 3:
                print("格式错误！请按“数字 运算符 数字”输入，例如：3 + 5\n")
                continue

            num1 = float(parts[0])
            op = parts[1]
            num2 = float(parts[2])

            result = calculate(num1, op, num2)
            print(f"结果：{result:g}\n")

        except ValueError:
            print("输入有误！请确保输入的是合法数字和运算符。\n")
        except ZeroDivisionError as e:
            print(f"错误：{e}\n")


if __name__ == '__main__':
    main()
```
### 操作方式与错误处理

运行后，您只需按“数字 运算符 数字”的格式输入，就可以快速完成运算。

- **交互流程**：程序启动后会显示支持的运算符和输入示例，然后进入循环等待输入。输入 `q`、`quit` 或 `exit` 即可退出。
- **输入校验**：代码会检查输入是否由三部分组成（数字、运算符、数字），如果格式不正确会提示重新输入。
- **运算逻辑**：`calculate` 函数分别处理加、减、乘、除四种运算，其中除法会检查除数是否为 0。
- **错误处理**：除了除零错误，输入非数字或非法运算符时也会给出友好提示，不会让程序崩溃。
---

**优化建议：** 目前仅支持两个数字和一个运算符，如果您希望支持像“3 + 5 * 2”这样的连续表达式，可以再扩展输入解析部分。
(agent) PS D:\hello-agents-main> 