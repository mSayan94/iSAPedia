import logging, json
from pathlib import Path
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from langchain.chains import RetrievalQA
from model.build import create_prompt_template, create_retriever, create_chat_history
from model.llm_helper import create_azure_chat_llm


# This script performs two main tasks.
# First, it establishes a custom logging level named "EVENT".
# Second, it configures the logging module to adhere to a custom format.
logging.addLevelName(25, "EVENT")
format = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=25, format=format)


# Function to load the configuration file
def load_config(config_file_name="config_model.json"):

    logging.log(logging.getLevelName("EVENT"), "Reading configuration file...")

    # Get the current working directory
    current_dir = Path(__file__).parent

    # Go up the directory structure until we find the  config file
    for path in current_dir.parents:
        config_path = path / config_file_name
        if config_path.exists():
            break

    with open(config_path) as f:
        config = json.load(f)

    logging.log(logging.getLevelName("EVENT"), "Configuration file read successfully.")

    return config


# Function to connect to Azure Key Vault
def connect_to_azure_keyvault(config):

    logging.log(
        logging.getLevelName("EVENT"), "Fetching secret client from Azure Key Vault..."
    )

    credential = DefaultAzureCredential()
    key_vault_uri = config["KEY_VAULT_URI"]
    secret_client = SecretClient(vault_url=key_vault_uri, credential=credential)

    logging.log(logging.getLevelName("EVENT"), "Secret client fetched successfully.")

    return secret_client


# This function initializes the retrieval question-answering chain.
def load_retrieval_qa_chain(config, secret_client):

    logging.log(logging.getLevelName("EVENT"), "Initializing retrieval QA chain...")

    prompt_template = create_prompt_template()
    retriever = create_retriever(config, secret_client)
    chat_history = create_chat_history()
    azure_chat_llm = create_azure_chat_llm(config, secret_client)

    qa_chain = RetrievalQA.from_chain_type(
        llm=azure_chat_llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={
            "verbose": False,
            "prompt": prompt_template,
            "memory": chat_history,
        },
    )

    logging.log(
        logging.getLevelName("EVENT"), "Retrieval QA chain initialized successfully."
    )

    return qa_chain


# Run the LLM model
def run_llm(question):

    # Load configuration
    config = load_config()

    # Connect to Azure Key Vault
    secret_client = connect_to_azure_keyvault(config)

    # Load the retrieval QA chain
    logging.log(logging.getLevelName("EVENT"), "Loading retrieval QA chain...")

    qa_chain = load_retrieval_qa_chain(config, secret_client)

    # Generate response to the question
    logging.log(
        logging.getLevelName("EVENT"), "Generating response to the user query..."
    )

    response = qa_chain.invoke({"query": question})
    return response


# if __name__ == "__main__":
#     output = main()
#     print(output["result"])
