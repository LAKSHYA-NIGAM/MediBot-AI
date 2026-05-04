from src.helper import load_pdf_file, filter_to_minimal_docs, text_split, download_hugging_face_embeddings, get_medical_knowledge_documents
from langchain_chroma import Chroma
import shutil
import os

CHROMA_DB_DIR = "./chroma_db"

# Clear old index
if os.path.exists(CHROMA_DB_DIR):
    shutil.rmtree(CHROMA_DB_DIR)
    print(f"Cleared old ChromaDB at '{CHROMA_DB_DIR}'")

# Load PDF data
extracted_data = load_pdf_file(data='data/')
filter_data = filter_to_minimal_docs(extracted_data)
print(f"PDF documents loaded: {len(filter_data)}")

# Load synthetic medical knowledge
medical_knowledge = get_medical_knowledge_documents()
print(f"Synthetic medical documents: {len(medical_knowledge)}")

# Combine all documents
all_documents = filter_data + medical_knowledge
print(f"Total documents before chunking: {len(all_documents)}")

# Chunk all documents
text_chunks = text_split(all_documents)
print(f"Total text chunks: {len(text_chunks)}")

# Download embeddings model
embeddings = download_hugging_face_embeddings()

# Store embeddings in ChromaDB (local, persistent)
docsearch = Chroma.from_documents(
    documents=text_chunks,
    embedding=embeddings,
    persist_directory=CHROMA_DB_DIR,
    collection_name="medical-chatbot"
)

print(f"Documents indexed successfully in '{CHROMA_DB_DIR}'!")