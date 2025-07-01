import streamlit as st
import requests
import json

# Konfigurasi halaman
st.set_page_config(
    page_title="Sistem Penerjemahan Indonesia-Inggris BY MGN",
    page_icon="🌐",
    layout="wide"
)

def translate_with_mymemory(text, source_lang="id", target_lang="en"):
    """
    Menggunakan MyMemory API untuk terjemahan (gratis, tanpa API key)
    """
    try:
        url = f"https://api.mymemory.translated.net/get"
        params = {
            "q": text,
            "langpair": f"{source_lang}|{target_lang}"
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if response.status_code == 200 and "responseData" in data:
            return data["responseData"]["translatedText"]
        else:
            return None
    except Exception as e:
        st.error(f"Error connecting to translation service: {e}")
        return None

def translate_with_libretranslate(text, source_lang="id", target_lang="en"):
    """
    Menggunakan LibreTranslate API sebagai backup
    """
    try:
        url = "https://libretranslate.de/translate"
        data = {
            "q": text,
            "source": source_lang,
            "target": target_lang,
            "format": "text"
        }
        
        response = requests.post(url, data=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            return result.get("translatedText", None)
        else:
            return None
    except Exception as e:
        return None

def simple_rule_based_translation(text):
    """
    Terjemahan sederhana berbasis aturan sebagai fallback terakhir
    """
    translations = {
        # Salam dan sapaan
        "halo": "hello",
        "hai": "hi",
        "selamat pagi": "good morning",
        "selamat siang": "good afternoon",
        "selamat sore": "good evening",
        "selamat malam": "good night",
        "sampai jumpa": "see you later",
        "sampai bertemu lagi": "see you again",
        
        # Pertanyaan umum
        "apa kabar": "how are you",
        "bagaimana kabar anda": "how are you",
        "siapa nama anda": "what is your name",
        "dari mana anda": "where are you from",
        "berapa umur anda": "how old are you",
        
        # Ungkapan umum
        "terima kasih": "thank you",
        "sama-sama": "you're welcome",
        "maaf": "sorry",
        "permisi": "excuse me",
        "tolong": "please",
        "ya": "yes",
        "tidak": "no",
        
        # Keluarga
        "ayah": "father",
        "ibu": "mother",
        "anak": "child",
        "kakak": "older sibling",
        "adik": "younger sibling",
        
        # Waktu
        "hari ini": "today",
        "kemarin": "yesterday",
        "besok": "tomorrow",
        "minggu": "week",
        "bulan": "month",
        "tahun": "year",
        
        # Tempat
        "rumah": "house",
        "sekolah": "school",
        "kantor": "office",
        "pasar": "market",
        "rumah sakit": "hospital",
        
        # Makanan
        "nasi": "rice",
        "air": "water",
        "makan": "eat",
        "minum": "drink",
        "lapar": "hungry",
        "haus": "thirsty"
    }
    
    text_lower = text.lower().strip()
    
    # Cek terjemahan langsung
    if text_lower in translations:
        return translations[text_lower]
    
    # Cek terjemahan parsial
    for indo, eng in translations.items():
        if indo in text_lower:
            text_lower = text_lower.replace(indo, eng)
    
    return text_lower

# Header aplikasi
st.title("🌐 Sistem Penerjemahan Mesin Bahasa Indonesia-Inggris BY MGN")
st.markdown("---")

# Sidebar dengan informasi
with st.sidebar:
    st.header("ℹ️ Informasi")
    st.markdown("""
    **Aplikasi ini menggunakan:**
    1. MyMemory API (utama)
    2. LibreTranslate API (backup)
    3. Rule-based translation (fallback)
    
    **Fitur:**
    - Terjemahan real-time
    - Multiple translation engines
    - Fallback system untuk reliability
    """)
    
    st.header("📝 Contoh Teks")
    examples = [
        "Halo, apa kabar?",
        "Selamat pagi, bagaimana kabar Anda?",
        "Terima kasih atas bantuan Anda",
        "Saya dari Indonesia",
        "Sampai jumpa nanti"
    ]
    
    for example in examples:
        if st.button(example, key=f"example_{example}"):
            st.session_state.input_text = example

# Main interface
col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Input (Bahasa Indonesia)")
    
    # Text area dengan session state
    if 'input_text' not in st.session_state:
        st.session_state.input_text = "Halo, apa kabar?"
    
    indonesian_text = st.text_area(
        "Masukkan teks Bahasa Indonesia:",
        value=st.session_state.input_text,
        height=200,
        key="main_input"
    )
    
    # Update session state
    st.session_state.input_text = indonesian_text

with col2:
    st.subheader("🔄 Output (English)")
    
    if st.button("Terjemahkan", type="primary", use_container_width=True):
        if indonesian_text.strip():
            with st.spinner("Menerjemahkan..."):
                # Coba MyMemory API terlebih dahulu
                translation = translate_with_mymemory(indonesian_text)
                
                if not translation:
                    st.warning("MyMemory API tidak tersedia, mencoba LibreTranslate...")
                    translation = translate_with_libretranslate(indonesian_text)
                
                if not translation:
                    st.warning("API eksternal tidak tersedia, menggunakan terjemahan sederhana...")
                    translation = simple_rule_based_translation(indonesian_text)
                
                if translation:
                    st.success("✅ Terjemahan berhasil!")
                    st.text_area(
                        "Hasil terjemahan:",
                        value=translation,
                        height=200,
                        disabled=True
                    )
                else:
                    st.error("❌ Terjemahan gagal. Silakan coba lagi.")
        else:
            st.warning("⚠️ Mohon masukkan teks untuk diterjemahkan.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p><strong>Sistem Penerjemahan Mesin Bahasa Indonesia-Inggris</strong></p>
    <p>Dibuat Oleh Muhammad Ghaisan Nafis</p>
</div>
""", unsafe_allow_html=True)


with st.expander("💡 Tips Penggunaan"):
    st.markdown("""
    1. **Untuk hasil terbaik**: Gunakan kalimat yang jelas dan tidak terlalu panjang
    2. **Jika terjemahan tidak akurat**: Coba pecah kalimat menjadi bagian yang lebih kecil
    3. **Untuk kata-kata khusus**: Aplikasi ini bekerja paling baik dengan bahasa sehari-hari
    4. **Jika API tidak tersedia**: Aplikasi akan otomatis menggunakan terjemahan sederhana
    """)

