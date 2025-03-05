import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()
api_key = os.getenv("api_key")
client = OpenAI(
    organization='org-jkOnohznVhRaRIy55kLfoCaQ',
    project='proj_LEK5rOMUfteMF6eO03RLso16',
    api_key=api_key
)

# from openai import OpenAI

# client = OpenAI()

stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{
        "role": "user", "content": "como hago para ir añadiendo el ccontexto de unchat. debería ir guardando en una db las respuestas tuyas y los prompts míos, para que en el campo 'messages del client.chat.completions.create' sean siempre citadas?"},
        {"role": "assistant",
         "content": "Para mantener el contexto en un chat utilizando la API de OpenAI, puedes implementar un sistema en el que guardes tanto las preguntas (prompts) que haces como las respuestas que recibes. De esta manera, podrás construir un historial de mensajes que puedes incluir en cada solicitud a la API."},
        {"role": "user",
         "content": "Y no existe una herramienta para saber qué datos serían los más relevantes para mantener el contexto sin guardar información innecesaria?"},
        {"role": "assistant",
         "content": "No existe una herramienta única y universal que te diga exactamente qué datos son los más relevantes para mantener el contexto en un chat, ya que esto puede variar según la aplicación y el tipo de conversación. Sin embargo, aquí hay algunas estrategias que pueden ayudarte a decidir qué información guardar:Implementar un mecanismo que solo almacene información relevante y necesaria no solo te ayudará a mantener el contexto, sino que también optimizará el uso de recursos y la eficiencia de las interacciones."},
        {"role": "user",
         "content": "Y en cuanto a chatGPT con su modelo 4o, cuál es el recomendado de longitud que debería tener un chat para no empezar con imprecisiones? es decir en texto haciendo la conversión a tokens del input y output promedio, o si puedes en tiempo de charla contínua."}],
    stream=True,
)
for chunk in stream: 
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
