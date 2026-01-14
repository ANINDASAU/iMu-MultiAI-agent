# 🎓 University Assistant - AI-Powered Multi-Agent System

> An intelligent student query management system that routes student questions to the right university department using AI-powered classification and automated Relay.app workflows.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128-green)
![React](https://img.shields.io/badge/React-18.2-cyan?logo=react)
![Vite](https://img.shields.io/badge/Vite-5.1-purple?logo=vite)
![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-blue)
![Gemini](https://img.shields.io/badge/Google-Gemini-orange)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [Architecture](#architecture)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Webhook Integration](#webhook-integration)
- [Security](#security)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

The **University Assistant** is an intelligent chatbot system that helps students get answers and route their queries to the appropriate university department. It uses:

- **Google Gemini LLM** for intelligent query classification and tone detection
- **Multi-agent Relay.app automations** for handling different unit workflows
- **Supabase PostgreSQL** for persistent storage
- **FastAPI** backend for conversation management
- **React + Vite** frontend for a responsive chat interface

The system collects student information (name, academic year, query) and intelligently routes it to one of 4 units:
1. **Admission & Financial Aid Unit** (scholarships, fees, eligibility)
2. **Academic Support Unit** (exams, syllabus, courses)
3. **Student Welfare & Counseling Unit** (mental health, stress management)
4. **Career & Skill Development Unit** (internships, jobs, skills)

---

## ✨ Features

✅ **AI-Powered Query Classification** — Uses Google Gemini to understand student intent and tone  
✅ **Multi-Unit Routing** — Directs queries to the correct department via dedicated webhooks  
✅ **Conversational Flow** — Collects student name → academic year → query step-by-step  
✅ **Tone & Urgency Detection** — Flags urgent/emergency queries for priority handling  
✅ **Persistent Storage** — Saves submissions in Supabase with metadata  
✅ **Relay.app Automation** — Integrates with 4 separate Relay automations per unit  
✅ **Session Management** — Maintains conversation state across requests  
✅ **Graceful Fallback** — Rule-based keyword routing if LLM is unavailable  
✅ **Responsive UI** — Modern chat interface with refresh & message management  
✅ **Security-First** — API keys hidden in `.env`, secrets not committed to git  

---

## 📁 Project Structure

```
VS_UniversityAgent/
├── backend/                           # FastAPI server
│   ├── app/
│   │   ├── main.py                   # FastAPI app & chat endpoint
│   │   ├── workflow.py               # Conversation manager & LLM logic
│   │   └── supabase_client.py        # Supabase database client
│   ├── db/
│   │   └── init.sql                  # Database schema (create table + columns)
│   ├── myvenv/                       # Python virtual environment
│   ├── requirements.txt              # Python dependencies
│   ├── .env                          # Environment variables (DO NOT COMMIT)
│   └── README.md
│
├── frontend/                          # React + Vite app
│   ├── src/
│   │   ├── App.jsx                   # Main React component (chat UI)
│   │   ├── main.jsx                  # Vite entry point
│   │   └── styles.css                # Chat styling (responsive)
│   ├── index.html                    # HTML entry
│   ├── package.json                  # Node dependencies
│   └── vite.config.js                # Vite configuration
│
├── .gitignore                         # Ignore .env, node_modules, __pycache__
├── README.md                          # This file

```

---

## 📦 Prerequisites

- **Python 3.12+** with pip
- **Node.js 18+** with npm
- **PostgreSQL/Supabase account** (free tier available)
- **Google Gemini API key** (free with Google Cloud account)
- **Relay.app account** with 4 configured automations
- **Git** for version control

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/VS_UniversityAgent.git
cd VS_UniversityAgent
```

### 2. Backend Setup

#### a. Create Virtual Environment

```bash
cd backend
python -m venv myvenv

# On Windows:
myvenv\Scripts\activate

# On macOS/Linux:
source myvenv/bin/activate
```

#### b. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `python-dotenv` - Environment variables
- `supabase` - Database client
- `httpx` - Async HTTP requests
- `google-generativeai` - Gemini LLM

#### c. Create & Configure `.env`

Create `backend/.env`:

```env
# Supabase Configuration
SUPABASE_URL="your-supabase-url"
SUPABASE_KEY="your-supabase-key"

# Unit-Specific Webhook URLs (Relay.app)
WEBHOOK_URL_ADMISSION_SCHOLARSHIP="https://hook.relay.app/api/v1/playbook/.../trigger/..."
WEBHOOK_URL_ACADEMIC_SUPPORT="https://hook.relay.app/api/v1/playbook/.../trigger/..."
WEBHOOK_URL_STUDENT_WELFARE="https://hook.relay.app/api/v1/playbook/.../trigger/..."
WEBHOOK_URL_CAREER_SKILL_DEVELOPMENT="https://hook.relay.app/api/v1/playbook/.../trigger/..."

# Google Gemini (Optional but recommended)
GOOGLE_API_KEY="your-gemini-api-key"
GEN_MODEL="models/gemini-2.5-flash"
GEN_CONFIDENCE_THRESHOLD="0.6"
```

### 3. Frontend Setup

```bash
cd frontend
npm install
```

This installs:
- `react` - UI library
- `vite` - Build tool & dev server

---

## 🗄️ Database Setup

### 1. Create Supabase Project

1. Go to [supabase.com](https://supabase.com) and create a free account
2. Create a new project (PostgreSQL)
3. Copy `SUPABASE_URL` and `SUPABASE_KEY` from Settings → API

### 2. Run Database Migration

1. Open your Supabase SQL editor
2. Copy & paste the contents of `backend/db/init.sql`:

```sql
-- Create student_queries table
create table if not exists public.student_queries (
  id bigserial primary key,
  student_name text not null,
  academic_year text not null,
  student_query text not null,
  routed_unit text not null,
  tone text,
  confidence double precision,
  timestamp timestamptz not null default now()
);

-- Create index for faster queries
create index if not exists idx_student_queries_timestamp on public.student_queries (timestamp);

-- Add tone and confidence columns (if not present)
ALTER TABLE public.student_queries
  ADD COLUMN IF NOT EXISTS tone text;

ALTER TABLE public.student_queries
  ADD COLUMN IF NOT EXISTS confidence double precision;
```

3. Execute the SQL

---

## ▶️ Running the Application

### Terminal 1: Backend Server

```bash
cd backend
myvenv\Scripts\activate  # Windows
# source myvenv/bin/activate  # macOS/Linux

uvicorn app.main:app --host 127.0.0.1 --port 8000
```

✅ Backend running at: **http://localhost:8000**

### Terminal 2: Frontend Dev Server

```bash
cd frontend
npm run dev
```

✅ Frontend running at: **http://localhost:5173** (or **5174** if 5173 is in use)

### Access the Chat UI

Open your browser and navigate to:
```
http://localhost:5173
```

---

## 🏗️ Architecture

### Conversation Flow

```
User Input
    ↓
[Frontend Chat UI]
    ↓
POST /chat (with session_id & message)
    ↓
[FastAPI Backend]
    ├─ Extract Name (if not present)
    ├─ Extract Academic Year (if not present)
    ├─ Extract Query (if not present)
    └─ Route Query:
       ├─ Try: Google Gemini LLM Classification
       │  └─ Returns: (unit, tone, confidence)
       └─ Fallback: Keyword-based Rule Mapping
    ↓
[Persist & Send]
    ├─ Save to Supabase
    └─ POST to Unit-Specific Relay.app Webhook
    ↓
[Relay.app Automation] (per unit)
    ↓
Response → Frontend
```

### Key Components

| Component | Purpose | Language |
|-----------|---------|----------|
| `App.jsx` | Chat UI, message rendering, send/refresh | React/JSX |
| `main.py` | FastAPI endpoints, CORS, session management | Python |
| `workflow.py` | Conversation state, LLM classification, routing | Python |
| `supabase_client.py` | Database insert with error handling & retry | Python |
| `init.sql` | Table schema with tone & confidence columns | SQL |

---

## 📡 API Documentation

### Endpoint: `/chat` (POST)

**Request:**
```json
{
  "session_id": "uuid-string-or-null",
  "message": "user message here"
}
```

**Response:**
```json
{
  "response": "bot message to user",
  "session_id": "uuid-string"
}
```

**Example:**

```bash
# 1. Start conversation
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"__start__"}'

# Response: session_id returned

# 2. Provide name
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id":"<sid>","message":"My name is Jane Doe"}'

# 3. Provide year
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id":"<sid>","message":"I am in 2nd year"}'

# 4. Submit query
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id":"<sid>","message":"I feel stressed before exams"}'
```

### Endpoint: `/health` (GET)

Health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

---

## 🧪 Testing

### Test Routing to Each Unit

Send queries that trigger different units:

1. **Admission & Scholarship** (Unit 1):
   - _"How can I apply for BTech admission?"_
   - _"Am I eligible for SC/ST scholarship?"_

2. **Academic Support** (Unit 2):
   - _"What is the syllabus for DBMS?"_
   - _"When is the next exam?"_

3. **Student Welfare** (Unit 3):
   - _"I feel stressed before exams"_
   - _"How can I manage study pressure?"_

4. **Career & Skill Development** (Unit 4):
   - _"Which internship suits me?"_
   - _"How can I improve my programming skills?"_

### Check Logs

Watch the backend terminal for:
- `[workflow] LLM routed session ... to unit: ...`
- `[workflow] Webhook sent to ... unit: ...`
- `[supabase] Inserted record into student_queries: ...`

### Verify in Supabase

1. Open Supabase dashboard
2. Go to **Tables** → **student_queries**
3. Confirm rows are being inserted with correct unit, tone, and confidence

---

## 🔗 Webhook Integration

### Relay.app Setup

Your system sends unit-specific webhooks to Relay.app:

| Unit | Webhook Key | Environment Variable |
|------|-------------|----------------------|
| Admission & Financial Aid | `WEBHOOK_URL_ADMISSION_SCHOLARSHIP` | Line 6 of `.env` |
| Academic Support | `WEBHOOK_URL_ACADEMIC_SUPPORT` | Line 7 of `.env` |
| Student Welfare | `WEBHOOK_URL_STUDENT_WELFARE` | Line 8 of `.env` |
| Career & Skill Development | `WEBHOOK_URL_CAREER_SKILL_DEVELOPMENT` | Line 9 of `.env` |

### Webhook Payload Format

```json
{
  "Student Name": "Jane Doe",
  "Academic Year": "2nd_year",
  "Student Query": "I feel stressed before exams",
  "unit": "student_welfare",
  "tone": "normal",
  "confidence": 0.92
}
```

### Setting Up in Relay.app

1. Create 4 separate Relay automations (one per unit)
2. Each automation receives HTTP POST requests on its unique webhook URL
3. Configure automations to handle:
   - Sending notifications to unit staff
   - Creating support tickets
   - Triggering follow-up emails
   - Logging to your internal system

---

## 🔐 Security

### Environment Variables

- **Never commit `.env` file** — it contains API keys
- `.gitignore` already configured to exclude it
- Use a `.env.example` template for developers

### If API Key Was Committed Accidentally

```bash
# 1. Remove from git history
git rm --cached backend/.env
git commit -m "Remove .env from repository"
git push

# 2. Rotate all exposed keys in their provider dashboards
# - Google Cloud Console (Gemini API key)
# - Supabase Settings (Database key)
# - Relay.app (Webhook URLs if exposed)

# 3. Rewrite git history (optional but recommended)
# See: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository
```

### Best Practices

✅ Store secrets in environment variables only  
✅ Use `.env` locally, secrets management in production (AWS Secrets Manager, Google Secret Manager)  
✅ Rotate API keys periodically  
✅ Enable Supabase Row Level Security (RLS) for production  
✅ Use HTTPS for all webhook communications  
✅ Validate webhook signatures (future enhancement)  

---

## 🐛 Troubleshooting

### Issue: Backend won't start

**Error:** `ModuleNotFoundError: No module named 'dotenv'`

**Solution:**
```bash
cd backend
myvenv\Scripts\activate
pip install -r requirements.txt
```

---

### Issue: Frontend can't connect to backend

**Error:** `Failed to fetch http://localhost:8000/chat`

**Solution:**
1. Ensure backend is running on port 8000
2. Check CORS middleware in `main.py` allows `http://localhost:5173`
3. Clear browser cache (Ctrl+Shift+Delete)

---

### Issue: Webhooks not triggering in Relay.app

**Solution:**
1. Verify all 4 webhook URLs are correct in `.env`
2. Test webhook manually: `curl -X POST <webhook-url> -d '{...}'`
3. Check Relay.app logs for POST receipt
4. Ensure database queries are saving (check Supabase table)

---

### Issue: LLM classification is slow or failing

**Error:** `[workflow] Error during LLM classify: ...`

**Solution:**
1. Verify `GOOGLE_API_KEY` is set in `.env`
2. Check Google Cloud API quota
3. System will fallback to keyword-based routing if LLM unavailable
4. Set `GEN_CONFIDENCE_THRESHOLD` to filter low-confidence results

---

## 📚 Database Schema Reference

```sql
student_queries (table):
  ├── id (bigserial, PK)
  ├── student_name (text)
  ├── academic_year (text) -- '12th_pass' | '1st_year' | '2nd_year' | '3rd_year' | '4th_year'
  ├── student_query (text)
  ├── routed_unit (text) -- 'admission_scholarship' | 'academic_support' | 'student_welfare' | 'career_skill_development'
  ├── tone (text) -- 'normal' | 'urgent'
  ├── confidence (double precision) -- 0.0 - 1.0
  └── timestamp (timestamptz)
```

---

## 🚀 Future Enhancements

- [ ] Session persistence in database (instead of in-memory)
- [ ] Webhook signature verification (HMAC)
- [ ] Rate limiting & DDoS protection
- [ ] Multi-language support
- [ ] Admin dashboard for analytics
- [ ] Chat history export (PDF/CSV)
- [ ] Sentiment analysis for improved tone detection
- [ ] Integration with university LDAP/SSO

---

## 📄 License

This project is licensed under the **MIT License** — feel free to use it for educational and commercial purposes.

---

## 👥 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit changes (`git commit -m "Add your feature"`)
4. Push to branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📞 Support

For issues, questions, or feature requests:
- Open an **Issue** on GitHub
- Email: your-email@example.com

---

**Built with ❤️ for university students.**

