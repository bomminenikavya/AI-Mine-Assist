from flask import Flask, request, render_template, jsonify
from groq_service import execute

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process-message", methods=["POST"])
def process_message():
    data = request.get_json()
    user_message = data["message"]
    generated_answer = execute(user_message)
    return jsonify({"response": generated_answer})


if __name__ == '__main__':
    app.run(debug=True, port=8080)