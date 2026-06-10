"""笑话生成器模块 - 集成多个外部 API"""

import requests
import json
from typing import Dict, List


class JokeGenerator:
    """笑话生成器 - 支持多个笑话 API"""
    
    # 笑话 API 列表
    APIS = {
        "official": {
            "name": "Official Joke API",
            "url": "https://official-joke-api.appspot.com/random_joke",
            "description": "官方笑话 API - 随机英文笑话"
        },
        "dad_jokes": {
            "name": "icanhazdadjoke",
            "url": "https://icanhazdadjoke.com/",
            "description": "爸爸笑话 API - 网络经典笑话"
        },
        "programming": {
            "name": "Official Joke API - Programming",
            "url": "https://official-joke-api.appspot.com/jokes/programming/random",
            "description": "编程笑话 API - 程序员专用"
        }
    }
    
    @staticmethod
    def get_random_joke(api_type: str = "official") -> Dict:
        """
        获取随机笑话
        
        Args:
            api_type: API 类型 ("official", "dad_jokes", "programming")
        
        Returns:
            笑话数据字典
        """
        if api_type not in JokeGenerator.APIS:
            return {
                "success": False,
                "error": f"未知的 API 类型: {api_type}",
                "available": list(JokeGenerator.APIS.keys())
            }
        
        api_config = JokeGenerator.APIS[api_type]
        
        try:
            response = requests.get(
                api_config["url"],
                headers={"Accept": "application/json"},
                timeout=5
            )
            response.raise_for_status()
            
            data = response.json()
            
            # 根据 API 类型格式化响应
            if api_type == "official":
                return {
                    "success": True,
                    "type": data.get("type", "general"),
                    "setup": data.get("setup", ""),
                    "punchline": data.get("punchline", ""),
                    "joke_id": data.get("id"),
                    "api": api_type
                }
            
            elif api_type == "dad_jokes":
                # icanhazdadjoke 返回纯文本，需要特殊处理
                if isinstance(data, dict) and "joke" in data:
                    return {
                        "success": True,
                        "joke": data["joke"],
                        "api": api_type
                    }
            
            elif api_type == "programming":
                # 编程笑话通常是数组
                if isinstance(data, list) and len(data) > 0:
                    joke = data[0]
                    return {
                        "success": True,
                        "type": joke.get("type", "programming"),
                        "setup": joke.get("setup", ""),
                        "punchline": joke.get("punchline", ""),
                        "joke_id": joke.get("id"),
                        "api": api_type
                    }
            
            return {
                "success": True,
                "data": data,
                "api": api_type
            }
        
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "请求超时",
                "api": api_type
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": "网络连接失败",
                "api": api_type
            }
        except requests.exceptions.HTTPError as e:
            return {
                "success": False,
                "error": f"HTTP 错误: {e.response.status_code}",
                "api": api_type
            }
        except json.JSONDecodeError:
            return {
                "success": False,
                "error": "无法解析 JSON 响应",
                "api": api_type
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "api": api_type
            }
    
    @staticmethod
    def get_multiple_jokes(count: int = 3, api_type: str = "official") -> List[Dict]:
        """
        获取多个笑话
        
        Args:
            count: 笑话数量
            api_type: API 类型
        
        Returns:
            笑话列表
        """
        jokes = []
        for _ in range(min(count, 10)):  # 最多 10 条
            joke = JokeGenerator.get_random_joke(api_type)
            if joke.get("success"):
                jokes.append(joke)
        
        return jokes
    
    @staticmethod
    def format_joke_display(joke: Dict) -> str:
        """
        格式化笑话显示
        
        Args:
            joke: 笑话数据
        
        Returns:
            格式化的笑话文本
        """
        if not joke.get("success"):
            return f"❌ 获取笑话失败: {joke.get('error', '未知错误')}"
        
        api = joke.get("api", "unknown")
        
        if api == "official" or api == "programming":
            setup = joke.get("setup", "")
            punchline = joke.get("punchline", "")
            joke_type = joke.get("type", "")
            
            display = f"😂 【{joke_type}笑话】\n\n"
            display += f"问: {setup}\n\n"
            display += f"答: {punchline}\n\n"
            display += f"来源: {api}"
            
            return display
        
        elif api == "dad_jokes":
            joke_text = joke.get("joke", "")
            display = f"😂 【爸爸笑话】\n\n{joke_text}\n\n来源: {api}"
            return display
        
        else:
            return f"😂 {joke.get('joke', joke.get('data', ''))}"
    
    @staticmethod
    def list_available_apis() -> Dict:
        """获取可用的 API 列表"""
        return {
            "total": len(JokeGenerator.APIS),
            "apis": JokeGenerator.APIS
        }


# 创建全局笑话生成器实例
joke_generator = JokeGenerator()
