# Streamlit Cloud Video İndirici
import streamlit as st
import sys
import subprocess
import os

# Önce yt-dlp'yi kontrol et ve kur
try:
    import yt_dlp
    yt_dlp_mevcut = True
except ImportError:
    yt_dlp_mevcut = False
    st.warning("yt-dlp kuruluyor... Lütfen bekleyin.")
    
    # yt-dlp'yi kur
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
    
    # Sayfayı yenile
    st.success("Kurulum tamamlandı! Sayfayı yenileyin.")
    st.stop()

# Uygulama başlığı
st.set_page_config(
    page_title="Video İndirici",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 Video İndirici")
st.markdown("YouTube'dan video indirin")

# Ana bölüm
url = st.text_input(
    "**YouTube Linki:**",
    placeholder="https://www.youtube.com/watch?v=...",
    help="YouTube video linkini buraya yapıştırın"
)

# Test butonu
if st.button("🎯 Test Linki Kullan"):
    st.session_state.test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    st.rerun()

if 'test_url' in st.session_state:
    url = st.session_state.test_url

if url:
    # Format seçimi
    format_secim = st.radio(
        "**Format Seçin:**",
        ["MP4 Video", "MP3 Müzik"],
        horizontal=True
    )
    
    # İndirme butonu
    if st.button("📥 İNDİR", type="primary", use_container_width=True):
        try:
            with st.spinner("İndirme başlıyor..."):
                # İndirme ayarları
                ydl_opts = {
                    'outtmpl': '%(title)s.%(ext)s',
                    'quiet': False,
                }
                
                if format_secim == "MP3 Müzik":
                    ydl_opts.update({
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                        }],
                    })
                
                # İndirme işlemi
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # Video bilgilerini al
                    info = ydl.extract_info(url, download=False)
                    video_adi = info.get('title', 'video')
                    
                    st.info(f"**Video:** {video_adi}")
                    st.info(f"**Format:** {format_secim}")
                    
                    # İlerleme barı
                    progress_bar = st.progress(0)
                    
                    def ilerleme_goster(d):
                        if d['status'] == 'downloading':
                            try:
                                yuzde = float(d.get('_percent_str', '0%').replace('%', ''))
                                progress_bar.progress(yuzde / 100)
                            except:
                                pass
                    
                    ydl_opts['progress_hooks'] = [ilerleme_goster]
                    
                    # YDL'yi yeniden oluştur
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl2:
                        ydl2.download([url])
                    
                    progress_bar.progress(100)
                    
                st.success("✅ **İndirme Tamamlandı!**")
                st.balloons()
                
                # Bilgilendirme
                st.info("""
                **📌 Not:** 
                - Dosya Streamlit Cloud sunucusuna indirildi
                - Yerel bilgisayarınıza inmesi için programı kendi bilgisayarınızda çalıştırın
                - https://github.com adresinden kodu indirebilirsiniz
                """)
                
        except Exception as e:
            st.error(f"❌ Hata: {str(e)}")

# Yardım bölümü
with st.expander("📖 Nasıl Kullanılır?", expanded=True):
    st.markdown("""
    1. **YouTube'da bir video açın**
    2. **Tarayıcı adres çubuğundaki linki kopyalayın**
    3. **Linki yukarıdaki kutuya yapıştırın**
    4. **MP4 Video veya MP3 Müzik seçin**
    5. **"İndir" butonuna tıklayın**
    6. **İndirme bitene kadar bekleyin**
    
    **⚠️ Dikkat:**
    - Sadece kişisel kullanım için
    - Telif hakkı olan içerikleri indirmeyin
    - Bu web sitesi eğitim amaçlıdır
    """)

# Alt bilgi
st.markdown("---")
st.caption("🎬 Video İndirici | Python + yt-dlp | Streamlit Cloud")