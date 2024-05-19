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
    # file_name = md5(file.read()).hexdigest()
    file_name = file.filename
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file_name)
    # file_path = app.config["UPLOAD_FOLDER"]
    file.save(file_path)
    print("file_name : ", file_name)
    print("file_path : ", file_path)
    text_chunks = run_voice_to_text(file_path)
    # text_chunks = [{'timestamp': (0.02, 25.1), 'text': ' ЗВОНОК ТЕЛЕФОНА 2422 машинист Карадин на перегоне Красногвардей, З-2 погромная.'}, {'timestamp': (26.82, 28.74), 'text': ' 2422, Карадин, слушаю вас.'}, {'timestamp': (29.8, 38.7), 'text': ' Здравствуйте, машинист, не затягивайтесь, хорошо, до станции Сорочинская проедьте, пожалуйста, по ТОЦКО по первому пути будете ехать до МС Бахтинова.'}, {'timestamp': (43.9, 46.46), 'text': ' Понятно, по первому пути.'}, {'timestamp': (47.86, 48.18), 'text': ' Станция ворочается.'}, {'timestamp': (49.36, 49.46), 'text': ' Национальный пустильный след.'}, {'timestamp': (50.2, 82.86), 'text': ' Бахчинова корабль. Я понял. Продолжение следует...'}]

    messages = [msg["text"] for msg in text_chunks]
    message = "\n".join(messages)
    message = message.replace("Продолжение следует...", "")
    # Продолжение следует...
    print(f"message is {message}")
    # message = message.encode('utf-8')
    result = txt_classifier(message)
    

    return {"script": message, "class": result}
