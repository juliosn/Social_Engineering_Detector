from flask import Flask, render_template, request
from services.watson_service import get_prediction

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        message = request.form.get("message", "")
        prediction, probability = get_prediction(message)

        if prediction is None:
            return render_template("index.html", message=message,
                                   prediction=None, probability=None,
                                   error="Erro ao processar a previsão.")
        return render_template("index.html", message=message,
                               prediction=prediction, probability=probability)
    return render_template("index.html", message=None, prediction=None, probability=None)

if __name__ == "__main__":
    app.run(debug=True)