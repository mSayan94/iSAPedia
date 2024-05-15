from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load the blob documents
def load_documents(loader):
    documents = loader.load()
    return documents

# Document preprocessing
def preprocess_documents(documents):
    for each_page in documents:
        page_content = each_page.page_content
        cleaned_text = " ".join(page_content.split())
        cleaned_text = cleaned_text.replace("\uf0b7","")
        cleaned_text = cleaned_text.replace("\n","")
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
