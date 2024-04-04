"""
**** Basic Autogen project using multiple GPT Models ****
    + Install pyautogen not autogen
    + The OAI_CONFIG_LIST can be edited for different GPT model versions.
    + Check Open AI site for the latest models:  https://platform.openai.com/docs/models
    + Watch usage costs:  https://platform.openai.com/usage
"""
import autogen
from typing import List, Dict, Any


# Configuration for GPT-3.5 model
config_list_gpt3: List[Dict[str, Any]] = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-3.5-turbo-0125"]
    }
)

# Configuration for GPT-4 model
config_list_gpt4: List[Dict[str, Any]] = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-4-0125-preview"]
    }
)

# Configuration dictionary for GPT-3.5 model
llm_config_gpt3: Dict[str, Any] = {
    "temperature": 0,
    "timeout": 300,
    "seed": 21,
    "config_list": config_list_gpt3
}

# Configuration dictionary for GPT-4 model
llm_config_gpt4: Dict[str, Any] = {
    "temperature": 0,
    "timeout": 300,
    "seed": 15,
    "config_list": config_list_gpt4
}

# Creating an instance of AssistantAgent with GPT-3.5 configuration
assistant: autogen.AssistantAgent = autogen.AssistantAgent(
    name="Assistant",
    system_message="You are a helpful assistant",
    # select model here (GPT 3.5 or 4.0)
    llm_config=llm_config_gpt3
)

# Creating an instance of UserProxyAgent with specific configurations
user_proxy: autogen.UserProxyAgent = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="ALWAYS",
    code_execution_config={
        "work_dir": "programs",
        # needs to be set to False if not using Docker
        "use_docker": False
    },
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
)

# Initiating a chat between the user proxy and the assistant
user_proxy.initiate_chat(assistant, message="Write a snake game using pygame. It should keep score: whenever the snake"
                                            " passes over the food the score should increase by one."
                                            " It should also have a start button to start the game.")
