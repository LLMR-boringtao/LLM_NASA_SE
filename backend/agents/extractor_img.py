import chromadb
from typing_extensions import Annotated

import autogen
from autogen import AssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent

config_list = autogen.config_list_from_json("OAI_CONFIG_LIST")
llm_config = {
    "config_list": config_list,
    "max_tokens": 4000,
    "seed": 42,
    "temperature": 0,
}
extractor = MultimodalConversableAgent(
    name="extractor",
    max_consecutive_auto_reply=5,
    llm_config=llm_config,
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    system_message="I am a user proxy agent",
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=0,
    code_execution_config={
        "use_docker": False,
    },
)

message = """
提取商品及金额信息.
使用中文.
列表输出商品及金额信息.
<img data/invoice.jpg>.
"""

user_proxy.initiate_chat(extractor, message=message)

class Extractor:
    def __init__(self, request, context=""):
        self.request = request
        self.context = context

    def perceiver(self):
        query_request = self.request
        query_context = self.context
        query = str(query_request + " " + query_context)
        return query

    def planner(self):
        pass

    def actor(self):
        query = self.perceiver()
        result = query

        return result