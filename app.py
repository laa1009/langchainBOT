# app.py
import os
from flask import Flask, jsonify, render_template, request, session
from openai_module import get_openai_response, reset_conversation
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# Configurar una clave secreta para las sesiones
app.secret_key = os.getenv("FLASK_SECRET_KEY", os.urandom(24))

# OAuth Configuration
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SHAREPOINT_SITE_URL = os.getenv("SHAREPOINT_SITE_URL")

TOKEN_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
SCOPE = ["https://graph.microsoft.com/.default"]

def get_access_token():
    try:
        oauth2_session = OAuth2Session(client_id=CLIENT_ID, scope=SCOPE)
        token = oauth2_session.fetch_token(
            token_url=TOKEN_URL,
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            scope=SCOPE,
            grant_type="client_credentials"
        )
        return token["access_token"]
    except Exception as e:
        print(f"Error getting access token: {str(e)}")
        return None

def get_sharepoint_documents(folder_path):
    simulated_response = {
        "d": {
            "results": [
                {
                    "Name": "Document1.pdf",
                    "ServerRelativeUrl": f"{SHAREPOINT_SITE_URL}/Shared Documents/YourFolder/Document1.pdf"
                },
                {
                    "Name": "Document2.docx",
                    "ServerRelativeUrl": f"{SHAREPOINT_SITE_URL}/Shared Documents/YourFolder/Document2.docx"
                }
            ]
        }
    }
    return simulated_response

@app.route('/documents', methods=['GET'])
def documents():
    try:
        folder_path = request.args.get('folder_path', 'Shared Documents/YourFolder')
        documents = get_sharepoint_documents(folder_path)
        return jsonify(documents)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        if not data or 'messages' not in data:
            return jsonify({"error": "No messages provided"}), 400
        
        messages = data.get("messages", [])
        
        # Validar formato de mensajes
        if not all(isinstance(m, dict) and 'role' in m and 'content' in m for m in messages):
            return jsonify({"error": "Invalid message format"}), 400

        # Obtener o crear ID de sesión
        if 'session_id' not in session:
            session['session_id'] = os.urandom(16).hex()

        # Obtener la respuesta usando LangChain
        response = get_openai_response(messages)
        
        return jsonify({
            "response": response,
            "session_id": session['session_id']
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# En las importaciones, actualizar:
from openai_module import get_openai_response, reset_conversation

# Actualizar la ruta /reset-chat:
@app.route('/reset-chat', methods=['POST'])
def reset_chat():
    try:
        # Obtener session_id actual
        session_id = session.get('session_id', 'default')
        # Reiniciar la conversación
        reset_conversation(session_id)
        # Limpiar la sesión actual
        session.clear()
        return jsonify({"message": "Conversación reiniciada exitosamente"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/widget')
def widget():
    return render_template('chat-widget.html')

@app.route('/embed-code')
def embed_code():
    """Retorna el código para embeber el widget en SharePoint"""
    embed_code = """
    <div id="chat-widget-root"></div>
    <script src="/static/js/chat.js"></script>
    <link rel="stylesheet" href="/static/css/chat.css">
    """
    return jsonify({"code": embed_code})

# Manejador de errores para rutas no encontradas
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Ruta no encontrada"}), 404

# Manejador de errores para errores de servidor
@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Error interno del servidor"}), 500

if __name__ == "__main__":
    # Verificar configuración necesaria
    required_env_vars = ["OPENAI_API_KEY", "FLASK_SECRET_KEY"]
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Error: Faltan las siguientes variables de entorno: {', '.join(missing_vars)}")
        exit(1)
        
    app.run(debug=True)
