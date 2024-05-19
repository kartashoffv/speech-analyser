from dotenv import load_dotenv
import os
import streamlit as st
import logging
from components.sidebar import sidebar
import time
from core.parsing import load_audio_file

import requests

load_dotenv()

supported_formats = ["mp3", "wav"]
pretty_supported_formats = ", ".join(supported_formats)

logger = logging.getLogger()

st.set_page_config(page_title="Анализатор РЖД", page_icon="📖", layout="wide")
st.header("Анализатор служебных переговоров")

sidebar()

uploaded_files = st.file_uploader(
    f"Загрузите файлы в следующих форматах: {supported_formats}",
    type=supported_formats,
    accept_multiple_files=True,
)

submit = st.button("Отправить файлы на анализ")

if not uploaded_files:
    st.stop()

processed_files = []

progress_text = "Загрузка файлов. Загружено {} из {}"
progress_bar = st.progress(0, text=progress_text.format(0, len(uploaded_files)))

for ind, file in enumerate(uploaded_files):
    file_no = ind + 1
    processed_file = load_audio_file(file)
    if not processed_file:
        st.error(
            f"Формат файла {file.name} не поддерживается.\n\
            Список поддерживаемых форматов: {pretty_supported_formats}"
        )
        logger.error(f"Формат файла {file.name} не поддерживается")
        continue
    if not processed_file.is_valid():
        st.error(
            f"Файл {file.name} не был определен как файл формата {processed_file.format}.\n\
            Убедитесь, что файл не поврежден"
        )
        logger.error("Не удалось прочитать файл")
        uploaded_files.remove(file)
        processed_file.dispose()
        continue
    progress_bar.progress(
        file_no / len(uploaded_files),
        text=progress_text.format(file_no, len(uploaded_files)),
    )
    processed_files.append(processed_file)
else:
    time.sleep(0.5)
    progress_bar.empty()

if not processed_files:
    st.stop()


results = []

if not submit:
    st.stop()

progress_text = "Анализ файлов. Проанализировано {} из {}"
progress_bar = st.progress(0, text=progress_text.format(0, len(processed_files)))

for ind, processed_file in enumerate(processed_files):
    file_no = ind + 1
    API_HOST = os.getenv("API_HOST")
    response = requests.post(
        url=f"http://{API_HOST}:5000/api/audio_file",
        files={"file": processed_file.bytes},
    )
    if not response.status_code == 200:
        st.error(
            f"Возникла серверная ошибка при обработке файла {processed_file.initial_name}.\n\
                 Обратитесь в службу поддержки."
        )
        continue
    progress_bar.progress(
        file_no / len(processed_files),
        text=progress_text.format(file_no, len(processed_files)),
    )
    response = response.json()
    results.append(
        {
            "file_name": processed_file.initial_name,
            "script": response["script"],
            "class": response["class"],
        }
    )
    processed_file.dispose()

progress_bar.empty()


if not results:
    st.stop()

# Output Columns
file_name_col, script_col, class_col = st.columns([2, 3, 1])

with file_name_col:
    st.header("Имя файла")
    for result in results:
        st.markdown(result["file_name"])

with script_col:
    st.header("Транскрипция диалога")
    for result in results:
        st.markdown(result["script"])

with class_col:
    st.header("Результат")
    for result in results:
        st.markdown(result["class"])
