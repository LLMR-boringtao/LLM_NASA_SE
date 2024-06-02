import chromadb
from typing_extensions import Annotated

import autogen
from autogen import AssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent

config_list = autogen.config_list_from_json("OAI_CONFIG_LIST")

print("LLM models: ", [config_list[i]["model"] for i in range(len(config_list))])

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