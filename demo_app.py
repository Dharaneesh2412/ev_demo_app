import streamlit as st
import random
import time
from datetime import datetime

st.set_page_config(page_title="EV Green Corridor Demo", layout="wide")
st.title("🚑 EV Green Corridor — Demo App (IoT GPS + Camera + Sensors)")

# --- Route ---
INTERSECTIONS = ["Junction A", "Junction B", "Junction C", "Hospital"]
NUM = len(INTERSECTIONS)

# --- State ---
if "pos" not in st.session_state:
    st.session_state.pos = 0
if "logs" not in st.session_state:
    st.session_state.logs = []
if "preempt" not in st.session_state:
    st.session_state.preempt = set()

def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    st.session_state.logs.insert(0, f"[{ts}] {msg}")

def schedule_preempt(idx, lookahead=1):
    end = min(NUM-1, idx+lookahead)
    for i in range(idx, end+1):
        st.session_state.preempt.add(i)
    log(f"Preemption: {', '.join(INTERSECTIONS[i] for i in st.session_state.preempt)}")

# --- UI ---
st.subheader("Controls")
col1, col2 = st.columns([1,2])

with col1:
    if st.button("🚑 Start Ambulance (reset)"):
        st.session_state.pos = 0
        st.session_state.preempt.clear()
        st.session_state.logs.clear()
        log("Ambulance started from Junction A")

    if st.button("➡️ Move Forward"):
        if st.session_state.pos < NUM-1:
            st.session_state.pos += 1
            log(f"Ambulance reached {INTERSECTIONS[st.session_state.pos]}")
        else:
            st.success("✅ Ambulance reached Hospital!")
            log("Ambulance reached Hospital")

    st.markdown("---")
    st.write("### Simulate Detection")
    if st.button("📡 IoT GPS"):
        schedule_preempt(st.session_state.pos+1, lookahead=2)
    if st.button("📷 Camera AI"):
        schedule_preempt(st.session_state.pos+1, lookahead=1)
    if st.button("🔦 Sensor RFID/IR"):
        schedule_preempt(st.session_state.pos, lookahead=0)

    st.markdown("---")
    st.write("### Simulated GPS")
    lat = 12.9716 + random.uniform(-0.001, 0.001)
    lon = 77.5946 + random.uniform(-0.001, 0.001)
    st.write(f"Lat: {lat:.6f}, Lon: {lon:.6f}")

with col2:
    st.write("### Traffic Signals")
    cols = st.columns(NUM)
    for i, name in enumerate(INTERSECTIONS):
        if i == st.session_state.pos:
            cols[i].metric(name, "🟢 EV Present")
        elif i in st.session_state.preempt:
            cols[i].metric(name, "🟢 Preempted")
        else:
            cols[i].metric(name, "🔴 Normal")

    st.write("### Logs")
    if st.session_state.logs:
        st.text("\n".join(st.session_state.logs[:10]))
    else:
        st.text("No events yet")
