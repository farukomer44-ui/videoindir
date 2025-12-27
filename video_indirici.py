# YÖNLENDİRİCİ WEB SİTESİ
import streamlit as st

st.set_page_config(page_title="Video İndirici", page_icon="🎬")

st.title("🎬 Video İndirici - Online Araçlar")
st.markdown("Aşağıdaki online araçları kullanarak video indirebilirsiniz:")

# Online araçlar listesi
araçlar = [
    {
        "ad": "Y2Mate",
        "url": "https://en.y2mate.is/",
        "aciklama": "YouTube, Facebook, Instagram, TikTok",
        "ozellik": "Çoklu site desteği"
    },
    {
        "ad": "SaveFrom.net",
        "url": "https://en.savefrom.net/",
        "aciklama": "YouTube, Vimeo, Dailymotion",
        "ozellik": "Hızlı ve güvenilir"
    },
    {
        "ad": "OnlineVideoConverter",
        "url": "https://www.onlinevideoconverter.com/",
        "aciklama": "MP4, MP3, AVI, WMV",
        "ozellik": "Çoklu format"
    },
    {
        "ad": "YTMP3",
        "url": "https://ytmp3.cc/",
        "aciklama": "YouTube'dan MP3",
        "ozellik": "Sadece ses"
    },
    {
        "ad": "SSYouTube",
        "url": "https://ssyoutube.com/",
        "aciklama": "YouTube indirici",
        "ozellik": "Kalite seçimi"
    }
]

# URL girişi
url = st.text_input("YouTube Linkiniz:", placeholder="Linki buraya yapıştırın")

if url:
    st.success("Link alındı! Aşağıdaki araçlardan birini seçin:")
    
    # Her araç için buton
    for araç in araçlar:
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(f"🔗 {araç['ad']}")
                st.write(f"📝 {araç['aciklama']}")
                st.write(f"⭐ {araç['ozellik']}")
            with col2:
                # Otomatik link oluştur
                import urllib.parse
                encoded_url = urllib.parse.quote(url)
                target_url = f"{araç['url']}?url={encoded_url}"
                
                st.markdown(f"""
                <a href="{target_url}" target="_blank">
                    <button style="
                        background-color: #4CAF50;
                        color: white;
                        padding: 10px 20px;
                        border: none;
                        border-radius: 5px;
                        cursor: pointer;
                        font-weight: bold;
                    ">
                        ⚡ Aç
                    </button>
                </a>
                """, unsafe_allow_html=True)
            st.markdown("---")

# Nasıl kullanılır
with st.expander("📖 Nasıl Kullanılır?"):
    st.markdown("""
    1. YouTube linkini yukarıdaki kutuya yapıştır
    2. Açılan araçlardan birini seç
    3. Yeni sekmede açılacak
    4. O sitede "Download" butonuna tıkla
    5. Video/Müzik bilgisayarına inecek
    
    **Avantajları:**
    - Bot engeli yok
    - Her zaman çalışır
    - Kalite seçeneği var
    - Ücretsiz
    
    **Dezavantajları:**
    - Reklam olabilir
    - Başka siteye yönlendirme
    """)

st.markdown("---")
st.caption("ℹ️ Bu site sadece online araçlara yönlendirme yapar")
