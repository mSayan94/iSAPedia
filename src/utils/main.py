import json, logging
from pathlib import Path
from functools import partial
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure_instances import (
    create_vectorstore,
    create_document_loader,
    create_docintelligence_loader,
    create_embeddings,
)
from document_processing import (
    load_documents,
    preprocess_documents,
    create_chunks,
    add_documents_to_vector_store,
)

# This script sets up a custom logging level named "EVENT" with a numeric value of 25.
# The value 25 is chosen because it sits between the default INFO (20) and WARNING (30) levels,
# indicating that EVENT is of higher priority than INFO but lower than WARNING.
# It also configures the logging module to use a custom format for log messages and to log messages at the "EVENT" level and above.
import logging

logging.addLevelName(25, "EVENT")  # Define a new level
format = "%(asctime)s - %(levelname)s - %(message)s"  # Create a custom format
logging.basicConfig(level=25, format=format)  # Configure the logging module


# Function to load the configuration file
def load_config(config_file_name="config_utils.json"):
    # Get the current working directory
    current_dir = Path(__file__).parent

    # Go up the directory structure until we find the  config file
    for path in current_dir.parents:
        config_dir = path / "config"
        if config_dir.exists():
            config_path = config_dir / config_file_name
            break

    with open(config_path) as f:
        config = json.load(f)
    return config


# Function to connect to Azure Key Vault
def connect_to_azure_keyvault(key_vault_uri):
    credential = DefaultAzureCredential()
    secret_client = SecretClient(vault_url=key_vault_uri, credential=credential)
    return secret_client


# Main function
def main():
    # Load the configuration at the start of the program
    logging.log(25, "Reading config parameters...")
    config = load_config()
    logging.log(25, "Config parameters were read successfully.")

    # Establish connection to Azure Key Vault
    logging.log(25, "Establishing connection to Azure Keyvault...")
    secret_client = connect_to_azure_keyvault(config["KEY_VAULT_URI"])
    logging.log(25, "Connected to Azure Keyvault successfully...")

    # Generate vector store
    logging.log(25, "Creating vector store...")
    vector_store = create_vectorstore(config, secret_client)
    logging.log(25, "Vector store created successfully.")

    # Generate document loader
    logging.log(25, "Creating document loader...")
    loader = partial(
        create_docintelligence_loader, config=config, secret_client=secret_client
    )
    logging.log(25, "Document loader created successfully.")

    # Load the documents
    logging.log(25, "Loading documents...")
    documents = load_documents(config, secret_client, loader)
    logging.log(25, "Documents loaded successfully.")

    # Preprocess the documents
    logging.log(25, "Preprocessing documents...")
    documents = preprocess_documents(documents)
    logging.log(25, "Documents preprocessed successfully.")

    # Create chunks
    logging.log(25, "Creating chunks...")
    docs, num_chunks = create_chunks(documents)
    logging.log(25, f"{num_chunks} Chunks created successfully.")

    # Add documents to the Azure AI Search vector store
    logging.log(25, "Adding documents to vector store...")
    add_documents_to_vector_store(vector_store, docs)
    logging.log(25, "Documents added to vector store successfully.")


if __name__ == "__main__":
    main()
