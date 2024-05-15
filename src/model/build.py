import logging

from langchain_community.retrievers import AzureAISearchRetriever
from langchain_core.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory


# Creates a prompt template for QnA Model.
# It does not require any input variables.
def create_prompt_template():

    logging.log(logging.getLevelName("EVENT"), "Creating prompt template...")

    qna_prompt = """
        Answer the question as detailed as possible. Search from the provided 'Context' and 'Chat History', make sure to provide all the details, if the answer is not in
        in the conext, just say, "I regret to inform you that I currently lack the necessary data to address your inquiry. Perhaps there's another way I can be of assistance?", 
        don't provide any wrong answer\n\n
        Context:\n{context}\n
        Chat History:\n{history}\n
        Question:\n{question}\n

        Answer:
        """
    prompt_template = PromptTemplate(
        template=qna_prompt, input_variables=["question", "context", "history"]
    )

    logging.log(logging.getLevelName("EVENT"), "Prompt template created.")

    return prompt_template


# Creates an Azure AI Search Retriever
# It requires the following input variables: "config", "secret_client"
def create_retriever(config, secret_client):

    logging.log(logging.getLevelName("EVENT"), "Creating Azure AI Search Retriever...")

    api_key_name = config["AZURE_AISEARCH_APIKEY_NAME"]
    search_servicename = config["AZURE_AISEARCH_SERVICENAME"]
    index_name = config["AZURE_AISEARCH_INDEXNAME"]
    API_KEY = secret_client.get_secret(api_key_name).value

    logging.log(
        logging.getLevelName("EVENT"),
        "Setting up Azure AI Search Retriever parameters...",
    )

    retriever = AzureAISearchRetriever(
        service_name=search_servicename,
        index_name=index_name,
        api_key=API_KEY,
        content_key="content",
        top_k=3,
    )

    logging.log(
        logging.getLevelName("EVENT"), "Azure AI Search Retriever created successfully."
    )

    return retriever


# Creates a chat history memory
# We are using the "ConversationBufferMemory" class from the langchain memory module
def create_chat_history():

    logging.log(logging.getLevelName("EVENT"), "Creating chat history...")

    chat_history = ConversationBufferMemory(
        input_key="question", memory_key="history", return_messages=True
    )

    logging.log(logging.getLevelName("EVENT"), "Chat history created.")

    return chat_history
