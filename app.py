"""
Handwriting Forensics Lab - Streamlit Web Application
High-energy, dark-neon forensic laboratory for graphology drama analysis.
"""

import os
import glob
from pathlib import Path
from PIL import Image
import streamlit as st

from analyzer import analyze_handwriting
from scoring import generate_dramatic_report

# -----------------------------------------------------------------------------
# 1. Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Forensic Graphology Lab // Dept. of Absurd Metrics",
    page_icon="🧪",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# -----------------------------------------------------------------------------
# 2. Dark/Neon Forensic Lab Custom CSS Styling
# -----------------------------------------------------------------------------
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700;800&family=Orbitron:wght@600;800;900&family=Plus+Jakarta+Sans:wght@400;600;700&display=swap');

    /* Global Dark Slate Blue Theme */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #16243d 0%, #0d1527 40%, #070c16 100%) !important;
        color: #e2e8f0;
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    }

    /* Dramatic Forensic Header Badge */
    .lab-badge-wrapper {
        display: flex;
        justify-content: center;
        margin-top: -15px;
        margin-bottom: 25px;
    }
    
    .lab-badge {
        display: inline-flex;
        align-items: center;
        gap: 12px;
        background: rgba(13, 27, 50, 0.9);
        border: 1px solid #00f0ff;
        box-shadow: 0 0 18px rgba(0, 240, 255, 0.35), inset 0 0 12px rgba(0, 240, 255, 0.15);
        border-radius: 9999px;
        padding: 8px 22px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        color: #00f0ff;
        text-transform: uppercase;
        animation: badgePulse 3s infinite alternate;
    }

    .badge-dot {
        width: 10px;
        height: 10px;
        background-color: #00ff9d;
        border-radius: 50%;
        box-shadow: 0 0 10px #00ff9d, 0 0 20px #00ff9d;
        animation: blinkDot 1.4s infinite;
    }

    .badge-classified {
        background: #00f0ff;
        color: #060b13;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: 800;
        font-size: 0.72rem;
    }

    @keyframes badgePulse {
        0% { box-shadow: 0 0 12px rgba(0, 240, 255, 0.25); }
        100% { box-shadow: 0 0 22px rgba(0, 240, 255, 0.55); }
    }

    @keyframes blinkDot {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.3; transform: scale(0.75); }
    }

    /* Main Title Styling */
    .lab-title-container {
        text-align: center;
        margin-bottom: 20px;
    }

    .lab-main-title {
        font-family: 'Orbitron', sans-serif;
        font-weight: 900;
        font-size: 2.35rem;
        letter-spacing: 3px;
        background: linear-gradient(135deg, #00f0ff 0%, #00ff9d 60%, #ffffff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
        text-shadow: 0 0 30px rgba(0, 240, 255, 0.4);
    }

    .lab-subtitle {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.95rem;
        color: #94a3b8;
        letter-spacing: 1px;
    }

    .lab-subtitle span {
        color: #00ff9d;
        font-weight: 600;
    }

    /* Tabs Customization */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(13, 21, 38, 0.85) !important;
        border: 1px solid rgba(0, 240, 255, 0.2) !important;
        border-radius: 12px !important;
        padding: 6px !important;
        gap: 8px !important;
    }

    .stTabs [data-baseweb="tab"] {
        color: #94a3b8 !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        padding: 8px 18px !important;
        transition: all 0.25s ease !important;
        border: none !important;
        background-color: transparent !important;
    }

    .stTabs [aria-selected="true"] {
        color: #00f0ff !important;
        background: rgba(0, 240, 255, 0.14) !important;
        border: 1px solid rgba(0, 240, 255, 0.4) !important;
        box-shadow: 0 0 14px rgba(0, 240, 255, 0.2) !important;
    }

    /* Action Button - High Energy Neon Pulse */
    .stButton > button {
        background: linear-gradient(135deg, #00f0ff 0%, #00ff9d 100%) !important;
        color: #070c16 !important;
        font-family: 'Orbitron', 'JetBrains Mono', sans-serif !important;
        font-size: 1.05rem !important;
        font-weight: 800 !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.4), 0 0 35px rgba(0, 255, 157, 0.25) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) scale(1.01) !important;
        box-shadow: 0 0 28px rgba(0, 240, 255, 0.7), 0 0 45px rgba(0, 255, 157, 0.45) !important;
    }

    /* Hero Metric Highlight Card: Main Character Energy */
    .hero-metric-card {
        background: linear-gradient(145deg, rgba(17, 30, 54, 0.9) 0%, rgba(9, 16, 30, 0.95) 100%);
        border: 1.5px solid #00f0ff;
        box-shadow: 0 0 25px rgba(0, 240, 255, 0.3), inset 0 0 20px rgba(0, 240, 255, 0.1);
        border-radius: 16px;
        padding: 24px 28px;
        margin: 22px 0 28px 0;
        position: relative;
        overflow: hidden;
    }

    .hero-metric-card::after {
        content: "";
        position: absolute;
        top: 0;
        right: 0;
        width: 150px;
        height: 150px;
        background: radial-gradient(circle, rgba(0, 240, 255, 0.15) 0%, transparent 70%);
        pointer-events: none;
    }

    .hero-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }

    .hero-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.15rem;
        font-weight: 800;
        letter-spacing: 2px;
        color: #00f0ff;
        text-transform: uppercase;
    }

    .hero-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 1px;
        color: #00ff9d;
        background: rgba(0, 255, 157, 0.12);
        border: 1px solid rgba(0, 255, 157, 0.4);
        border-radius: 6px;
        padding: 4px 10px;
    }

    .hero-body {
        display: flex;
        align-items: baseline;
        gap: 20px;
        margin-bottom: 14px;
    }

    .hero-score {
        font-family: 'Orbitron', monospace;
        font-size: 3.8rem;
        font-weight: 900;
        color: #ffffff;
        text-shadow: 0 0 25px #00f0ff;
        line-height: 1;
    }

    .hero-percent {
        font-size: 2.2rem;
        color: #00f0ff;
    }

    .hero-verdict-pill {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.92rem;
        color: #cbd5e1;
    }

    .hero-progress-bg {
        width: 100%;
        height: 12px;
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid rgba(0, 240, 255, 0.3);
        border-radius: 9999px;
        overflow: hidden;
        margin-top: 8px;
    }

    .hero-progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #00f0ff 0%, #00ff9d 100%);
        box-shadow: 0 0 12px #00f0ff;
        border-radius: 9999px;
        transition: width 1s ease-in-out;
    }

    /* Sub-Metric Highlight Cards (2x2 Grid) */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 16px;
        margin-bottom: 28px;
    }

    @media (max-width: 640px) {
        .metric-grid {
            grid-template-columns: 1fr;
        }
    }

    .metric-card {
        background: rgba(14, 24, 43, 0.85);
        border: 1px solid rgba(0, 240, 255, 0.22);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
        border-radius: 12px;
        padding: 18px;
        transition: all 0.25s ease;
        position: relative;
    }

    .metric-card:hover {
        border-color: #00f0ff;
        box-shadow: 0 0 18px rgba(0, 240, 255, 0.28);
        transform: translateY(-2px);
    }

    .metric-card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }

    .metric-card-name {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 1px;
        color: #94a3b8;
        text-transform: uppercase;
    }

    .metric-card-icon {
        font-size: 1.25rem;
    }

    .metric-card-value {
        font-family: 'Orbitron', monospace;
        font-size: 2.1rem;
        font-weight: 800;
        color: #00ff9d;
        text-shadow: 0 0 15px rgba(0, 255, 157, 0.35);
        margin-bottom: 10px;
    }

    .metric-mini-bar-bg {
        width: 100%;
        height: 6px;
        background: rgba(15, 23, 42, 0.8);
        border-radius: 999px;
        overflow: hidden;
    }

    .metric-mini-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #00f0ff, #00ff9d);
        border-radius: 999px;
    }

    /* Section Subheaders */
    .section-header {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.15rem;
        font-weight: 800;
        letter-spacing: 2px;
        color: #00f0ff;
        text-transform: uppercase;
        margin: 28px 0 16px 0;
        display: flex;
        align-items: center;
        gap: 10px;
        border-bottom: 1px solid rgba(0, 240, 255, 0.2);
        padding-bottom: 8px;
    }

    /* Drama Report Dialogues Cards */
    .dialogue-card {
        background: rgba(13, 22, 39, 0.85);
        border-left: 4px solid #00f0ff;
        border-top: 1px solid rgba(0, 240, 255, 0.15);
        border-right: 1px solid rgba(0, 240, 255, 0.15);
        border-bottom: 1px solid rgba(0, 240, 255, 0.15);
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 14px;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .dialogue-card.pen { border-left-color: #ff3366; }
    .dialogue-card.ego { border-left-color: #ffb800; }
    .dialogue-card.space { border-left-color: #00ff9d; }
    .dialogue-card.chaos { border-left-color: #00f0ff; }

    .dialogue-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 5px;
    }

    .dialogue-card.pen .dialogue-title { color: #ff3366; }
    .dialogue-card.ego .dialogue-title { color: #ffb800; }
    .dialogue-card.space .dialogue-title { color: #00ff9d; }
    .dialogue-card.chaos .dialogue-title { color: #00f0ff; }

    .dialogue-quote {
        font-size: 0.95rem;
        color: #f1f5f9;
        line-height: 1.5;
    }

    /* Final Forensic Lab Verdict Box */
    .final-verdict-box {
        background: linear-gradient(135deg, rgba(20, 36, 65, 0.95) 0%, rgba(10, 18, 33, 0.98) 100%);
        border: 2px solid #00ff9d;
        box-shadow: 0 0 30px rgba(0, 255, 157, 0.25), inset 0 0 15px rgba(0, 255, 157, 0.1);
        border-radius: 14px;
        padding: 24px;
        margin-top: 24px;
        text-align: center;
    }

    .verdict-header {
        font-family: 'Orbitron', sans-serif;
        font-size: 0.95rem;
        font-weight: 800;
        letter-spacing: 3px;
        color: #00ff9d;
        text-transform: uppercase;
        margin-bottom: 12px;
    }

    .verdict-content {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.15rem;
        font-weight: 700;
        color: #ffffff;
        line-height: 1.6;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.4);
    }

    /* Audio Stinger Notification Badge */
    .audio-alert-badge {
        display: flex;
        align-items: center;
        gap: 10px;
        background: rgba(0, 240, 255, 0.12);
        border: 1px solid rgba(0, 240, 255, 0.35);
        border-radius: 8px;
        padding: 10px 16px;
        margin: 18px 0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        color: #00f0ff;
    }

    /* Style file uploader and camera containers */
    [data-testid="stFileUploader"], [data-testid="stCameraInput"] {
        background: rgba(13, 22, 39, 0.6) !important;
        border: 1px dashed rgba(0, 240, 255, 0.3) !important;
        border-radius: 12px !important;
        padding: 14px !important;
    }

    [data-testid="stFileUploader"]:hover, [data-testid="stCameraInput"]:hover {
        border-color: #00f0ff !important;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.2) !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 3. Audio Resolver Helper
# -----------------------------------------------------------------------------
def get_audio_source(is_high_drama: bool):
    """
    Checks if an 'assets' folder exists in the project directory containing sound files (.mp3 or .wav).
    If found, returns local file path or bytes.
    If not found, falls back gracefully to playing lightweight royalty-free web audio URLs.
    """
    assets_dir = Path("assets")
    target_type = "dramatic" if is_high_drama else "comedy"

    # 1. Check local assets directory
    if assets_dir.is_dir():
        # Priority check: dramatic.wav / dramatic.mp3 or comedy.wav / comedy.mp3
        for ext in [".wav", ".mp3", ".ogg"]:
            candidate = assets_dir / f"{target_type}{ext}"
            if candidate.exists() and candidate.is_file():
                mime = "audio/wav" if ext == ".wav" else ("audio/mpeg" if ext == ".mp3" else "audio/ogg")
                return str(candidate), mime, "local"

        # Search for any audio file matching keyword
        audio_files = [f for f in assets_dir.iterdir() if f.suffix.lower() in [".wav", ".mp3", ".ogg"]]
        if audio_files:
            for f in audio_files:
                if target_type in f.stem.lower():
                    mime = "audio/wav" if f.suffix == ".wav" else ("audio/mpeg" if f.suffix == ".mp3" else "audio/ogg")
                    return str(f), mime, "local"
            # Return first available file
            first_f = audio_files[0]
            mime = "audio/wav" if first_f.suffix == ".wav" else ("audio/mpeg" if first_f.suffix == ".mp3" else "audio/ogg")
            return str(first_f), mime, "local"

    # 2. Royalty-free reliable web audio fallback URLs
    fallback_urls = {
        "dramatic": "https://actions.google.com/sounds/v1/emergency/emergency_siren_short_burst.ogg",
        "comedy": "https://actions.google.com/sounds/v1/cartoon/clang_and_wobble.ogg",
    }
    url = fallback_urls.get(target_type, fallback_urls["comedy"])
    return url, "audio/ogg", "web_fallback"


# -----------------------------------------------------------------------------
# 4. Header Badge & Lab Title
# -----------------------------------------------------------------------------
st.markdown(
    """
<div class="lab-badge-wrapper">
    <div class="lab-badge">
        <span class="badge-dot"></span>
        <span>🧪 FORENSIC GRAPHOLOGY LABORATORY // DEPT. OF ABSURD METRICS</span>
        <span class="badge-classified">ACTIVE</span>
    </div>
</div>
<div class="lab-title-container">
    <div class="lab-main-title">HANDWRITING FORENSICS</div>
    <div class="lab-subtitle">Real Computer Vision Analysis <span>// 100% Unhinged Malayalam Movie Verdicts</span></div>
</div>
""",
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 5. Input Tabs (Live Photo Camera vs Image File Upload)
# -----------------------------------------------------------------------------
tab1, tab2 = st.tabs(["📷 Take Live Photo", "📁 Upload Image File"])

uploaded_file = None

with tab1:
    camera_photo = st.camera_input("Hold handwriting sample up to the lens and capture:")
    if camera_photo:
        uploaded_file = camera_photo

with tab2:
    file_photo = st.file_uploader(
        "Upload scanned paper or high-contrast photo:",
        type=["jpg", "jpeg", "png"],
        help="Supports JPG, JPEG, and PNG formats.",
    )
    if file_photo:
        uploaded_file = file_photo

# -----------------------------------------------------------------------------
# 6. Sample Preview & Forensic Execution
# -----------------------------------------------------------------------------
if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file)
        st.image(image, caption="SPECIMEN SAMPLE [AUTHENTICATED]", use_container_width=True)
    except Exception as e:
        st.error(f"Error loading image specimen: {e}")

    if st.button("🔬 RUN DRAMA ANALYSIS", use_container_width=True):
        with st.spinner("Calibrating ink density & consulting Malayalam cine-forensic records..."):
            uploaded_file.seek(0)
            image_bytes = uploaded_file.read()

            # 1. Computer Vision Processing via OpenCV
            metrics = analyze_handwriting(image_bytes)

            if metrics is None:
                st.error("⚠️ SPECIMEN REJECTED: Could not detect clear handwriting strokes. Hold specimen closer to light and try again.")
            else:
                # 2. Dramatic Scoring & Malayalam Movie Dialogue Generation
                report = generate_dramatic_report(metrics)
                main_energy = report["main_character_energy"]
                is_high_drama = report.get("is_high_drama", False)

                # 3. Sound Effects Integration
                audio_src, audio_mime, audio_origin = get_audio_source(is_high_drama)
                audio_label = "Dramatic Emergency Alert Stinger" if is_high_drama else "Slapstick Comedy Hit"

                try:
                    if audio_origin == "local" and os.path.exists(audio_src):
                        with open(audio_src, "rb") as f:
                            st.audio(f.read(), format=audio_mime, autoplay=True)
                    else:
                        st.audio(audio_src, format=audio_mime, autoplay=True)
                except Exception:
                    # Silent graceful fallback to ensure app never crashes
                    pass

                # Sound status indicator
                st.markdown(
                    f"""
                <div class="audio-alert-badge">
                    <span>🔊</span>
                    <span><strong>FORENSIC AUDIO FX:</strong> Playing {audio_label} ({'Local Asset' if audio_origin == 'local' else 'Royalty-Free Fallback'})</span>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                # -----------------------------------------------------------------
                # Highlight Card 1: Main Character Energy (Hero Card)
                # -----------------------------------------------------------------
                if main_energy >= 75:
                    energy_tag = "SUPERNOVA LEVEL // CINEMATIC HERO"
                elif main_energy >= 50:
                    energy_tag = "STEADY LEAD // SUPPORTING PROTAGONIST"
                else:
                    energy_tag = "STEALTH OPERATIVE // BACKGROUND EXTRA"

                st.markdown(
                    f"""
                <div class="hero-metric-card">
                    <div class="hero-header">
                        <span class="hero-title">🎭 MAIN CHARACTER ENERGY</span>
                        <span class="hero-tag">STATUS: VERIFIED</span>
                    </div>
                    <div class="hero-body">
                        <div class="hero-score">{main_energy}<span class="hero-percent">%</span></div>
                        <div class="hero-verdict-pill">
                            <strong>CLASSIFICATION:</strong> {energy_tag}
                        </div>
                    </div>
                    <div class="hero-progress-bg">
                        <div class="hero-progress-bar" style="width: {main_energy}%;"></div>
                    </div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                # -----------------------------------------------------------------
                # Highlight Cards 2-5: Raw Laboratory Metrics (2x2 Grid)
                # -----------------------------------------------------------------
                st.markdown(
                    """
                <div class="section-header">
                    <span>📊</span>
                    <span>RAW LABORATORY METRICS</span>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f"""
                <div class="metric-grid">
                    <!-- Metric Card: Pen Aggression -->
                    <div class="metric-card">
                        <div class="metric-card-header">
                            <span class="metric-card-name">Pen Aggression</span>
                            <span class="metric-card-icon">💢</span>
                        </div>
                        <div class="metric-card-value">{metrics['pen_aggression']}%</div>
                        <div class="metric-mini-bar-bg">
                            <div class="metric-mini-bar-fill" style="width: {metrics['pen_aggression']}%;"></div>
                        </div>
                    </div>

                    <!-- Metric Card: Letter Ego -->
                    <div class="metric-card">
                        <div class="metric-card-header">
                            <span class="metric-card-name">Letter Ego</span>
                            <span class="metric-card-icon">📏</span>
                        </div>
                        <div class="metric-card-value">{metrics['letter_ego']}%</div>
                        <div class="metric-mini-bar-bg">
                            <div class="metric-mini-bar-fill" style="width: {metrics['letter_ego']}%;"></div>
                        </div>
                    </div>

                    <!-- Metric Card: Word Personal Space -->
                    <div class="metric-card">
                        <div class="metric-card-header">
                            <span class="metric-card-name">Word Personal Space</span>
                            <span class="metric-card-icon">🫂</span>
                        </div>
                        <div class="metric-card-value">{metrics['personal_space']}%</div>
                        <div class="metric-mini-bar-bg">
                            <div class="metric-mini-bar-fill" style="width: {metrics['personal_space']}%;"></div>
                        </div>
                    </div>

                    <!-- Metric Card: Chaos Level -->
                    <div class="metric-card">
                        <div class="metric-card-header">
                            <span class="metric-card-name">Chaos Level</span>
                            <span class="metric-card-icon">🌪️</span>
                        </div>
                        <div class="metric-card-value">{metrics['chaos_level']}%</div>
                        <div class="metric-mini-bar-bg">
                            <div class="metric-mini-bar-fill" style="width: {metrics['chaos_level']}%;"></div>
                        </div>
                    </div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                # -----------------------------------------------------------------
                # Malayalam Movie Drama Report
                # -----------------------------------------------------------------
                st.markdown(
                    """
                <div class="section-header">
                    <span>🎬</span>
                    <span>MALAYALAM MOVIE DRAMA REPORT</span>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f"""
                <div class="dialogue-card pen">
                    <div class="dialogue-title">✍️ Pen Pressure Analysis</div>
                    <div class="dialogue-quote">{report['pen_dialogue']}</div>
                </div>

                <div class="dialogue-card ego">
                    <div class="dialogue-title">📏 Letter Ego Evaluation</div>
                    <div class="dialogue-quote">{report['ego_verdict']}</div>
                </div>

                <div class="dialogue-card space">
                    <div class="dialogue-title">🫂 Word Spacing Forensics</div>
                    <div class="dialogue-quote">{report['space_verdict']}</div>
                </div>

                <div class="dialogue-card chaos">
                    <div class="dialogue-title">🌪️ Chaos & Entropy Spectrum</div>
                    <div class="dialogue-quote">{report['chaos_verdict']}</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                # -----------------------------------------------------------------
                # Final Lab Verdict Box
                # -----------------------------------------------------------------
                st.markdown(
                    f"""
                <div class="final-verdict-box">
                    <div class="verdict-header">📢 FINAL FORENSIC LAB VERDICT</div>
                    <div class="verdict-content">{report['final_conclusion']}</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )