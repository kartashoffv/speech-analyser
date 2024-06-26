import streamlit as st


def sidebar():
    with st.sidebar:
        st.markdown(
            "## Инструкция по использованию\n"
            "1. Загрузите файлы в формате MP3 или WAV\n"
            "2. Нажмите кнопку 'Отправить файлы на анализ\n'"
            "3. Дождитесь результатов работы программы\n"
        )

        st.markdown("---")
        st.markdown("О сервисе")
        st.markdown(
            "Данная служба позволяет выявлять нарушения регламентов служебных переговоров "
            "Для использования достаточно загрузить файл/файлы переговоров в формате .wav или .mp3. "
        )
