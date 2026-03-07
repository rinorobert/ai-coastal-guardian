import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random
import math
import time
from datetime import datetime

from gps.gps_tracker import GPSTracker
from data.weather_api import WeatherAPI
from models.sea_danger_model import SeaDangerModel
from utils.risk_engine import RiskEngine
from agents.risk_agent import RiskAgent

from streamlit_autorefresh import st_autorefresh
from dotenv import load_dotenv

load_dotenv()

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------

st.set_page_config(
    page_title="AI Coastal Guardian",
    page_icon="🌊",
    layout="wide"
)

# ------------------------------------------------
# SAFE REFRESH (3 SECONDS)
# ------------------------------------------------

st_autorefresh(interval=3000, key="dashboard_refresh")

# ------------------------------------------------
# HEADER
# ------------------------------------------------

st.title("🌊 AI Coastal Guardian")
st.caption("AI-Powered Marine Safety Monitoring System")

st.divider()

# ------------------------------------------------
# STYLES
# ------------------------------------------------

st.markdown("""
<style>

.metric-card{
padding:20px;
border-radius:12px;
color:white;
height:120px;
display:flex;
flex-direction:column;
justify-content:center;
box-shadow:0px 5px 15px rgba(0,0,0,0.4);
}

.metric-title{
font-size:16px;
opacity:0.9;
}

.metric-value{
font-size:30px;
font-weight:bold;
}

.location-card{
padding:20px;
border-radius:12px;
background:linear-gradient(135deg,#1f2937,#111827);
color:white;
box-shadow:0px 5px 15px rgba(0,0,0,0.4);
}

.log-box{
padding:10px;
border-radius:6px;
background:#1f2937;
margin-bottom:6px;
color:white;
font-size:14px;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# SYSTEM INIT
# ------------------------------------------------

gps = GPSTracker()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
weather_api = WeatherAPI(API_KEY)

risk_engine = RiskEngine()
risk_agent = RiskAgent()

@st.cache_resource
def load_model():
    model = SeaDangerModel()
    model.train()
    return model

model = load_model()

# ------------------------------------------------
# SESSION STATE
# ------------------------------------------------

if "event_log" not in st.session_state:
    st.session_state.event_log = []

if "risk_history" not in st.session_state:
    st.session_state.risk_history = []

if "weather_data" not in st.session_state:
    st.session_state.weather_data = None

if "last_weather_update" not in st.session_state:
    st.session_state.last_weather_update = 0

if "radar_angle" not in st.session_state:
    st.session_state.radar_angle = 0

# ------------------------------------------------
# RADAR SWEEP UPDATE
# ------------------------------------------------

st.session_state.radar_angle = (st.session_state.radar_angle + 8) % 360

# ------------------------------------------------
# EVENT LOG FUNCTION
# ------------------------------------------------

def log_event(message):

    timestamp = datetime.now().strftime("%H:%M:%S")

    st.session_state.event_log.insert(0,{
        "time":timestamp,
        "message":message
    })

    st.session_state.event_log = st.session_state.event_log[:7]

# ------------------------------------------------
# GPS LOCATION
# ------------------------------------------------

latitude, longitude = gps.get_location()

# ------------------------------------------------
# LOCATION CARD
# ------------------------------------------------

st.subheader("📍 Boat Location")

st.markdown(f"""
<div class="location-card">
<h3>Latitude: {round(latitude,4)}</h3>
<h3>Longitude: {round(longitude,4)}</h3>
</div>
""", unsafe_allow_html=True)

st.divider()

# ------------------------------------------------
# BOAT SIMULATION
# ------------------------------------------------

boats = [
{"name":"Boat A","lat":latitude,"lon":longitude},
{"name":"Boat B","lat":latitude + random.uniform(-0.1,0.1),"lon":longitude + random.uniform(-0.1,0.1)},
{"name":"Boat C","lat":latitude + random.uniform(-0.1,0.1),"lon":longitude + random.uniform(-0.1,0.1)},
{"name":"Boat D","lat":latitude + random.uniform(-0.1,0.1),"lon":longitude + random.uniform(-0.1,0.1)}
]

boat_df = pd.DataFrame(boats)

# ------------------------------------------------
# MAP
# ------------------------------------------------

st.subheader("🚢 Fishing Boats Monitoring Map")

st.map(boat_df.rename(columns={"lat":"lat","lon":"lon"}), zoom=12)

st.divider()

# ------------------------------------------------
# COLLISION DETECTION
# ------------------------------------------------

st.subheader("⚠ Boat Collision Monitoring")

collision=False

for i in range(len(boats)):
    for j in range(i+1,len(boats)):

        lat_diff=abs(boats[i]["lat"]-boats[j]["lat"])
        lon_diff=abs(boats[i]["lon"]-boats[j]["lon"])

        if lat_diff+lon_diff < 0.01:

            warning=f"Collision risk between {boats[i]['name']} and {boats[j]['name']}"
            st.warning(warning)

            log_event(warning)

            collision=True

if not collision:
    st.success("No collision risks detected")

st.divider()

# ------------------------------------------------
# RADAR DISPLAY
# ------------------------------------------------

st.subheader("📡 Nearby Boat Radar")

angles=[]
distance=[]

for boat in boats:

    dx=boat["lat"]-latitude
    dy=boat["lon"]-longitude

    angle=math.degrees(math.atan2(dy,dx))%360
    dist=math.sqrt(dx**2+dy**2)*100

    angles.append(angle)
    distance.append(dist)

fig=go.Figure()

# radar rings
for r in [20,40,60,80,100,120]:
    fig.add_trace(go.Scatterpolar(
        r=[r]*361,
        theta=list(range(361)),
        mode="lines",
        line=dict(color="rgba(0,255,0,0.2)")
    ))

# boat glow
fig.add_trace(go.Scatterpolar(
    r=distance,
    theta=angles,
    mode="markers",
    marker=dict(size=30,color="rgba(0,255,0,0.2)")
))

# boat targets
fig.add_trace(go.Scatterpolar(
    r=distance,
    theta=angles,
    mode="markers+text",
    text=[b["name"] for b in boats],
    marker=dict(size=10,color="lime")
))

# radar sweep
for i in range(5):

    fig.add_trace(go.Scatterpolar(
        r=[0,120],
        theta=[st.session_state.radar_angle-i*2]*2,
        mode="lines",
        line=dict(
            color=f"rgba(0,255,255,{0.4-i*0.08})",
            width=6-i
        )
    ))

fig.update_layout(
polar=dict(
bgcolor="black",
radialaxis=dict(visible=False),
angularaxis=dict(gridcolor="green")
),
height=750,
showlegend=False
)

col1,col2,col3 = st.columns([1,2,1])

with col2:
    st.plotly_chart(fig,use_container_width=True)

st.divider()

# ------------------------------------------------
# WEATHER UPDATE (EVERY 60 SECONDS)
# ------------------------------------------------

current_time=time.time()

if current_time - st.session_state.last_weather_update > 60:

    st.session_state.weather_data = weather_api.get_weather(latitude,longitude)
    st.session_state.last_weather_update = current_time

    log_event("Weather data updated")

weather_data = st.session_state.weather_data

if weather_data is None:
    st.stop()

# ------------------------------------------------
# SEA CONDITIONS
# ------------------------------------------------

wave_height = weather_data["wind_speed"] * 0.1

st.subheader("🌊 Sea Conditions")

col1,col2,col3,col4 = st.columns(4)

col1.metric("Temperature",f"{weather_data['temperature']} °C")
col2.metric("Wind Speed",f"{weather_data['wind_speed']} m/s")
col3.metric("Pressure",f"{weather_data['pressure']} hPa")
col4.metric("Wave Height",f"{round(wave_height,2)} m")

st.divider()

# ------------------------------------------------
# WIND COMPASS
# ------------------------------------------------

st.subheader("🧭 Wind Direction")

wind_direction = random.randint(0,360)

compass_image = "https://thumbs.dreamstime.com/b/golden-compass-background-outer-space-golden-compass-background-outer-space-332541955.jpg"

st.markdown(f"""
<div style="text-align:center;">
<div style="
position:relative;
width:420px;
height:420px;
margin:auto;
background:url('{compass_image}');
background-size:cover;
border-radius:50%;
">

<div style="
position:absolute;
top:50%;
left:50%;
width:5px;
height:170px;
background:linear-gradient(to top,#00eaff,#7df9ff);
transform-origin:bottom center;
transform: translate(-50%, -100%) rotate({wind_direction}deg);
"></div>

<div style="
position:absolute;
top:50%;
left:50%;
width:16px;
height:16px;
background:white;
border-radius:50%;
transform:translate(-50%,-50%);
"></div>

<div style="position:absolute; top:10px; left:50%; transform:translateX(-50%); color:white;">N</div>
<div style="position:absolute; right:10px; top:50%; transform:translateY(-50%); color:white;">E</div>
<div style="position:absolute; bottom:10px; left:50%; transform:translateX(-50%); color:white;">S</div>
<div style="position:absolute; left:10px; top:50%; transform:translateY(-50%); color:white;">W</div>

</div>

<div style="margin-top:10px;font-size:26px;color:#7df9ff;">
Wind Direction: {wind_direction}°
</div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ------------------------------------------------
# AI RISK ENGINE
# ------------------------------------------------

prediction, explanation, risk_level = risk_agent.assess(
model,
risk_engine,
weather_data,
wave_height
)

risk_map={"LOW":1,"MEDIUM":2,"HIGH":3}
st.session_state.risk_history.append(risk_map[risk_level])

st.subheader("⚠ Risk Assessment")

if risk_level=="HIGH":
    st.error("HIGH RISK — Dangerous sea conditions")

elif risk_level=="MEDIUM":
    st.warning("MEDIUM RISK — Fishermen should stay cautious")

else:
    st.success("LOW RISK — Safe sea conditions")

st.divider()

# ------------------------------------------------
# RISK GAUGE
# ------------------------------------------------

st.subheader("⚠ Risk Level Gauge")

value={"LOW":20,"MEDIUM":60,"HIGH":90}[risk_level]

fig=go.Figure(go.Indicator(
mode="gauge+number",
value=value,
title={'text':"Sea Risk Level"},
gauge={'axis':{'range':[0,100]},
'steps':[{'range':[0,40],'color':"green"},
{'range':[40,70],'color':"yellow"},
{'range':[70,100],'color':"red"}]}
))

st.plotly_chart(fig,use_container_width=True)

st.divider()

# ------------------------------------------------
# RISK TREND
# ------------------------------------------------

st.subheader("📈 Sea Risk Trend")

trend=pd.DataFrame({"risk":st.session_state.risk_history})

fig=go.Figure()

fig.add_trace(go.Scatter(
y=trend["risk"],
mode="lines+markers",
line=dict(color="cyan",width=3)
))

fig.update_layout(
yaxis=dict(tickvals=[1,2,3],ticktext=["LOW","MEDIUM","HIGH"]),
height=350
)

st.plotly_chart(fig,use_container_width=True)

st.divider()

# ------------------------------------------------
# EVENT LOG
# ------------------------------------------------

st.subheader("📡 System Event Log")

for event in st.session_state.event_log:

    st.markdown(f"""
<div class="log-box">
[{event['time']}] {event['message']}
</div>
""", unsafe_allow_html=True)