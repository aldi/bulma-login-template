import openai
import os
import json
import random

from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import PyMuPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma

from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain.agents.agent_toolkits import create_retriever_tool

from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from langchain.schema import SystemMessage
from langchain.prompts import MessagesPlaceholder

from dotenv import load_dotenv
load_dotenv()  

# Retrieve API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# load PDF documents using PayMuPDF
loader = DirectoryLoader('../content/', glob="**/*.pdf", show_progress=True, loader_cls=PyMuPDFLoader)
docs = loader.load()

# chunk pdf texts and create Chroma vector db
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
documents = text_splitter.split_documents(docs)
db = Chroma.from_documents(documents, OpenAIEmbeddings())

# Create retriever for Chroma db
retriever = db.as_retriever(search_type="mmr")

tool = create_retriever_tool(
    retriever,
    "search_deep_learning_documents",
    "Searches and returns documents regarding deep learning and NLP",
)
tools = [tool]

# add memory
memory_key = "history"
memory = ConversationBufferMemory(memory_key=memory_key, return_messages=True)

# fetch learning preferences from the quiz
def get_learning_preferences():
    try:
        with open('learning_preferences.json', 'r') as file:
            json_string = file.read()  # Read the file content as a string
            intermediate = json.loads(json_string)  # First parse: string to string (JSON representation)
            final_data = json.loads(intermediate)  # Second parse: JSON representation to dictionary
            return final_data
    except FileNotFoundError:
        print("File not found")
        return None
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        return None

def weighted_random_selection(weights):
    total = sum(weights.values())
    r = random.uniform(0, total)
    upto = 0
    for key, weight in weights.items():
        if upto + weight >= r:
            return key
        upto += weight

# Example usage
preferences = get_learning_preferences()
if preferences and isinstance(preferences, dict):
    selected_preference = weighted_random_selection(preferences)
    print(f"Selected Learning Preference: {selected_preference}")
else:
    print("Preferences is not a dictionary or no preferences found")

# define learning preferences
preferences_descriptions_all = {
    "Linguistic" : "This learning style is characterized by a preference for using words, both in speech and writing. Learners with a strong linguistic style enjoy reading, writing, telling stories, and playing word games. They tend to learn best by reading, listening to lectures, and discussing and debating about topics.",
    "Symbolic" : "This learning style involves the use of symbols and abstract representations, such as numbers and mathematical symbols. Learners with a symbolic learning style excel in thinking about abstract concepts, solving complex problems, and understanding complex systems. They often prefer activities like solving puzzles, playing chess, or engaging in strategic games.",
    "Artistic" : "Learners with an artistic style are often visual and spatial thinkers. They prefer using images, pictures, colors, and maps to organize information and communicate with others. They enjoy drawing, doodling, and creating visual aids, and they often excel in activities that involve visual arts and design.",
    "Poetic" : "This style is closely related to the linguistic style but with a specific focus on the rhythmic and emotive aspects of language. Learners with a poetic style are drawn to the rhythm, rhyme, and emotion in words. They enjoy reading and writing poetry, listening to and composing music with lyrical qualities, and are often moved by the expressive nature of language.",
    "Story-Telling" : "Story-telling learners excel when they can frame or understand information in the form of stories. They are skilled at seeing the narrative in information and experiences. This style involves learning by listening to and telling stories, and these learners often remember information better when it's presented as a narrative or through case studies.",
    "Conversational" : "This style involves learning through dialogue and discussion. Learners who favor a conversational style learn best through verbal exchanges, debates, discussions, and talking things through. They benefit greatly from collaborative learning environments where ideas are verbally shared and discussed."
}

preferences_description = preferences_descriptions_all.get(selected_preference)
    
system_message = SystemMessage(
    content=(
        "You are a friendly tutor for LIGN 167, a deep learning and NLP course at UCSD, with immense knowledge and experience in the field."
        "Answer students' questions in a simple, easily-understandable manner based on your knowledge and conversation history. Do not make up answers. Provide frequent examples to make concepts more understandable."
        "You should respond in a manner matching the student's learning peference of " + str(selected_preference) + ". The "+ str(selected_preference) + " learning style is defined as follows: " + str(preferences_description) +
        "If you do not know the answer to a question, just say \'I'm sorry, I do not know\'."
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