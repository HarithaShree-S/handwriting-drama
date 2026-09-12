import streamlit as st
from PIL import Image
from analyzer import analyze_handwriting
from scoring import generate_dramatic_report

st.set_page_config(page_title="Handwriting Forensics Lab", page_icon="🧪", layout="centered")

st.title("🧪 HANDWRITING FORENSICS LAB")
st.subheader("How Dramatic Is Your Handwriting? ✍️🎭")
st.write("Upload or snap your handwriting to get a 100% ridiculous forensic drama analysis!")

# Tabs for Camera vs File Upload
tab1, tab2 = st.tabs(["📷 Take Live Photo", "📁 Upload Image File"])

uploaded_file = None

with tab1:
    camera_photo = st.camera_input("Hold your handwriting up to the camera and take a snap!")
    if camera_photo:
        uploaded_file = camera_photo

with tab2:
    file_photo = st.file_uploader("Choose an image file...", type=["jpg", "jpeg", "png"])
    if file_photo:
        uploaded_file = file_photo

# When an image is captured or uploaded
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Handwriting Sample", use_container_width=True)
    
    if st.button("🔬 RUN DRAMA ANALYSIS", use_container_width=True):
        with st.spinner("Analyzing pen aggression and searching Malayalam meme database..."):
            uploaded_file.seek(0)
            image_bytes = uploaded_file.read()
            
            # 1. OpenCV Computer Vision Analysis
            metrics = analyze_handwriting(image_bytes)
            
            if metrics is None:
                st.error("Could not read handwriting. Try holding it closer to light.")
            else:
                # 2. Dramatic Malayalam Scoring Engine
                report = generate_dramatic_report(metrics)
                
                st.success("Analysis Complete!")
                st.markdown("---")
                
                # Big Highlight Score
                st.metric("🎭 MAIN CHARACTER ENERGY", f"{report['main_character_energy']}%")
                
                st.subheader("📊 RAW LABORATORY METRICS")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("💢 Pen Aggression", f"{metrics['pen_aggression']}%")
                    st.metric("📏 Letter Ego", f"{metrics['letter_ego']}%")
                with col2:
                    st.metric("🫂 Word Personal Space", f"{metrics['personal_space']}%")
                    st.metric("🌪️ Chaos Level", f"{metrics['chaos_level']}%")
                
                st.markdown("---")
                st.subheader("🎬 MALAYALAM MOVIE DRAMA REPORT")
                
                st.warning(f"✍️ **Pen Pressure:**\n\n{report['pen_dialogue']}")
                st.info(f"📏 **Letter Ego:**\n\n{report['ego_verdict']}")
                st.success(f"🫂 **Word Spacing:**\n\n{report['space_verdict']}")
                st.error(f"🌪️ **Chaos Evaluation:**\n\n{report['chaos_verdict']}")
                
                st.markdown("---")
                st.header(f"📢 FINAL LAB VERDICT")
                st.subheader(report['final_conclusion'])
                