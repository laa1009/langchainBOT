import os
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template
from requests_ntlm import HttpNtlmAuth
import requests

app = Flask(__name__)
load_dotenv()
# Configuración
SHAREPOINT_SITE_URL = "https://cnco.sharepoint.com/sites/SeguridadInformticaColombia"
# Reemplaza con tu usuario en formato DOMINIO\\usuario
SHAREPOINT_USERNAME = os.getenv("SHAREPOINT_USERNAME")
SHAREPOINT_PASSWORD = os.getenv("SHAREPOINT_PASSWORD")
USERNAME = f"{SHAREPOINT_USERNAME}"
PASSWORD = f"{SHAREPOINT_PASSWORD}"


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/get-sites', methods=['GET'])
def get_sites():
    # Configura los encabezados para la petición
    headers = {
        "Accept": "application/json;odata=verbose"
    }

    # Realiza la petición GET a SharePoint utilizando NTLM
    try:
        response = requests.get(
            f"{SHAREPOINT_SITE_URL}/_api/web/webs",
            headers=headers,
            auth=HttpNtlmAuth(USERNAME, PASSWORD)
        )

        # Verifica el estado de la respuesta
        if response.status_code == 200:
            data = response.json()
            return jsonify(data)
        else:
            return jsonify({"error": f"Error al obtener sitios: {response.status_code}", "details": response.text})
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(port=5000, debug=True)
