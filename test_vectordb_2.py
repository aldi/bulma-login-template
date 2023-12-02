import os
import openai

from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import PyMuPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.vectorstores import Chroma

# Retrieve API key
#os.environ['OPENAI_API_KEY'] = getpass.getpass('OpenAI API Key:')
openai.api_key = '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'

text_loader_kwargs={'autodetect_encoding': True}
loader = DirectoryLoader('content/processed_pdfs/', glob="**/*pymupdf.txt", show_progress=True, loader_cls=TextLoader, loader_kwargs=text_loader_kwargs)
docs = loader.load()

# Load the document, split it into chunks, embed each chunk and load it into the vector store.
""" raw_documents = TextLoader('content/processed_pdfs/Goldberg/Goldberg.pymupdf.txt').load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
documents = text_splitter.split_documents(raw_documents)
db = Chroma.from_documents(documents, OpenAIEmbeddings())

query = "What is a Recurrent Neural Network (RNN)?"

embedding_vector = OpenAIEmbeddings().embed_query(query)
docs = db.similarity_search_by_vector(embedding_vector)
print(docs[0].page_content) """