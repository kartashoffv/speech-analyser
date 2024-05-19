from flask import Flask, request, abort
from ai_models.lang_model import txt_classifier
from ai_models.voice_to_text_model import run_voice_to_text
from dotenv import load_dotenv
import os
from hashlib import md5

load_dotenv()

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.getenv("UPLOAD_FOLDER")


@app.route("/test")
def test_api():
    return {"result": "OK"}


@app.route("/api/audio_file", methods=["POST"])
def process_file():
    if "file" not in request.files:
        abort(422, "Файлы не были загружены")

    file = request.files["file"]
    file_name = md5(file.read()).hexdigest()
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file_name)
    file.save(file_path)

    text_chunks = run_voice_to_text(file_path)

    messages = [msg["text"] for msg in text_chunks]
    message = " ".join(messages)

    result = txt_classifier(message)

    return {"script": message, "class": result}
