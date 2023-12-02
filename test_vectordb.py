import openai
import faiss
import numpy as np
from langchain.chains import RetrievalChain
from langchain.retrievers import EmbeddingRetriever

# OpenAI API Key
openai.api_key = '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'

# Function to get embeddings
def get_embedding(text):
    response = openai.Embedding.create(
        input=text,
        model="text-similarity-babbage-001"
    )
    return response['data'][0]['embedding']

# Vector Database Class
class VectorDB:
    def __init__(self):
        self.dimension = 768
        self.index = faiss.IndexFlatL2(self.dimension)

    def store_embeddings(self, embeddings):
        self.index.add(np.array(embeddings).astype('float32'))

    def find_similar(self, query_embedding, k=5):
        _, indices = self.index.search(np.array([query_embedding]).astype('float32'), k)
        return indices[0]

# Initialize VectorDB
vector_db = VectorDB()

# Read and process text files
def process_text_files(file_paths):
    text_chunks = []
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            text = file.read()
            chapters = text.split('Chapter')  # Assuming chapters are split by the word 'Chapter'
            for chapter in chapters:
                # Further split into smaller chunks if needed
                text_chunks.extend(chunk_text(chapter))
    return text_chunks

# Function to chunk text
def chunk_text(text, chunk_size=500, overlap=50):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size-overlap)]

# Process and store embeddings
text_files = ['content/processed_pdfs/Goldberg/Goldberg.pymupdf.txt', 'content/processed_pdfs/Jurafsdky_Martin/Jurafsdky_Martin.pymupdf.txt']  # Replace with actual file paths
text_chunks = process_text_files(text_files)
embeddings = [get_embedding(chunk) for chunk in text_chunks]
vector_db.store_embeddings(embeddings)

# LangChain setup for Retrieval Chain
retriever = EmbeddingRetriever(vector_db, get_embedding)
chain = RetrievalChain(retriever, openai.Completion.create, model="gpt-4-1106-preview")

# Function to handle queries
def handle_query(query, learning_style):
    # Tailor the prompt based on learning style, if needed
    tailored_prompt = f"{query}\n\n[Learning Style: {learning_style}]"
    response = chain.run(tailored_prompt)
    return response

# Example usage
response = handle_query("What is deep learning?", "Visual")
print(response)