import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Metrónomo", layout="centered")

st.title("Metrónomo ajustable")

st.write("Selecciona los BPM y usa los botones para iniciar y detener.")

bpm = st.slider("BPM", min_value=30, max_value=240, value=100, step=1)

html_code = f"""
<div style="font-family: sans-serif">
  <h3>Metrónomo</h3>
  <p>BPM actual: <strong>{bpm}</strong></p>
  <button id="start">Iniciar</button>
  <button id="stop">Detener</button>
  <p>Cada tercer pulso tiene acento.</p>
</div>
<script>
  let bpm = {bpm};
  let interval = 60000 / bpm;
  let beat = 0;
  let timer = null;
  let audioCtx = null;

  function getAudioCtx() {{
    if (!audioCtx) {{
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      audioCtx = new AudioContext();
    }}
    return audioCtx;
  }}

  function click(accent) {{
    const ctx = getAudioCtx();
    if (ctx.state === "suspended") {{
      ctx.resume();
    }}

    const osc = ctx.createOscillator();
    const gainNode = ctx.createGain();

    osc.frequency.value = accent ? 880 : 440;
    gainNode.gain.setValueAtTime(1, ctx.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.1);

    osc.connect(gainNode);
    gainNode.connect(ctx.destination);

    osc.start();
    osc.stop(ctx.currentTime + 0.1);
  }}

  function startMetronome() {{
    if (timer) return;

    beat = 1;
    click(false);

    timer = setInterval(() => {{
      beat = beat + 1;
      const accent = (beat % 3) === 0;
      click(accent);
    }}, interval);
  }}

  function stopMetronome() {{
    if (timer) {{
      clearInterval(timer);
      timer = null;
    }}
  }}

  document.getElementById("start").onclick = () => {{
    startMetronome();
  }};

  document.getElementById("stop").onclick = () => {{
    stopMetronome();
  }};
</script>
"""

components.html(html_code, height=240)
 