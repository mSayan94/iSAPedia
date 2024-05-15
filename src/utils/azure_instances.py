from langchain_openai.embeddings import AzureOpenAIEmbeddings
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_community.document_loaders import AzureBlobStorageContainerLoader


def create_embeddings(config, secret_client):
    
    # Load the configuration variables
    api_key_name = config['AZURE_OPENAI_SUBSCRIPTION_NAME']
    base_url = config['AZURE_BASE_URL']
    embedding_deployment_name = config['AZURE_EMBEDDING_DEPLOYMENT_NAME']
    API_KEY = secret_client.get_secret(api_key_name).value  

    # Create the Azure OpenAI Embeddings instance
    embeddings:AzureOpenAIEmbeddings = AzureOpenAIEmbeddings(
        default_headers={
            'Content-Type': "application/json",
            'Ocp-Apim-Subscription-Key': API_KEY,
        },
        azure_deployment="text-embedding-ada-002",
        model=embedding_deployment_name,
        azure_endpoint=base_url,
        openai_api_type="azure",
        api_key=API_KEY
    )

    return embeddings

def create_vectorstore(config, secret_client):

    # Load the configuration variables
    vector_store_address: str = config["AZURE_AISEARCH_URL"]
    index_name: str = config['AZURE_AISEARCH_INDEXNAME']
    api_key_name = config['AZURE_AISEARCH_APIKEY_NAME']
    api_key = secret_client.get_secret(api_key_name).value
    embeddings = create_embeddings(config, secret_client)

    # Create the Azure Search instance
    vector_store: AzureSearch = AzureSearch(
        azure_search_endpoint=vector_store_address,
        azure_search_key=api_key,
        index_name=index_name,
        embedding_function=embeddings.embed_query
    )

    return vector_store

def create_document_loader(config, secret_client):

    # Load the configuration variables
    secret_name = config['SECRET_NAME']
    container_name = config['CONTAINER_NAME']
    blob_connection_string = secret_client.get_secret(secret_name).value

    # Create the Azure BlobStorage Container Loader instance
    loader = AzureBlobStorageContainerLoader(
        conn_str = blob_connection_string,
        container = container_name
    )

    return loader

