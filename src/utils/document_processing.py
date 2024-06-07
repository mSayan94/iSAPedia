from azure.storage.blob import BlobServiceClient, BlobSasPermissions, generate_blob_sas
from datetime import datetime, timedelta
from langchain_community.document_loaders import AzureAIDocumentIntelligenceLoader
from azure.keyvault.secrets import SecretClient
from langchain_text_splitters import RecursiveCharacterTextSplitter
import time, logging

# Load the blob documents
# def load_documents(loader):
#     documents = loader.load()
#     return documents


def read_all_blobs(account_name, account_key, container_name):
    blob_service_client = BlobServiceClient(
        account_url=f"https://{account_name}.blob.core.windows.net",
        credential=account_key,
    )
    container_client = blob_service_client.get_container_client(container_name)
    blobs_list = container_client.list_blobs()
    return blobs_list


def generate_sas_url(config, secret_client, blob_name):
    account_name = config["STORAGE_ACCOUNT_NAME"]
    container_name = config["CONTAINER_NAME"]
    account_key_name = config["STORAGE_ACCOUNT_SECRET_NAME"]
    account_key = secret_client.get_secret(account_key_name).value

    blob_service_client = BlobServiceClient(
        account_url=f"https://{account_name}.blob.core.windows.net",
        credential=account_key,
    )
    blob_client = blob_service_client.get_blob_client(container_name, blob_name)
    sas_token = generate_blob_sas(
        blob_service_client.account_name,
        blob_client.container_name,
        blob_client.blob_name,
        account_key=account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1),  # Token will be valid for 1 hour
    )
    sas_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{blob_client.container_name}/{blob_client.blob_name}?{sas_token}"
    return sas_url


def load_documents(config, secret_client, loader):
    # Load the configuration variables
    account_name = config["STORAGE_ACCOUNT_NAME"]
    account_key_name = config["STORAGE_ACCOUNT_SECRET_NAME"]
    container_name = config["CONTAINER_NAME"]
    account_key = secret_client.get_secret(account_key_name).value

    # Load the blob documents
    blobs_list = read_all_blobs(account_name, account_key, container_name)
    documents = []

    if blobs_list is not None:
        for blob in blobs_list:
            # Load only PDF files
            if blob.name.endswith(".pdf"):
                sas_url = generate_sas_url(config, secret_client, blob.name)
                doc_loader = loader(sas_url=sas_url)
                documents = documents + doc_loader.load()
    else:
        print("No blobs found in the container.")

    return documents


# Usage:
# loader = create_document_loader(config, secret_client)
# load_documents(loader, config, secret_client)


# Document preprocessing
def preprocess_documents(documents):
    for each_page in documents:
        page_content = each_page.page_content
        cleaned_text = " ".join(page_content.split())
        cleaned_text = cleaned_text.replace("\uf0b7", "")
        cleaned_text = cleaned_text.replace("\n", "")
        cleaned_text = cleaned_text.strip()
        each_page.page_content = cleaned_text

    return documents


# Create chunks
def create_chunks(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)
    return docs, len(docs)


# Add documents to the Azure AI Search vector store
def add_documents_to_vector_store(vector_store, docs):

    # Split chunks into subset of 100 chunks each
    chunks_subset = [docs[i : i + 100] for i in range(0, len(docs), 100)]
    # Initialize counter for processed documents with type int
    processed_chunks: int = 0

    for subset in chunks_subset:
        # Add the subset of documents to the vector store
        vector_store.add_documents(documents=subset)
        # Increment the counter by the number of documents in the current subset
        processed_chunks += len(subset)
        logging.log(25, f"Processed {processed_chunks} chunks so far.")
        # Pause execution for 220 seconds before processing the next subset
        time.sleep(220)
