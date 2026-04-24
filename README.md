# AI Coastal Guardian 🌊⚓

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Machine Learning](https://img.shields.io/badge/AI-Machine%20Learning-orange)
![Dashboard](https://img.shields.io/badge/Dashboard-Streamlit-red)
![Status](https://img.shields.io/badge/Status-Functional%20Prototype-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green.svg)

AI Coastal Guardian is an AI-powered maritime safety monitoring system designed to improve the safety of small-scale fishermen.

The platform predicts dangerous sea conditions using machine learning, monitors nearby fishing boats, detects collision risks, and provides a real-time operational dashboard for marine safety awareness.

This project combines **Artificial Intelligence, GPS tracking, weather intelligence, agent-based decision systems, radar visualization, and real-time monitoring** to create a smart safety assistant for coastal fishing operations.

---

## 🎯 Project Goal

Build an intelligent marine safety platform that helps fishermen by:

- Predicting dangerous sea conditions
- Monitoring live boat location and surroundings
- Detecting nearby boat collision risks
- Alerting fishermen when risks are detected
- Supporting emergency distress communication
- Improving coastal fishing safety using AI

---

## 🚀 Implemented Features

### 🌊 AI Sea Danger Prediction

Machine learning model predicts sea risk levels using:

- Wind speed
- Atmospheric pressure
- Wave height

### 📍 GPS Boat Tracking

Simulated GPS system tracks boat coordinates in real time.

### 🌦 Live Weather Integration

Weather data fetched using OpenWeather API.

### 🤖 Agent-Based AI System

Multiple intelligent agents collaborate:

- **Monitoring Agent** – observes environmental conditions  
- **Risk Agent** – evaluates danger level  
- **Safety Agent** – generates warnings and responses  

### 📡 Maritime Radar Dashboard

Real-time radar system showing nearby boats with:

- Sweep animation
- Boat targets
- Relative distance plotting

### ⚠ Collision Detection

Nearby boats are analyzed and collision warnings are triggered automatically.

### 🧭 Wind Direction Compass

Live compass panel showing simulated wind direction.

### 📊 Monitoring Dashboard (Streamlit)

Interactive dashboard includes:

- Boat map
- Weather cards
- Radar system
- Risk gauge
- Risk trend chart
- Event log
- Collision alerts

### 🧠 Explainable AI

Feature influence scores explain model decisions.

### 📋 Event Logging

System events such as:

- Weather updates
- Collision warnings
- Monitoring alerts

---

## 🛠 Technology Stack

| Category | Technology |
|----------|------------|
| Language | Python |
| AI / ML | Scikit-learn |
| Dashboard | Streamlit |
| Visualization | Plotly |
| API | OpenWeather API |
| Data | Pandas |
| Config | Python-dotenv |

---

## 📂 Project Structure

```text
COSTA_GUARDO/
│
├── agents/
│   ├── monitoring_agent.py
│   ├── risk_agent.py
│   └── safety_agent.py
│
├── communication/
│   └── distress_signal.py
│
├── dashboard/
│   └── app.py
│
├── data/
│   └── weather_api.py
│
├── gps/
│   └── gps_tracker.py
│
├── models/
│   └── sea_danger_model.py
│
├── utils/
│   └── risk_engine.py
│
├── main.py
├── requirements.txt
└── README.md
```

---

## ▶ How to Run

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Main System

```bash
python main.py
```

### Run Dashboard

```bash
streamlit run dashboard/app.py
```

---

## 📌 Current Status

✅ Functional prototype completed

Current capabilities:

- AI prediction system
- Real-time dashboard
- Radar visualization
- Collision monitoring
- Risk analytics
- Event logging

Planned future enhancements:

- Better boat movement simulation
- Real hardware GPS support
- Distress communication upgrades
- Offshore route intelligence

---

## 📈 Resume Value Highlights

This project demonstrates:

- Applied AI
- Real-time monitoring systems
- Dashboard engineering
- API integration
- Simulation systems
- Risk analytics
- Product-oriented development

---

## 👨‍💻 Author

B.Tech AI & Data Science Project  
Focused on improving safety for coastal fishermen communities.

---

## 📄 License

This project is licensed under the MIT License.