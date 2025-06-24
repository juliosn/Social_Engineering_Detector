from flask import Flask, render_template, request
import requests
import uuid
import uuid
from datetime import datetime

app = Flask(__name__)

def get_prediction(text):
    token_response = requests.post(
        'https://iam.cloud.ibm.com/identity/token',
        data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'}
    )
    mltoken = token_response.json()['access_token']
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

    # ID único para cada chamada (para rastreamento no Data Mart)
    record_id = str(uuid.uuid4())

    payload = {
        "input_data": [
            {
                "fields": ["Email Text"],
                "values": [[text]],
                "meta": {
                    "fields": ["Email Text"],
                    "subscription": {
                        "id": ""
                    },
                    "record_id": record_id
                }
            }
        ]
    }

    response = requests.post(DEPLOYMENT_URL, json=payload, headers=header)
    result = response.json()

    prediction = int(result['predictions'][0]['values'][0][0])
    probability = result['predictions'][0]['values'][0][1][prediction]
    return prediction, probability

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email_text = request.form["email_text"]
        prediction, probability = get_prediction(email_text)
        return render_template("index.html", email_text=email_text, prediction=prediction, probability=probability)
    # Passa valores padrão (None) para evitar erro no template
    return render_template("index.html", email_text=None, prediction=None, probability=None)

if __name__ == "__main__":
    app.run(debug=True)
