from flask import Flask, render_template, request
from services.watson_service import get_prediction
from services.database import save_prediction

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        message = request.form.get("message", "")
        prediction, probability = get_prediction(message)

        if prediction is not None:
            save_prediction(message, prediction, probability)

        return render_template("index.html", message=message,
                               prediction=prediction, probability=probability)
    return render_template("index.html", message=None, prediction=None, probability=None)


if __name__ == "__main__":
    app.run(debug=True)