import streamlit.components.v1 as components

def render_panic_alarm():
    js_code = """
    <script>
    function triggerSiren() {
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = audioCtx.createOscillator();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(1000, audioCtx.currentTime);
        osc.connect(audioCtx.destination);
        osc.start();
        setTimeout(() => osc.stop(), 3000);
    }
    triggerSiren();
    </script>
    <div style="padding: 10px; background-color: #ff4b4b; color: white; text-align: center; border-radius: 5px; font-weight: bold;">
        🚨 PANIC ALARM ACTIVATED 🚨
    </div>
    """
    components.html(js_code, height=60)