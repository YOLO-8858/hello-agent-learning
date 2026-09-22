from serpapi import SerpApiClient
import os
from dotenv import load_dotenv

load_dotenv()

def search(query:str)-> str:
    try:
        serpapi=os.getenv("SERPAPI_API_KEY")
        if not serpapi:
            return "没有可用的api"

        params = {
            "engine": "google",
            "q": query,
            "api_key": serpapi,
            "gl": "cn",  # 国家代码
            "hl": "zh-cn", # 语言代码
        }

        client=SerpApiClient(params)
        results=client.get_dict()

        if "answer_box_list" in results:
            return "\n".join(results["answer_box_list"])
        if "answer_box" in results and "answer" in results["answer_box"]:
            return results["answer_box"]["answer"]
        if "knowledge_graph" in results and "description" in results["knowledge_graph"]:
            return results["knowledge_graph"]["description"]
        if "organic_results" in results and results["organic_results"]:
            snippets = [
                f"[{i+1}] {res.get('title', '')}\n{res.get('snippet', '')}"
                for i, res in enumerate(results["organic_results"][:3])
            ]
            return "\n\n".join(snippets)
        
        return f"对不起，没有找到关于 '{query}' 的信息。"

    except Exception as e:
        return f"搜索时发生错误{e}"