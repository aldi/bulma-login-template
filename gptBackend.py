import openai
import os

# from flask import Flask, request
import json

from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import PyMuPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma

from langchain.chat_models import ChatOpenAI

from langchain.agents import AgentExecutor
from langchain.memory import ConversationBufferMemory

# used to create the retrieval tool
from langchain.agents.agent_toolkits import create_retriever_tool

# used to create the memory
from langchain.memory import ConversationBufferMemory

# used to create the prompt template
from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from langchain.schema import SystemMessage
from langchain.prompts import MessagesPlaceholder

# used to create the agent executor
from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor

# # Retrieve API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# load PDF documents using PayMuPDF
loader = DirectoryLoader('content/', glob="**/*.pdf", show_progress=True, loader_cls=PyMuPDFLoader)
docs = loader.load()

# chunk pdf texts and create Chroma vector db
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
documents = text_splitter.split_documents(docs)
db = Chroma.from_documents(documents, OpenAIEmbeddings())

retriever = db.as_retriever(search_type="mmr")

tool = create_retriever_tool(
    retriever,
    "search_deep_learning_textbooks",
    "Searches and returns documents regarding deep learning and NLP",
)
tools = [tool]

memory_key = "history"
memory = ConversationBufferMemory(memory_key=memory_key, return_messages=True)

learning_style = "Visual: Bullet Points"
# app = Flask(__name__)
# @app.route('/api/savePreferences', methods=['POST'])
# def save_preferences():
#     data = request.json
#     # need to take these learning preferences and get the values and choose
#     learning_prefs = data['learningPreferences']
#     # Process or save the learning preferences as needed
#     return json.dumps({'status': 'success'})

system_message = SystemMessage(
        content=(
            "You are a tutor for LIGN 167, a deep learning and NLP course at UCSD, with immense knowledge and experience in the field."
            "Answer students' questions based on your knowledge and conversation history. Do not make up answers."
            "If you do not know the answer to a question, just say \'I don't know\'."
            "If asked a question not relevant to deep learning or NLP, just say \'I cannot answer your question\'."
            "Tailor your response to match a " + learning_style + " learning style."
        )
)

prompt = OpenAIFunctionsAgent.create_prompt(
        system_message=system_message,
        extra_prompt_messages=[MessagesPlaceholder(variable_name=memory_key)]
    )

llm = ChatOpenAI(temperature = 0, model = "gpt-4-1106-preview")

agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True)

# # Run the Flask app
# if __name__ == '__main__':
#     app.run(debug=True)