# SafeDrive AI 🚗

SafeDrive AI is an intelligent driver safety system designed to detect driver drowsiness and prevent road accidents using real-time computer vision.

The system monitors the driver's eyes through a camera and detects signs of fatigue such as prolonged eye closure. When risky behavior is detected, the system triggers progressive alerts and logs the event to a backend server for monitoring and analysis.

---

# Problem

Driver fatigue is one of the leading causes of road accidents worldwide. Many drivers fall asleep or lose focus while driving long distances.

Most current solutions are expensive and only available in premium vehicles.

SafeDrive AI aims to provide an affordable and intelligent driver monitoring solution.

---

# Solution

SafeDrive AI continuously monitors the driver's eyes using a camera and analyzes facial landmarks to detect drowsiness.

The system follows a multi-level alert system:

1. Warning Alert – gentle sound alert
2. Critical Alert – stronger warning sound
3. Emergency Alert – emergency siren + backend logging

This proactive system helps prevent accidents before they occur.

---

# Key Features

• Real-time driver monitoring using camera  
• Automatic calibration for each driver  
• Eye Aspect Ratio (EAR) based drowsiness detection  
• Progressive alert escalation system  
• Emergency siren activation  
• Backend risk logging using FastAPI  
• Risk history storage using MongoDB Atlas  

---

# System Architecture

Camera
↓
OpenCV + MediaPipe (Face Landmark Detection)
↓
Drowsiness Detection Algorithm
↓
Alert System (Warning / Critical / Emergency)
↓
FastAPI Backend
↓
MongoDB Atlas Database


---

# Technologies Used

Python  
OpenCV  
MediaPipe  
FastAPI  
MongoDB Atlas  
Pydantic  
NumPy  

---

# Project Structure

SafeDrive-AI

backend/
database.py
main.py
models.py

ai_engine.py
ambulance.wav
.env
.gitignore


---

# Installation

Clone the repository
git clone https://github.com/SamSana-00/SafeDrive-AI.git
cd SafeDrive-AI
Install required packages
pip install -r requirements.txt

Run the backend server
cd backend
uvicorn main:app --reload

Run the AI detection engine
python ai_engine.py

---

# API Endpoints

### Check backend status

GET /

Returns backend status message.

---

### Log risk data

POST /log-risk

Stores driver fatigue data into MongoDB.

---

### Get history
GET /get-history
Returns stored risk logs.

---

# Future Improvements

• Head pose detection  
• Yawning detection  
• GPS integration for emergency alerts  
• Mobile application integration  
• Vehicle hardware integration  

---

# Author

Samreen Sana  
AI Safety System Project


