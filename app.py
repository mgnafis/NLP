import streamlit as st
from transformers import pipeline

@st.cache_resource
def load_translator():
    # Menggunakan model yang lebih ringan atau yang secara eksplisit mendukung CPU
    # Helsinki-NLP/opus-mt-id-en seharusnya bekerja dengan CPU secara default
    translator = pipeline("translation", model="Helsinki-NLP/opus-mt-id-en")
    return translator

st.title("Sistem Penerjemahan Mesin Bahasa Indonesia-Inggris")

translator = load_translator()

indonesian_text = st.text_area("Masukkan teks Bahasa Indonesia di sini:", "Halo, apa kabar?")

if st.button("Terjemahkan ke Bahasa Inggris"):
    if indonesian_text:
        with st.spinner("Menerjemahkan..."):
            english_text = translator(indonesian_text)[0]["translation_text"]
        st.success("Terjemahan berhasil!")
        st.text_area("Terjemahan Bahasa Inggris:", english_text, height=150)
    else:
        st.warning("Mohon masukkan teks untuk diterjemahkan.")


