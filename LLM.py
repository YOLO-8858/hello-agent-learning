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
        file_name='task4.output.txt'

        responseText = llmClient.think(examplemessage,temperature=0.8)
        if responseText:
            print(responseText)
            with open(file_name,'w',encoding="utf-8") as file_obj:
                file_obj.write(responseText)

    except Exception as e:
        print(e)
        
