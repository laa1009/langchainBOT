import os
from dotenv import load_dotenv
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

load_dotenv()

# Cliente OpenAI estándar
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Configuración de LangChain
llm = ChatOpenAI(
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o-mini"
)

# Template para el prompt usando el nuevo formato
prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente servicial, creativo, inteligente y muy amigable."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# Clase para manejar el historial de mensajes
class ChatHistory(BaseChatMessageHistory):
    def __init__(self):
        self.messages = []
    
    def add_message(self, message):
        self.messages.append(message)
    
    def clear(self):
        self.messages = []

# Crear el chain con el nuevo formato
chain = prompt | llm

# Crear el runnable con historial de mensajes
runnable_chain = RunnableWithMessageHistory(
    chain,
    lambda session_id: ChatHistory(),
    input_messages_key="input",
    history_messages_key="history"
)

def get_openai_response(messages):
    # Extraer el último mensaje del usuario
    last_message = messages[-1]["content"] if messages else ""
    
    try:
        # Usar el nuevo formato de LangChain para mantener la conversación
        response = runnable_chain.invoke(
            {"input": last_message},
            config={"configurable": {"session_id": "default"}}
        )
        return response.content
    except Exception as e:
        print(f"Error en LangChain: {str(e)}")
        # Fallback a OpenAI directo si hay error
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return response.choices[0].message.content

# Función para reiniciar la conversación
def reset_conversation(session_id="default"):
    chat_history = ChatHistory()
    chat_history.clear()
