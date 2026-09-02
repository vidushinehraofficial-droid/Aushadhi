# Aushadhi
# 🚨 Accessible Multimodal Campus Health & Safety Companion

An AI-powered emergency response and multimodal triage platform engineered for campus safety. Built with **Gemini 2.5 Flash**, **Streamlit**, **Twilio**, and **Folium**, this system provides immediate visual injury grounding, voice-assisted first-aid guidance, panic sirens, automated emergency dispatch, and offline fallback resilience.

---

## Key Features

* 🤖 **AI-Powered Visual Triage (`Gemini 2.5 Flash`)**: Analyzes scene images and patient context to evaluate severity (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`), generate step-by-step first-aid guidance, and flag critical warnings.
* 🎯 **Visual Grounding & Bounding Box Overlay**: Draws high-contrast rectangular bounding boxes on emergency images to highlight specific injuries or environmental hazards.
* 🔊 **Multilingual Voice Accessibility**: Automatically generates and streams audio summaries in target languages (English, Spanish, Hindi, French) using `gTTS`.
* 🚨 **Panic Siren & Visual Strobe**: Triggers a high-frequency 1000Hz audio siren via Web Audio API and a full-screen flashing strobe overlay for immediate localized help.
* 📲 **Automated Emergency SOS Dispatch**: Sends SMS alerts with live Google Maps coordinates to campus security via Twilio whenever `HIGH` or `CRITICAL` severity is detected.
* 📡 **Offline Fallback Protocol**: Features a zero-network resilience engine backed by pre-loaded Red Cross procedures for emergency situations with lost connectivity.
* 🗺️ **GIS Campus Mapping**: Interactive Folium map pinning real-time user coordinates relative to campus emergency response stations.

---

## Repository Structure

```text
.
├── config/
│   └── settings.py              # Pydantic-based environment configuration
├── core/
│   ├── spatial_triage.py        # Gemini 2.5 Flash SDK integration & JSON schema validation
│   └── visualizer.py            # PIL bounding box overlay generator
├── tools/
│   ├── campus_dispatch.py       # Twilio SMS dispatcher & Google Maps URL builder
│   └── panic_system.py          # Web Audio API siren & strobe alert components
├── offline/
│   ├── fallback_protocols.json  # Pre-compiled emergency response procedures
│   └── manager.py               # Fuzzy-matching offline protocol fallback engine
├── tests/
│   └── test_app.py              # Pytest unit testing suite
├── .env.example                 # Environment variables template
├── app.py                       # Main Streamlit web frontend
├── requirements.txt             # Project Python dependencies
└── README.md                    # System documentation

