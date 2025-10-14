from flask import Flask, render_template, request
import requests
import uuid
import uuid
import requests
import uuid
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import config


app = Flask(__name__)

API_KEY = config.API_KEY
DEPLOYMENT_URL = config.DEPLOYMENT_URL

def get_prediction(text):
    # Obter token
    token_response = requests.post(
        'https://iam.cloud.ibm.com/identity/token',
        data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'}
    )
    token_response.raise_for_status()
    mltoken = token_response.json()['access_token']
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

    # Montar payload
    record_id = str(uuid.uuid4())
    payload = {
        "input_data": [
            {
                "fields": ["Conteudo"],  
                "values": [[text]],
                "meta": {"record_id": record_id}
            }
        ]
    }

    # Chamada ao Watsonx
    response = requests.post(DEPLOYMENT_URL, json=payload, headers=header)
    result = response.json()

    print("Resposta da API:", result)  # debug

    # Validação
    if "predictions" not in result:
        raise ValueError(f"Resposta inesperada: {result}")

    prediction = int(result['predictions'][0]['values'][0][0])
    probability = result['predictions'][0]['values'][0][1][prediction]
    return prediction, probability
