import streamlit as st
from io import BytesIO
from gtts import gTTS
import folium
from streamlit_folium import st_folium
from spatial_triage import analyze_emergency
from visualizer import draw_bounding_boxes
from campus_dispatch import dispatch_emergency_sos
from panic_system import render_panic_alarm
from manager import get_offline_protocol

# ===== PAGE CONFIG & THEME =====
st.set_page_config(
    page_title="Campus Health & Safety Companion",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "🏥 Campus Emergency Response System",
        "Get help": "https://campus-safety.edu/help"
    }
)

# ===== CUSTOM CSS STYLING =====
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #FF4444;
        --secondary-color: #1E3A5F;
        --success-color: #00B86F;
        --warning-color: #FFA500;
        --danger-color: #DC143C;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #FF4444 0%, #DC143C 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(255, 68, 68, 0.3);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.95;
    }
    
    /* Card styling */
    .info-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #e9ecef 100%);
        border-left: 4px solid #FF4444;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Severity badges */
    .severity-critical {
        background: #DC143C;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    .severity-high {
        background: #FF6B6B;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        font-weight: 600;
    }
    
    .severity-medium {
        background: #FFA500;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        font-weight: 600;
    }
    
    .severity-low {
        background: #00B86F;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        font-weight: 600;
    }
    
    /* Instructions styling */
    .instruction-box {
        background: #f0f8ff;
        border-left: 4px solid #1E3A5F;
        padding: 1rem 1.5rem;
        border-radius: 5px;
        margin: 0.8rem 0;
    }
    
    .warning-box {
        background: #fff5e6;
        border-left: 4px solid #FFA500;
        padding: 1rem 1.5rem;
        border-radius: 5px;
        margin: 0.8rem 0;
    }
    
    .danger-box {
        background: #ffe6e6;
        border-left: 4px solid #DC143C;
        padding: 1rem 1.5rem;
        border-radius: 5px;
        margin: 0.8rem 0;
    }
    
    /* Section headers */
    .section-header {
        border-bottom: 3px solid #FF4444;
        padding-bottom: 0.5rem;
        margin: 2rem 0 1.5rem 0;
        font-size: 1.4rem;
        font-weight: 600;
        color: #1E3A5F;
    }
    
    /* Panic button */
    .panic-btn {
        background: linear-gradient(135deg, #DC143C 0%, #8B0000 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 50px;
        font-size: 1.2rem;
        font-weight: 700;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(220, 20, 60, 0.4);
        transition: all 0.3s ease;
    }
    
    .panic-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(220, 20, 60, 0.6);
    }
    
    /* Input styling */
    .input-section {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin: 1rem 0;
    }
    
    /* Status indicators */
    .status-success {
        color: #00B86F;
        font-weight: 600;
    }
    
    .status-error {
        color: #DC143C;
        font-weight: 600;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }
    
    .stTabs [role="tablist"] {
        border-bottom: 2px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# ===== SIDEBAR =====
with st.sidebar:
    st.markdown("### ⚙️ SETTINGS & INFO")
    
    lang = st.selectbox(
        "🗣️ Select Language",
        ["English", "Spanish", "Hindi", "French"],
        help="Choose the language for analysis and instructions"
    )
    
    st.divider()
    
    st.markdown("### 📍 Campus Info")
    st.write("""
    - **Campus Name**: Central University
    - **Coordinates**: 28.607°N, 77.213°E
    - **Security Hotline**: +91-XXXX-XXXX
    - **Response Time**: ~5-8 minutes
    """)
    
    st.divider()
    
    st.markdown("### ❓ EMERGENCY HOTLINES")
    st.write("""
    - 🚑 **Ambulance**: 102
    - 🚨 **Police**: 100
    - 🔥 **Fire**: 101
    - 💊 **Poison Control**: 1-800-222-1222
    """)

# ===== MAIN HEADER =====
st.markdown("""
<div class="main-header">
    <h1>🚨 CAMPUS SAFETY COMPANION</h1>
    <p>Intelligent Emergency Response System for Campus Health & Safety</p>
</div>
""", unsafe_allow_html=True)

# ===== EMERGENCY BUTTON ROW =====
col1, col2, col3 = st.columns([2, 1, 1])

with col2:
    if st.button("🚨 PANIC ALARM", key="panic_btn", use_container_width=True, type="primary"):
        with st.spinner("🔔 Triggering emergency alert..."):
            render_panic_alarm()
            st.success("✅ Panic alarm activated! Emergency services alerted.")

# ===== MAIN CONTENT TABS =====
tab1, tab2, tab3 = st.tabs(["📋 Report Emergency", "🗺️ Campus Map", "ℹ️ Information"])

# ===== TAB 1: EMERGENCY REPORTING =====
with tab1:
    st.markdown('<div class="section-header">📸 Report Emergency Scene</div>', unsafe_allow_html=True)
    
    # Image input section
    input_col1, input_col2 = st.columns(2)
    
    with input_col1:
        st.markdown('<div class="info-card"><b>📤 Upload Photo</b></div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Upload emergency scene photo",
            type=["jpg", "jpeg", "png"],
            key="uploader",
            label_visibility="collapsed"
        )
    
    with input_col2:
        st.markdown('<div class="info-card"><b>📷 Capture Photo</b></div>', unsafe_allow_html=True)
        camera_file = st.camera_input(
            "Take emergency photo",
            key="camera",
            label_visibility="collapsed"
        )
    
    active_file = uploaded_file or camera_file
    
    # Description input
    st.markdown('<div class="section-header">📝 Emergency Details</div>', unsafe_allow_html=True)
    user_notes = st.text_area(
        "Describe the emergency situation or symptoms:",
        placeholder="e.g., 'Person collapsed on the ground', 'Severe allergic reaction', 'Accident victim with bleeding'...",
        height=100,
        label_visibility="collapsed"
    )
    
    # Submit button
    submit_col1, submit_col2, submit_col3 = st.columns([1, 2, 1])
    with submit_col2:
        submit_btn = st.button(
            "🔍 ANALYZE & REPORT",
            use_container_width=True,
            type="primary",
            key="submit_report"
        )
    
    # ===== ANALYSIS & RESULTS =====
    if submit_btn:
        if active_file and user_notes.strip():
            img_bytes = active_file.read()
            
            with st.spinner("🔄 Analyzing emergency... Please wait..."):
                try:
                    result = analyze_emergency(img_bytes, user_notes, lang)
                    
                    # SEVERITY DISPLAY
                    st.markdown('<div class="section-header">🚨 Analysis Results</div>', unsafe_allow_html=True)
                    
                    severity_colors = {
                        "CRITICAL": "🔴 CRITICAL",
                        "HIGH": "🟠 HIGH",
                        "MEDIUM": "🟡 MEDIUM",
                        "LOW": "🟢 LOW"
                    }
                    
                    result_col1, result_col2 = st.columns(2)
                    
                    with result_col1:
                        severity_display = severity_colors.get(result.severity, result.severity)
                        st.markdown(f"""
                        <div class="danger-box">
                            <h3>Severity Assessment</h3>
                            <div style="font-size: 1.8rem; font-weight: 700; color: #DC143C;">
                                {severity_display}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with result_col2:
                        st.markdown(f"""
                        <div class="warning-box">
                            <h3>Safety Disclaimer</h3>
                            <p>{result.disclaimer}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # IMAGE WITH ANNOTATIONS
                    st.markdown('<div class="section-header">🖼️ Annotated Scene Analysis</div>', unsafe_allow_html=True)
                    annotated_img = draw_bounding_boxes(img_bytes, result.bounding_boxes)
                    st.image(annotated_img, caption="Visual Analysis with Detection Annotations", use_column_width=True)
                    
                    # FIRST AID INSTRUCTIONS
                    st.markdown('<div class="section-header">🏥 First Aid Instructions</div>', unsafe_allow_html=True)
                    for i, step in enumerate(result.first_aid_steps, 1):
                        st.markdown(f"""
                        <div class="instruction-box">
                            <b>Step {i}:</b> {step}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # WARNINGS
                    st.markdown('<div class="section-header">⚠️ Critical: What NOT to Do</div>', unsafe_allow_html=True)
                    for warn in result.what_not_to_do:
                        st.markdown(f"""
                        <div class="danger-box">
                            {warn}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # AUDIO GUIDANCE
                    st.markdown('<div class="section-header">🔊 Audio Guidance</div>', unsafe_allow_html=True)
                    tts = gTTS(text=result.voice_summary, lang='en')
                    fp = BytesIO()
                    tts.write_to_fp(fp)
                    st.audio(fp.getvalue(), format="audio/mp3")
                    
                    # DISPATCH ALERT
                    if result.severity in ["HIGH", "CRITICAL"]:
                        st.markdown('<div class="section-header">📡 Emergency Dispatch</div>', unsafe_allow_html=True)
                        with st.spinner("📞 Contacting emergency services..."):
                            dispatch_res = dispatch_emergency_sos(28.607, 77.213, "Campus Incident", result.severity)
                            if dispatch_res.get('status') == "sent":
                                st.success(f"✅ Emergency SOS DISPATCHED! Status: {dispatch_res.get('status')}")
                                st.info("🚑 Emergency services have been notified. Stay on the line.")
                            else:
                                st.warning(f"ℹ️ Emergency alert logged: {dispatch_res.get('status')}")
                
                except Exception as e:
                    st.warning("⚠️ Online analysis unavailable. Using offline protocols...")
                    offline_response = get_offline_protocol(user_notes)
                    st.markdown(f"""
                    <div class="info-card">
                        <h4>Offline Protocol Response:</h4>
                        <p>{offline_response}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        else:
            if not active_file:
                st.error("❌ Please upload or capture a photo of the emergency scene.")
            if not user_notes.strip():
                st.error("❌ Please describe the emergency situation or symptoms.")

# ===== TAB 2: CAMPUS MAP =====
with tab2:
    st.markdown('<div class="section-header">🗺️ Campus Security Locations</div>', unsafe_allow_html=True)
    
    map_col, info_col = st.columns([3, 1])
    
    with map_col:
        m = folium.Map(
            location=[28.607, 77.213],
            zoom_start=16,
            tiles="OpenStreetMap"
        )
        folium.Marker(
            [28.607, 77.213],
            popup="<b>Campus Security HQ</b><br>Emergency Response Center<br>Available 24/7",
            tooltip="Security Headquarters",
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(m)
        
        folium.Marker(
            [28.610, 77.215],
            popup="<b>Medical Center</b><br>First Aid & Medical Services",
            tooltip="Medical Center",
            icon=folium.Icon(color="green", icon="plus")
        ).add_to(m)
        
        folium.Marker(
            [28.605, 77.210],
            popup="<b>Emergency Assembly Point</b><br>Meet here during emergencies",
            tooltip="Assembly Point",
            icon=folium.Icon(color="blue", icon="flag")
        ).add_to(m)
        
        st_folium(m, width=None, height=500)
    
    with info_col:
        st.markdown("""
        ### 🔴 Security HQ
        **Status**: Active 24/7
        
        **Services:**
        - Emergency Response
        - First Aid
        - Traffic Control
        
        ---
        
        ### 🟢 Medical Center
        **Staff**: Always Available
        
        **Services:**
        - Emergency Treatment
        - Consultation
        - Ambulance
        
        ---
        
        ### 🔵 Assembly Point
        **Location**: Safe Zone
        
        **For**: Evacuations
        """)

# ===== TAB 3: INFORMATION =====
with tab3:
    info_tab1, info_tab2, info_tab3 = st.columns(3)
    
    with info_tab1:
        st.markdown("""
        ### 📚 How to Use
        
        1. **Report Emergency**
           - Upload or take a photo
           - Describe the situation
           - Click analyze
        
        2. **Get Instructions**
           - Follow first aid steps
           - Avoid warnings
           - Listen to audio guide
        
        3. **Emergency Dispatch**
           - Automatic for critical cases
           - Services respond within 5-8 min
           - Stay in safe location
        """)
    
    with info_tab2:
        st.markdown("""
        ### 🆘 When to Use
        
        ✅ **Use This App For:**
        - Injuries & Wounds
        - Allergic Reactions
        - Unconsciousness
        - Accidents
        - Medical Emergencies
        
        ❌ **Call 911 For:**
        - Severe Trauma
        - Loss of Consciousness
        - Difficulty Breathing
        - Chest Pain
        """)
    
    with info_tab3:
        st.markdown("""
        ### 💡 Quick Tips
        
        - 📸 Photo helps analysis
        - 📝 Be specific in description
        - 🎧 Listen to audio guidance
        - 📞 Emergency numbers ready
        - ⏱️ Response time: 5-8 min
        - 📍 Share your location
        """)
    
    st.divider()
    
    st.markdown("""
    <div class="info-card">
        <h3>📋 Emergency Hotlines</h3>
        <p><b>🚑 Ambulance/Medical:</b> 102 or Campus Medical Center</p>
        <p><b>🚨 Police/Security:</b> 100 or Campus Security</p>
        <p><b>🔥 Fire Department:</b> 101</p>
        <p><b>☠️ Poison Control:</b> 1-800-222-1222</p>
    </div>
    """, unsafe_allow_html=True)