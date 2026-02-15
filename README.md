🚀 Real-Time Notification System
Apache Kafka + Redis + JWT + Docker
📌 Project Overview

This project implements a real-time notification system using Apache Kafka and Redis.
It was developed as part of the Data Managing (Upravljanje podacima) course.

The system demonstrates event-driven communication, token-based authentication, and containerized deployment.

🏗 System Architecture

The application follows an event-driven architecture:

User (Web UI)
        │
        ▼
Flask API (JWT Authentication)
        │
        ├── Kafka Producer → Topic: notifications
        ▼
Kafka Broker
        ▼
Worker (Kafka Consumer)
        ▼
Redis (Storage + Unread Counter)
🔹 Components
Component	Role
Flask API	REST API and JWT authentication
Kafka	Event streaming and message broker
Worker	Consumes events and processes notifications
Redis	Stores user notifications and unread counters
Docker	Containerized multi-service deployment
🔐 Authentication

The system uses:

Short-lived Access Token

Long-lived Refresh Token (HttpOnly cookie)

Automatic token refresh mechanism

Secure logout process

📦 Features

User registration

User login

JWT-based authentication

Real-time notification processing

Kafka event publishing

Kafka consumer worker

Redis-based message storage

Unread notification counter

Mark notifications as read

Clear all notifications

Dockerized environment

🛠 Technologies Used

Python (Flask)

Apache Kafka

Redis

Flask-JWT-Extended

Docker & Docker Compose

HTML / CSS / JavaScript

▶️ How to Run the Project
1️⃣ Start all services
docker compose up --build
2️⃣ Open the application
http://localhost:5000
📡 Example Kafka Event
{
  "type": "NOTIFICATION_CREATED",
  "to_user": "mateo",
  "from_user": "monika",
  "message": "Hello!",
  "ts": 1771191122
}
📂 Project Structure
rt-notify/
│
├── app/
│   ├── auth.py
│   ├── notifications.py
│   ├── main.py
│   ├── redis_client.py
│   └── static/
│       ├── app.js
│       └── styles.css
│
├── worker/
│   └── worker.py
│
├── docker-compose.yml
├── Dockerfile
└── README.md
🎓 Academic Requirements Fulfilled

✔ Apache Kafka integration
✔ Redis usage
✔ Real-time communication
✔ Authentication (login & registration)
✔ Docker deployment
✔ Web-based user interface

👨‍🎓 Course Information

Course: Data Management (Upravljanje podacima)
Year: 2026