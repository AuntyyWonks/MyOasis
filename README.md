# Oasis – Home Garden Plant Assistant

Oasis is a South African-focused home garden advisory platform designed to help households optimize their available space for growing nutritious crops. The platform integrates AI-driven guidance, planting calendars, community crop-sharing, and water-wise solutions to empower users to grow their own food efficiently.

## Features

Personalized Garden Guidance – AI suggests crops based on soil type, water availability, and regional climate.

Localized Planting Calendars – Know exactly when to plant specific crops in your province.

Starter Kits & Tutorials – Affordable seed, soil, and tools paired with digital tutorials in local languages.

Community Crop-Sharing – Connect with neighbors to trade and share harvests.

Water-Wise Gardening – Guides for DIY drip irrigation and affordable soil moisture monitoring.

Gamification – Share your progress, earn badges, and inspire others in your community.

### Prerequisites

Python 3.10+

Node.js & npm

Gemini API key (for AI chat features)

## Quick Start

The included start-oasis.bat script automates the setup:

@echo off
echo ========================================
echo    OASIS - Plant Assistant
echo    Professional Development Environment
echo ========================================
echo.

### Steps Performed by the Script

#### Backend Setup

Creates and activates a Python virtual environment in oasis-serverside.

Installs required Python packages: flask, flask-cors, google-genai, python-dotenv.

Launches the Flask backend in a separate terminal window.

#### Frontend Setup

Waits a few seconds to ensure backend is running.

Starts the Vite React frontend in a new terminal window.

#### Access

Backend API: http://localhost:5000

Frontend UI: http://localhost:3000

####  Open your browser to http://localhost:3000 to start using Oasis.

## Project Structure
oasis/
├─ client/                 # React frontend
├─ oasis-serverside/       # Flask backend
│  ├─ app.py               # Flask app entry
│  ├─ ai_handlers.py       # AI logic for crop suggestions and plant health
│  └─ venv/                # Python virtual environment
└─ start-oasis.bat         # Setup and launch script

### Notes

Make sure your Gemini API key is stored in a .env file in oasis-serverside:

GEMINI_API_KEY=your_api_key_here


The chat AI and crop recommendation features require an active internet connection to communicate with the API.