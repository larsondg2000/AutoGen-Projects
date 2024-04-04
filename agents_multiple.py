"""
**** Autogen project using multiple agents ****
    + Install pyautogen not autogen
    + The OAI_CONFIG_LIST can be edited for different GPT model versions.  Check the
    + Open AI site for the latest models:  https://platform.openai.com/docs/models
    + Watch usage costs:  https://platform.openai.com/usage
"""

import autogen

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        # see list of models in OAI_CONFIG_LIST
        "model": ["gpt-3.5-turbo-1106"]
    }
)

llm_config_editor = {
    "timeout": 400,
    "seed": 42,
    "config_list": config_list,
    "temperature": 0,
}

llm_config_writer = {
    "timeout": 400,
    "seed": 43,
    "config_list": config_list,
    "temperature": 1,
}

writer = autogen.AssistantAgent(
    name="Writer",
    llm_config=llm_config_writer,
    system_message="Your task is to write an article on a given subject and to rewrite it after receiving feedback "
                   "from the editor.  Reply with TERMINATE after you create a corrected version"
)

editor = autogen.AssistantAgent(
    name="Editor",
    llm_config=llm_config_editor,
    system_message="Your task is to correct the article submitted by the writer. Check if the information is accurate. "
                   "Do not rewrite the article, instead create a list of adjustments to be made, "
                   "make it relatively short."
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    system_message="A human admin",
    human_input_mode="ALWAYS",
    code_execution_config={
        "work_dir": "programs",
        "use_docker": False  # prevents error if not using docker
    },
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
)

group_chat = autogen.GroupChat(
    agents=[user_proxy, writer, editor],
    messages=[],
    max_round=10,
    speaker_selection_method="manual"
)

manager = autogen.GroupChatManager(
    groupchat=group_chat,
    llm_config=llm_config_editor,
)

user_proxy.initiate_chat(
    manager,
    message="write an article about large language models",
)
