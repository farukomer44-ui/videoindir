# VIDEO INDIRICI - PYTUBE ILE
import streamlit as st
from pytube import YouTube
import os
import time

st.set_page_config(page_title="Video İndirici", page_icon="🎬")

st.title("🎬 Video İndirici (PyTube)")
st.markdown("YouTube bot korumasını bypass eder")

url = st.text_input(
    "YouTube Linki:",
    placeholder="https://www.youtube.com/watch?v=..."
)

# Test butonu
if st.button("🎯 Test Linki (Çalışan)"):
    # Bu linkler genellikle çalışır
    test_links = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Rick Astley
        "https://www.youtube.com/watch?v=JGwWNGJdvx8",  # Ed Sheeran
        "https://www.youtube.com/watch?v=9bZkp7q19f0",  # PSY - Gangnam Style
    ]
    st.session_state.url = test_links[0]
    st.rerun()

if 'url' in st.session_state:
    url = st.session_state.url

if url:
    # Format seçimi
    format_secim = st.radio(
        "İndirme Türü:",
        ["Video", "Sadece Ses (MP3)"],
        horizontal=True
    )
    
    # Kalite seçimi (video için)
    if format_secim == "Video":
        kalite = st.selectbox(
            "Kalite:",
            ["720p", "480p", "360p", "240p", "144p"]
        )
    
    if st.button("📥 İNDİR", type="primary"):
        try:
            with st.spinner("Video bilgileri alınıyor..."):
                # YouTube nesnesi
                yt = YouTube(
                    url,
                    use_oauth=False,
                    allow_oauth_cache=True
                )
                
                # Video bilgileri
                st.success(f"✅ Video bulundu: **{yt.title}**")
                st.info(f"**Kanal:** {yt.author}")
                st.info(f"**Süre:** {yt.length // 60}:{yt.length % 60:02d} dakika")
                st.info(f"**Görüntüleme:** {yt.views:,}")
                
                # Stream seçimi
                if format_secim == "Sadece Ses (MP3)":
                    stream = yt.streams.filter(only_audio=True).first()
                    if not stream:
                        stream = yt.streams.get_audio_only()
                else:
                    # Kaliteye göre filtrele
                    if kalite == "720p":
                        stream = yt.streams.filter(res="720p", progressive=True).first()
                        if not stream:
                            stream = yt.streams.filter(res="720p").first()
                    elif kalite == "480p":
                        stream = yt.streams.filter(res="480p", progressive=True).first()
                        if not stream:
                            stream = yt.streams.filter(res="480p").first()
                    else:
                        stream = yt.streams.filter(res=kalite).first()
                
                if not stream:
                    st.error("İstenen kalitede stream bulunamadı!")
                    stream = yt.streams.get_highest_resolution()
                
                st.info(f"**Seçilen:** {stream.resolution if hasattr(stream, 'resolution') else 'Audio'} | {stream.filesize_mb:.1f} MB")
                
                # İndirme butonu
                if st.button("🎬 İndirmeyi Başlat", type="secondary"):
                    # İlerleme barı
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # İlerleme callback
                    def on_progress(stream, chunk, bytes_remaining):
                        total_size = stream.filesize
                        bytes_downloaded = total_size - bytes_remaining
                        percentage = (bytes_downloaded / total_size) * 100
                        progress_bar.progress(percentage / 100)
                        status_text.text(f"İndiriliyor: %{percentage:.1f}")
                    
                    yt.register_on_progress_callback(on_progress)
                    
                    # İndirme
                    with st.spinner("İndiriliyor..."):
                        # İndirme başlangıcı
                        status_text.text("İndirme başlıyor...")
                        
                        # Dosyayı indir
                        output_path = stream.download()
                        
                        # MP3'e çevir (eğer seçildiyse)
                        if format_secim == "Sadece Ses (MP3)":
                            import subprocess
                            mp3_path = output_path.replace(".mp4", ".mp3")
                            subprocess.run(['ffmpeg', '-i', output_path, mp3_path])
                            os.remove(output_path)
                            output_path = mp3_path
                        
                        progress_bar.progress(100)
                        status_text.text("✅ İndirme tamamlandı!")
                    
                    st.success(f"**Dosya indirildi:** {os.path.basename(output_path)}")
                    
                    # Dosya boyutu
                    file_size = os.path.getsize(output_path) / (1024*1024)
                    st.info(f"**Dosya boyutu:** {file_size:.1f} MB")
                    
        except Exception as e:
            st.error(f"❌ Hata: {str(e)}")
            st.info("""
            **Sorun giderme:**
            1. Link doğru mu?
            2. Video özel/private olabilir
            3. YouTube bot engellemiş olabilir
            4. İnternet bağlantını kontrol et
            """)

# Alternatif indirme yöntemleri
with st.expander("🔄 Alternatif İndirme Seçenekleri"):
    st.markdown("""
    **Eğer yukarıdaki çalışmazsa:**
    
    **1. Playlist indirici:**
    ```python
    from pytube import Playlist
    playlist = Playlist("LINK")
    for video in playlist.videos:
        video.streams.first().download()
    ```
    
    **2. Farklı formatlar:**
    - WebM formatını dene
    - DASH videoları
    - Adaptive streams
    
    **3. Manuel indirme:**
    1. https://en.y2mate.is/ sitesine git
    2. YouTube linkini yapıştır
    3. İndir butonuna tıkla
    4. Manuel olarak indir
    """)

# Önemli not
st.warning("""
**⚠️ DİKKAT:**
- Sadece kişisel kullanım için
- Telif hakkı olan içerikleri indirmeyin
- YouTube'un şartlarını ihlal etmeyin
- Çok fazla indirme yaparsanız IP'niz banlanabilir
""")

st.markdown("---")
st.caption("🎬 PyTube Video İndirici | YouTube API")
