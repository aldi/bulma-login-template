import openai
import os
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

from dotenv import load_dotenv
load_dotenv()  

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

# added this here
def get_learning_preferences():
    try:
        with open('learning_preferences.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return None  # or return default preferences
    
# Example usage in backend.py
preferences = get_learning_preferences()
print("before preferences")
print(preferences)
print("after preferences")

preferences_descriptions = {
    "Linguistic" : "prefers lists, text blocks, and summarization",
    "Symbolic": "prefers bullet points, symbols, mathematical formulas, and flowcharts",
    "Artistic": "prefers aesthetic use of formatting including bold, itallics, underlining",
    "Poetic": "prefers mnemonic devices, rhythm, and word-play", 
    "Story-Telling": "prefers real-life scenarios, stories, or other anecdotes as teaching tools", 
    "Conversational": "prefers casual conversation/discussion with others to review and learn content"
}

system_message = SystemMessage(
        content=(
            "You are a friendly tutor for LIGN 167, a deep learning and NLP course at UCSD, with immense knowledge and experience in the field."
            "Answer students' questions in a simple, easily-understandable manner based on your knowledge and conversation history. Do not make up answers. Provide examples to make concepts more understandable."
            "You should respond in a conversational, friendly, helpful manner which is tailored to learning peferences with relative weighted importance as follows: " + str(preferences) + ". Please only use these preferences where conducive to crafting the most effective response. Learning preferences are defined as follows: " + str(preferences_descriptions) +
            "If you do not know the answer to a question, just say \'I don't know\'."
            "If asked a question not relevant to deep learning or NLP, just say \'I cannot answer your question\'."
        )
)

prompt = OpenAIFunctionsAgent.create_prompt(
        system_message=system_message,
        extra_prompt_messages=[MessagesPlaceholder(variable_name=memory_key)]
    )

llm = ChatOpenAI(temperature = 0, model = "gpt-4-1106-preview")

agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True)
