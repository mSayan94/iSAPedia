import logging

from langchain_openai import AzureChatOpenAI


def create_azure_chat_llm(config, secret_client):
    """
    Initializes the Azure Chat LLM Model.
    """

    logging.log(
        logging.getLevelName("EVENT"), "Initializing AzureChatOpenAI LLM Model..."
    )

    api_key_name = config["AZURE_OPENAI_SUBSCRIPTION_NAME"]
    BASE_URL = config["AZURE_BASE_URL"]
    DEPLOYMENT_NAME = config["AZURE_OPENAI_DEPLOYMENT_NAME"]
    TEMPERATURE: float = config["AZURE_OPENAI_TEMPERATURE"]
    API_VERSION = config["AZURE_OPENAI_API_VERSION"]
    API_KEY = secret_client.get_secret(api_key_name).value

    azure_chat_llm = AzureChatOpenAI(
        default_headers={"Ocp-Apim-Subscription-Key": API_KEY},
        azure_endpoint=BASE_URL,
        azure_deployment=DEPLOYMENT_NAME,
        temperature=TEMPERATURE,
        api_key=API_KEY,
        api_version=API_VERSION,
    )

    logging.log(logging.getLevelName("EVENT"), "AzureChatOpenAI LLM Model initialized.")

    return azure_chat_llm
