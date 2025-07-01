import streamlit as st
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

@st.cache_resource
def load_translator():
    # Menggunakan model yang tidak memerlukan sentencepiece
    # atau menggunakan model dengan tokenizer yang sudah tersedia
    try:
        # Coba gunakan model yang lebih kompatibel
        model_name = "Helsinki-NLP/opus-mt-id-en"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        translator = pipeline("translation", model=model, tokenizer=tokenizer)
        return translator
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

st.title("Sistem Penerjemahan Mesin Bahasa Indonesia-Inggris")

translator = load_translator()

if translator is not None:
    indonesian_text = st.text_area("Masukkan teks Bahasa Indonesia di sini:", "Halo, apa kabar?")

    if st.button("Terjemahkan ke Bahasa Inggris"):
        if indonesian_text:
            with st.spinner("Menerjemahkan..."):
                try:
                    english_text = translator(indonesian_text)[0]["translation_text"]
                    st.success("Terjemahan berhasil!")
                    st.text_area("Terjemahan Bahasa Inggris:", english_text, height=150)
                except Exception as e:
                    st.error(f"Error during translation: {e}")
        else:
            st.warning("Mohon masukkan teks untuk diterjemahkan.")
else:
    st.error("Model tidak dapat dimuat. Silakan coba lagi nanti.")

