# NOVA AI

LangChain + Google groq powered chat aur quiz app, FastAPI backend ke saath.

## Features

- **AI Chat** — groq se real-time conversation
- **AI Quiz** — Kisi bhi topic par auto-generated MCQ quiz
- **Web UI** — Dark orange themed chat interface

## Setup

### 1. Dependencies install karo

```bash
pip install -r req.txt
```

### 2. API key set karo

`.env.example` ko copy karke `.env` banao:

```bash
copy .env.example .env
```

`.env` mein apni groq API key likho ([Google AI Studio](https://aistudio.google.com/apikey)):

```
groq_API_KEY=your_key_here
```

### 3. Server start karo

```bash
uvicorn main:app --reload
```

### 4. Browser mein kholo

[http://127.0.0.1:8000](http://127.0.0.1:8000)

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Server status check |
| POST | `/CHAT` | Chat message bhejo `{ "message": "..." }` |
| POST | `/quiz/generate` | Quiz banao `{ "topic": "Python", "num_questions": 5 }` |

## Project Structure

```
├── main.py          # FastAPI app + chat endpoint
├── routes/quiz.py   # Quiz generation API
├── index.html       # Frontend UI
├── script.js        # Chat + Quiz logic
├── style.css        # Styling
├── req.txt          # Python dependencies
└── complex_demo.py  # Separate Complex number demo
```
