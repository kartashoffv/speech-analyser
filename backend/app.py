from flask import Flask, request

app = Flask(__name__)


@app.route("/test")
def test_api():
    return {"result": "OK"}


@app.route("/api/audio_file", methods=["POST"])
def process_file():
    file = request.files
    file_path = request.values['path']
    #model.process(file)
    return {"result": "OK"}
