from dotenv import load_dotenv
import os
import streamlit as st
import logging
from components.sidebar import sidebar
import time
from core.parsing import load_audio_file

import requests

supported_formats = ["mp3", "wav"]
pretty_supported_formats = ", ".join(supported_formats)

logger = logging.getLogger()

st.set_page_config(page_title="Анализатор РЖД", page_icon="📖", layout="wide")
st.header("Анализатор служебных переговоров")

sidebar()


file_count = 0
load_dotenv()


uploaded_files = st.file_uploader(
    f"Загрузите файлы в следующих форматах: {supported_formats}",
    type=supported_formats,
    accept_multiple_files=True,
)

if not uploaded_files:
    st.stop()

processed_files = []

progress_text = "Загрузка файлов. Загружено {} из {}"
file_count = progress_bar = st.progress(
    0, text=progress_text.format(0, len(uploaded_files))
)

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

for processed_file in processed_files:
    api = os.getenv("API_HOST")
    payload = {"path": processed_file.file_path}
    response = requests.post(
        url=f"http://{api}:5000/api/audio_file",
        files={'file': processed_file.bytes},
        data=payload,
    )
    print(response.content)
    # TODO Обработка ошибки сервера
    results.append(response)


#    # Output Columns
#    answer_col, sources_col = st.columns(2)
#
#    llm = get_llm(model=model, openai_api_key=openai_api_key, temperature=0)
#    result = query_folder(
#        folder_index=folder_index,
#        query=query,
#        return_all=return_all_chunks,
#        llm=llm,
#    )
#
#    with answer_col:
#        st.markdown("#### Answer")
#        st.markdown(result.answer)
#
#    with sources_col:
#        st.markdown("#### Sources")
#        for source in result.sources:
#            st.markdown(source.page_content)
#            st.markdown(source.metadata["source"])
#            st.markdown("---")
