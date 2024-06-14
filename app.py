import autogen
from autogen import AssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent
import json

config_list = autogen.config_list_from_json("OAI_CONFIG_LIST")
llm_config = {
    "config_list": config_list,
    "max_tokens": 4000,
    "seed": 42,
    "temperature": 0
}
assistant = AssistantAgent(
    name="assistant",
    llm_config=llm_config
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

groupchat=autogen.GroupChat(agents=[assistant, user_proxy], messages=[], speaker_selection_method='round_robin')
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

from flask import Flask, jsonify, render_template, redirect, request
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run", methods=["GET", "POST"])
def run():
    data = request.get_json()
    task = data["message"]
    user_proxy.initiate_chat(manager, message=task)

    messages = [msg for msg in user_proxy.chat_messages[manager] if msg['role'] == 'user']
    for msg in messages:
        msg['content'] = msg['content'].replace('\\n', '\n')
    return app.response_class(
        response=json.dumps(messages, ensure_ascii=False),
        mimetype='application/json'
    )

