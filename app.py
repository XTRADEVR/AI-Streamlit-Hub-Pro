import streamlit as st
import requests
import json

st.set_page_config(
    page_title="Streamlit AI Hub Pro",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Styling (Streamlit High Quality Theme)
st.markdown(
    """
    <style>
        .main { background-color: #0b0f19; color: #f8fafc; }
        .stSidebar { background-color: #111827; }
        .card { background: #1f2937; padding: 20px; border-radius: 12px; border: 1px solid #374151; margin-bottom: 16px; }
        .stButton>button { width: 100%; border-radius: 8px; font-weight: 600; background: #dc2626; color: white; }
        .stButton>button:hover { background: #b91c1c; }
    </style>
    """
    unsafe_allow_html=True
)

# Inisialisasi st.session_state untuk persistensi data agar riwayat tidak hilang
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Halo! Selamat datang di Streamlit AI Hub Pro. Semua data obrolan dan API key disimpan di st.session_state."}
    ]

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "💬 AI Chat"

# Sidebar
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=400&auto=format&fit=crop&q=80", width=120)
    st.title("Streamlit AI Hub")
    st.markdown("---")
    
    st.subheader("🔑 Konfigurasi API Key")
    api_key_input = st.text_input("Gemini API Key", value=st.session_state.api_key, type="password", help="Masukkan API Key Gemini Anda")
    if api_key_input:
        st.session_state.api_key = api_key_input
        st.success("API Key tersimpan di st.session_state!")
        
    st.markdown("---")
    st.subheader("📌 Navigasi Menu")
    selected_menu = st.radio("Pilih Menu:", ["💬 AI Chat", "🌐 Situs AI Free", "⚙️ Pengaturan & Data"], index=0)
    
    st.markdown("---")
    if st.button("🗑️ Hapus Riwayat Chat"):
        st.session_state.messages = [{"role": "assistant", "content": "Riwayat dibersihkan."}]
        st.rerun()
        
    st.markdown("<p style='font-size: 12px; color: #9ca3af; text-align: center;'>Dibuat dengan Streamlit & st.session_state</p>", unsafe_allow_html=True)

# Main Content Routing
if selected_menu == "💬 AI Chat":
    st.title("💬 AI Chat Playground (Persisten)")
    st.markdown("Riwayat obrolan dan API key otomatis tersimpan menggunakan st.session_state sehingga tidak hilang saat halaman dimuat ulang.")
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ketik pesan Anda di sini..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("AI sedang berpikir..."):
                response_text = f"Halo! Pesan Anda: '{prompt}' diterima dengan baik melalui st.session_state."
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})

elif selected_menu == "🌐 Situs AI Free":
    st.title("🌐 Direktori Situs AI Gratis Terbaik")
    st.markdown("Daftar lengkap situs dan platform AI gratis terbaik di dunia dengan gambar dan tautan langsung.")
    
    col1, col2, col3 = st.columns(3)
    ai_sites = [
        {"name": "ChatGPT", "category": "Chatbot", "url": "https://chatgpt.com", "img": "https://images.unsplash.com/photo-1677442136019-21780efad99a?w=400&auto=format&fit=crop&q=80", "desc": "Asisten AI serbaguna dari OpenAI."},
        {"name": "Google Gemini", "category": "Chatbot", "url": "https://gemini.google.com", "img": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=400&auto=format&fit=crop&q=80", "desc": "AI multimodal canggih dari Google."},
        {"name": "Claude", "category": "Coding & Reasoning", "url": "https://claude.ai", "img": "https://images.unsplash.com/photo-1614680376593-902f749f7ffc?w=400&auto=format&fit=crop&q=80", "desc": "Model AI dengan penalaran dan analisis tingkat tinggi."},
    ]
    for idx, site in enumerate(ai_sites):
        col = [col1, col2, col3][idx % 3]
        with col:
            st.markdown(f"<div class='card'><h4 style='color:white;'>{site['name']}</h4><a href='{site['url']}' target='_blank'>Kunjungi</a></div>", unsafe_allow_html=True)

elif selected_menu == "⚙️ Pengaturan & Data":
    st.title("⚙️ Pengaturan & Status Session State")
    st.json({"total_messages": len(st.session_state.messages), "api_key_configured": bool(st.session_state.api_key)})
