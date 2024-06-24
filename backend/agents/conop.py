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
    "temperature": 0
}
copop = MultimodalConversableAgent(
    name="copop",
    llm_config=llm_config,
    system_message="I am a copop agent",
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    llm_config=llm_config,
    human_input_mode="NEVER",
    system_message="Reply TERMINATE if the task has been solved at full satisfaction. Otherwise, reply CONTINUE, or the reason why the task is not solved yet.",
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    max_consecutive_auto_reply=0,
    code_execution_config={
        "use_docker": False,
    }
)

task = """
2加2等于多少？
"""

user_proxy.initiate_chat(copop, message=task)

class COPOP:
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