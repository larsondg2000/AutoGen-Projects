"""
Autogen using local lm studio and ollama along with chatgpt
The OAI_CONFIG_LIST has the three model parameters
"""

import autogen
import json

filter_criteria = {"model": ["phi"]}

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST.json",
    filter_dict=filter_criteria
)

assistant = autogen.AssistantAgent(
    name="Assistant Agent",
    llm_config={
        "cache_seed": 44,
        "temperature": 0.7,
        "config_list": config_list
    }
)


user = autogen.UserProxyAgent(
    name="User",
    human_input_mode="ALWAYS",
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    # default_auto_reply="create the code for each function. "
    #                   "If the code is complete, save the code to the folder. "
    #                   "If everything is complete exit or terminate",
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False
    }
)

message = """
save the code to disk.

Can you write a total of three functions:

1. The first function takes a string and outputs the number of characters.
2. The second function checks a string to test if it is a palindrome.
3. The third function will take a number and return the square root of it.

"""

user.initiate_chat(
    recipient=assistant,
    message=message,
    silent=False,
    summary_prompt="Summarize the takeaway from the conversation. Do not ass any introductory phrases.  If the intended"
                   "request is NOT properly addressed, please point it out",
    summary_method="reflection_with_llm"
)

json.dump(user.chat_messages[assistant], open("conversations.json", "w"), indent=2)
