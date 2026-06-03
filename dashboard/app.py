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
# AUTO REFRESH
# ------------------------------------------------

st_autorefresh(interval=3000, key="dashboard_refresh")

# ------------------------------------------------
# HEADER
# ------------------------------------------------

st.title("🌊 AI Coastal Guardian")
st.caption("AI-Powered Marine Safety Monitoring System")

st.divider()

# ------------------------------------------------
# CSS
# ------------------------------------------------

st.markdown("""
<style>

.metric-card{
padding:22px;
border-radius:14px;
color:white;
height:130px;
display:flex;
flex-direction:column;
justify-content:center;
box-shadow:0px 6px 18px rgba(0,0,0,0.35);
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
padding:22px;
border-radius:14px;
background:linear-gradient(135deg,#1f2937,#111827);
color:white;
box-shadow:0px 6px 18px rgba(0,0,0,0.35);
}

.log-box{
padding:12px;
border-radius:8px;
background:#1f2937;
margin-bottom:8px;
color:white;
font-size:15px;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# INIT
# ------------------------------------------------

gps = GPSTracker()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
try:
    API_KEY = st.secrets["OPENWEATHER_API_KEY"]
except:
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
# RADAR ROTATION
# ------------------------------------------------

st.session_state.radar_angle = (st.session_state.radar_angle + 12) % 360

# ------------------------------------------------
# LOG FUNCTION
# ------------------------------------------------

def log_event(message):
    timestamp = datetime.now().strftime("%H:%M:%S")

    st.session_state.event_log.insert(0,{
        "time": timestamp,
        "message": message
    })

    st.session_state.event_log = st.session_state.event_log[:7]

# ------------------------------------------------
# GPS
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
# OFFSHORE BOAT SIMULATION
# ------------------------------------------------

boats = [
    {"name":"Boat A","lat":latitude,"lon":longitude}
]

for name in ["Boat B","Boat C","Boat D"]:
    lat_offset = random.uniform(-0.03,0.03)
    lon_offset = random.uniform(-0.18,-0.05)

    boats.append({
        "name":name,
        "lat":latitude + lat_offset,
        "lon":longitude + lon_offset
    })

boat_df = pd.DataFrame(boats)

# ------------------------------------------------
# MAP
# ------------------------------------------------

st.subheader("🚢 Fishing Boats Monitoring Map")

st.map(boat_df.rename(columns={"lat":"lat","lon":"lon"}), zoom=10)

st.info(
    """
ℹ️ Simulation Notice

Boat positions shown on the map are generated using simulated GPS coordinates for demonstration purposes.

Since this prototype currently uses synthetic data instead of real AIS/GPS vessel feeds, some markers may occasionally appear on land or unrealistic locations.

Future versions will integrate real-world maritime tracking data.
"""
)

st.divider()

# ------------------------------------------------
# COLLISION MONITORING
# ------------------------------------------------

st.subheader("⚠ Boat Collision Monitoring")

collision = False

for i in range(len(boats)):
    for j in range(i+1, len(boats)):

        lat_diff = abs(boats[i]["lat"] - boats[j]["lat"])
        lon_diff = abs(boats[i]["lon"] - boats[j]["lon"])

        if lat_diff + lon_diff < 0.01:
            warning = f"Collision risk between {boats[i]['name']} and {boats[j]['name']}"
            st.warning(warning)
            log_event(warning)
            collision = True

if not collision:
    st.success("No collision risks detected")

st.divider()

# ------------------------------------------------
# RADAR
# ------------------------------------------------

st.subheader("📡 Nearby Boat Radar")

angles = []
distance = []

for boat in boats:

    dx = boat["lat"] - latitude
    dy = boat["lon"] - longitude

    angle = math.degrees(math.atan2(dy, dx)) % 360
    dist = math.sqrt(dx**2 + dy**2) * 400

    angles.append(angle)
    distance.append(dist)

fig = go.Figure()

for r in [20,40,60,80,100,120]:
    fig.add_trace(go.Scatterpolar(
        r=[r]*361,
        theta=list(range(361)),
        mode="lines",
        line=dict(color="rgba(0,255,0,0.18)")
    ))

fig.add_trace(go.Scatterpolar(
    r=distance,
    theta=angles,
    mode="markers",
    marker=dict(size=28,color="rgba(0,255,0,0.18)")
))

fig.add_trace(go.Scatterpolar(
    r=distance,
    theta=angles,
    mode="markers+text",
    text=[b["name"] for b in boats],
    textposition="top center",
    marker=dict(size=10,color="lime"),
    hovertemplate="Boat: %{text}<br>Range: %{r:.1f}<extra></extra>"
))

for i in range(5):
    fig.add_trace(go.Scatterpolar(
        r=[0,120],
        theta=[st.session_state.radar_angle-i*2]*2,
        mode="lines",
        line=dict(
            color=f"rgba(0,255,255,{0.45-i*0.08})",
            width=6-i
        )
    ))

fig.update_layout(
polar=dict(
    bgcolor="black",
    radialaxis=dict(visible=False),
    angularaxis=dict(gridcolor="green")
),
height=700,
showlegend=False
)

col1,col2,col3 = st.columns([1,2,1])

with col2:
    st.plotly_chart(fig, width="stretch")

st.divider()

# ------------------------------------------------
# WEATHER CACHE
# ------------------------------------------------

current_time = time.time()

if current_time - st.session_state.last_weather_update > 60:

    st.session_state.weather_data = weather_api.get_weather(latitude, longitude)
    st.session_state.last_weather_update = current_time
    log_event("Weather data updated")

weather_data = st.session_state.weather_data

if weather_data is None:
    st.error(
        "Unable to retrieve weather data. Check OpenWeather API configuration."
    )
    st.stop()

wave_height = weather_data["wind_speed"] * 0.1

# ------------------------------------------------
# SEA CONDITION CARDS
# ------------------------------------------------

st.subheader("🌊 Sea Conditions")

c1,c2 = st.columns(2)
c3,c4 = st.columns(2)

with c1:
    st.markdown(f"""
    <div class="metric-card" style="background:#ef4444;">
    <div class="metric-title">Temperature</div>
    <div class="metric-value">{weather_data['temperature']} °C</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card" style="background:#2563eb;">
    <div class="metric-title">Wind Speed</div>
    <div class="metric-value">{weather_data['wind_speed']} m/s</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card" style="background:#16a34a;">
    <div class="metric-title">Pressure</div>
    <div class="metric-value">{weather_data['pressure']} hPa</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card" style="background:#eab308;">
    <div class="metric-title">Wave Height</div>
    <div class="metric-value">{round(wave_height,2)} m</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ------------------------------------------------
# GOLDEN WIND COMPASS
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

<div style="margin-top:10px;font-size:24px;color:#7df9ff;">
Wind Direction: {wind_direction}°
</div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ------------------------------------------------
# RISK ENGINE
# ------------------------------------------------

prediction, explanation, risk_level = risk_agent.assess(
    model,
    risk_engine,
    weather_data,
    wave_height
)

risk_map = {"LOW":1,"MEDIUM":2,"HIGH":3}
st.session_state.risk_history.append(risk_map[risk_level])

st.subheader("⚠ Risk Assessment")

if risk_level == "HIGH":
    st.error("HIGH RISK — Dangerous sea conditions")
elif risk_level == "MEDIUM":
    st.warning("MEDIUM RISK — Fishermen should stay cautious")
else:
    st.success("LOW RISK — Safe sea conditions")

st.divider()

# ------------------------------------------------
# RISK GAUGE
# ------------------------------------------------

st.subheader("⚠ Risk Level Gauge")

# Convert categorical risk to numerical score
risk_score_map = {
    "LOW": 25,
    "MEDIUM": 55,
    "HIGH": 85
}

value = risk_score_map[risk_level]

# ------------------------------------------------
# RISK SUMMARY
# ------------------------------------------------

col1, col2 = st.columns([1, 2])

with col1:
    st.metric(
    label="Current Risk Level",
    value=risk_level,
    delta=f"{value}% Risk Score"
    )

with col2:
    if risk_level == "LOW":
        st.success(
            "🟢 Low Risk Sea Conditions — Fishing operations can proceed normally."
        )

    elif risk_level == "MEDIUM":
        st.warning(
            "🟡 Moderate Risk Sea Conditions — Extra caution is recommended."
        )

    else:
        st.error(
            "🔴 High Risk Sea Conditions — Fishing activity should be avoided."
        )

# ------------------------------------------------
# GAUGE CHART
# ------------------------------------------------

fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=value,

    title={
        "text": "Sea Risk Score",
        "font": {"size": 24}
    },

    number={
        "suffix": "%",
        "font": {"size": 48}
    },

    gauge={
        "axis": {
            "range": [0, 100],
            "tickwidth": 1,
            "tickcolor": "white"
        },

        "bar": {
            "color": "white",
            "thickness": 0.30
        },

        "steps": [
            {
                "range": [0, 40],
                "color": "green"
            },
            {
                "range": [40, 70],
                "color": "yellow"
            },
            {
                "range": [70, 100],
                "color": "red"
            }
        ],

        "threshold": {
            "line": {
                "color": "white",
                "width": 4
            },
            "thickness": 0.75,
            "value": value
        }
    }
))

fig.update_layout(
    height=350,

    margin=dict(
        l=40,
        r=40,
        t=80,
        b=20
    ),

    paper_bgcolor="#0E1117",
    plot_bgcolor="#0E1117",

    font=dict(
        color="white",
        size=16
    )
)

st.plotly_chart(fig, width="stretch")

st.caption(
    f"AI Risk Score: {value}% ({risk_level}) • Calculated using wind speed, atmospheric pressure, estimated wave conditions, and the maritime risk assessment engine."
)

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