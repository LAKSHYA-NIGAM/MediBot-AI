# MediBot-AI — Intelligent Medical Chatbot with RAG & Multimodal Vision

[![CI](https://github.com/LAKSHYA-NIGAM/MediBot-AI/actions/workflows/ci.yml/badge.svg)](https://github.com/LAKSHYA-NIGAM/MediBot-AI/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1-black.svg)](https://flask.palletsprojects.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Store-orange.svg)](https://www.trychroma.com/)
[![Google Gemini](https://img.shields.io/badge/Google_Gemini-2.5_Flash-4285F4.svg)](https://ai.google.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An intelligent medical assistant powered by **Retrieval-Augmented Generation (RAG)**, **Google Gemini 2.5 Flash**, **ChromaDB**, and **Flask**. MediBot provides educational answers on symptoms, diseases, medications, first aid, and lifestyle health backed by verified medical literature, alongside multimodal medical image analysis and PDF report comprehension.

> ⚠️ **Medical Disclaimer:** MediBot-AI is an educational AI assistant and is NOT a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of a qualified healthcare provider for any medical condition.

---

## Key Features

- **Retrieval-Augmented Generation (RAG)**: Uses ChromaDB vector embeddings generated from medical literature to ground LLM responses with factual context.
- **Multimodal Medical Vision**: Upload medical scans, dermatology images, or clinical diagrams for Gemini 2.5 vision analysis.
- **Document Understanding**: Upload medical records and lab report PDFs for contextual document Q&A.
- **Secure Authentication**: Built-in user registration, bcrypt password hashing, and session management.
- **Chat History & Persistence**: SQLite storage tracking conversational context per user account with clear-history controls.
- **Automated Health Monitoring**: `/health` endpoint for container orchestration and uptime verification.

---

## System Architecture

```text
User / Browser
   │
   ├── (1) Authentication & Session Guard (Flask + SQLite)
   │
   ├── (2) Multimodal Upload Handler (PDF / Image / Text)
   │
   └── (3) Retrieval-Augmented Generation (RAG)
             ├── ChromaDB Vector Store (Medical Knowledge Base)
             ├── HuggingFace MiniLM Embeddings
             └── Google Gemini 2.5 Flash LLM Chain
```

---

## Technology Stack

- **Backend**: Python 3.10+, Flask, SQLite
- **AI & RAG**: LangChain, ChromaDB, Google Gemini 2.5 Flash (`google-genai` & `langchain-google-genai`), HuggingFace Sentence Transformers
- **Document & Vision**: PyPDF, Pillow (PIL)
- **Security**: Werkzeug security password hashing, CSRF session guards, file extension sanitization

---

## Quick Start & Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/LAKSHYA-NIGAM/MediBot-AI.git
cd MediBot-AI
```

### 2. Set Up Virtual Environment

```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On Linux / macOS
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```ini
GOOGLE_API_KEY="your-gemini-api-key"
SECRET_KEY="your-random-flask-secret-key"
PORT=8080
```

### 5. Launch the Application

```bash
python app.py
```

Open [http://localhost:8080](http://localhost:8080) in your browser.

---

## Automated Testing

MediBot-AI includes an automated 13-test verification suite covering authentication flows, session handling, file extension security filters, prompt consistency, and service health:

```bash
# Run unit test suite
python -m unittest discover tests
```

### Test Coverage Highlights:
- **`test_auth.py` (8 tests)**: User registration, password confirmation verification, minimum length enforcement (>= 6 chars), duplicate credential rejection, login validation, session termination, and chronological SQLite chat history ordering.
- **`test_app.py` (5 tests)**: Container `/health` status endpoint, security file extension whitelisting (`.pdf`, `.png`, `.jpg`, `.txt`), unauthenticated redirect guards, and system prompt safety disclaimer verification.

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
