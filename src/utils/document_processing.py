from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import AzureBlobStorageContainerLoader
from azure.storage.blob import BlobServiceClient

# Load the blob documents
# def load_documents(loader):
#     documents = loader.load()
#     return documents


def load_documents(loader: AzureBlobStorageContainerLoader, config, secret_client):
    # Load the configuration variables
    secret_name = config["SECRET_NAME"]
    container_name = config["CONTAINER_NAME"]
    # blob_connection_string = secret_client.get_secret(secret_name).value
    secret = secret_client.get_secret(secret_name)
    blob_connection_string = secret.value

    # Create the BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(
        blob_connection_string
    )
    container_client = blob_service_client.get_container_client(container_name)
    documents = []

    # Iterate over all blobs in the container
    for blob in container_client.list_blobs():
        # Check if the blob's file extension is .pdf
        if blob.name.lower().endswith(".pdf"):
            # Load the blob using the loader
            document = loader.load(blob.name)
            documents = documents.append(document)

    return


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
    return docs


# Add documents to the Azure AI Search vector store
def add_documents_to_vector_store(vector_store, docs):
    vector_store.add_documents(documents=docs)
