# 🧭 Navisight

**Navisight** is a prototype assistive navigation system designed to help **visually challenged individuals** navigate their surroundings more safely. The project focuses on **obstacle detection, distance estimation, and navigation assistance** using a **software-first approach**.

This project validates the core idea through backend logic and frontend testing before moving toward full hardware implementation.

---

## 🎯 Problem Statement

Visually challenged individuals often face difficulties while navigating unfamiliar environments due to the lack of real-time obstacle awareness. Many existing assistive solutions are either expensive, hardware-dependent, or limited in flexibility.

Navisight aims to explore a **cost-effective and scalable solution** by first validating the navigation logic at the software level, enabling rapid prototyping before investing in physical hardware.

---

## 💡 Project Overview

- Navisight is currently a **software prototype**
- No physical sensors or embedded hardware are used
- Obstacle detection and navigation logic are validated using a **device camera**
- Backend processes visual input and generates navigation feedback
- Frontend is used to simulate real-world interaction

Future plans include integrating **GPS, maps, and physical sensors**, which are currently on hold.

---

## 🧠 How Navisight Works

1. A front-facing camera captures real-time visual input.
2. Backend modules process frames for obstacle detection.
3. Distance estimation logic calculates obstacle proximity.
4. Navigation logic determines safe movement directions.
5. Voice and feedback modules generate user guidance.
6. Frontend simulates interaction and output for testing.

---

## 🧩 Project Structure

navisight/
│
├── ml/
│ ├── detection.py
│ ├── navigation.py
│ ├── scene_segmentation.py
│ ├── tts.py
│ └── voice_command.py
│
├── routes/
│ ├── vision.py
│ ├── navigation.py
│ ├── voice.py
│ └── route.py
│
├── services/
│
├── static/
├── templates/
│
├── app.py
├── main.py
├── requirements.txt
├── README.md
└── .gitignore




---

## 🛠️ Technologies Used

- Python
- Flask
- Computer Vision concepts
- REST APIs
- Camera-based input simulation
- Text-to-Speech concepts

---

