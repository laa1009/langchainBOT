# LangChain Flask Bot

Agente conversacional utilizando LangChain, OpenAI y Graph API con Flask.

## Instalación

```bash
git clone https://github.com/TuNombreDeUsuario/langchain-flask-bot.git
cd langchain-flask-bot
python -m venv env
source env/bin/activate   # En Linux/Mac
.\env\Scripts\activate    # En Windows
pip install -r requirements.txt
```

## Configuración

### Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto y agrega las siguientes variables de entorno:

```env
FLASK_SECRET_KEY=tu_clave_secreta
OPENAI_API_KEY=tu_openai_api_key
TENANT_ID=tu_tenant_id
CLIENT_ID=tu_client_id
CLIENT_SECRET=tu_client_secret
SHAREPOINT_SITE_URL=tu_sharepoint_site_url
```

### Configuración para Azure OpenAI (Opcional)

Si tienes las licencias de Azure AD y Azure OpenAI, agrega las siguientes variables de entorno al archivo `.env`:

```env
AZURE_OPENAI_API_KEY=tu_azure_openai_api_key
AZURE_OPENAI_ENDPOINT=tu_azure_openai_endpoint
```

## Uso

### Ejecutar la Aplicación

```bash
flask run
```

### Acceder al Chatbot

Abre tu navegador y ve a `http://localhost:5000/widget` para ver el widget del chatbot.

## Código de Inserción para SharePoint

Para embeber el widget en SharePoint, usa el siguiente código:

```html
<!-- Botón flotante para abrir el chat -->
<div id="chat-widget-button" class="chat-widget-button">
    <img src="/static/images/chat-icon.png" alt="Chat">
</div>

<!-- Contenedor principal del chat -->
<div id="chat-widget-container" class="chat-widget-container hidden">
    <!-- Encabezado del chat -->
    <div class="chat-header">
        <span class="chat-title">Chatbot</span>
        <div class="chat-controls">
            <button id="minimize-button" class="control-button">_</button>
            <button id="close-button" class="control-button">X</button>
        </div>
    </div>

    <!-- Área de mensajes -->
    <div class="chat-messages" id="chat-messages"></div>

    <!-- Área de entrada -->
    <div class="chat-input-area">
        <input type="text" id="chat-input" placeholder="Escribe un mensaje...">
        <button id="send-button">Enviar</button>
    </div>
</div>

<!-- Enlaces a los archivos CSS y JavaScript -->
<link rel="stylesheet" href="/static/css/chat.css">
<link rel="stylesheet" href="/static/css/adaptive-cards.css">
<script src="/static/js/chat.js"></script>
```

## Transición a Azure OpenAI

### Actualización del Código

1. **Actualizar `openai_module.py` para usar Azure OpenAI**:

    ```python
    # filepath: /c:/Users/laa1009/OneDrive - Cencosud/chatbotDEV/openai_module.py
    import os
    from dotenv import load_dotenv
    import requests

    load_dotenv()

    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

    def get_openai_response(messages):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        data = {
            "model": "gpt-4o-mini",
            "messages": messages
        }
        response = requests.post(f"{endpoint}/openai/deployments/gpt-4/chat/completions", headers=headers, json=data)
        return response.json()
    ```

2. **Actualizar `app.py` para usar la nueva función**:

    ```python
    # filepath: /C:/Users/laa1009/OneDrive - Cencosud/chatbotDEV/app.py
    from azure_openai_module import get_openai_response, reset_conversation

    # Rutas y lógica de la aplicación permanecen igual
    ```

### Actualización de Variables de Entorno

Asegúrate de que las variables de entorno para Azure OpenAI estén configuradas en tu archivo `.env`:

```env
AZURE_OPENAI_API_KEY=tu_azure_openai_api_key
AZURE_OPENAI_ENDPOINT=tu_azure_openai_endpoint
```

Con estos cambios, tu aplicación estará configurada para usar Azure OpenAI en lugar de OpenAI. Asegúrate de probar la aplicación después de realizar estos cambios para verificar que todo funcione correctamente.