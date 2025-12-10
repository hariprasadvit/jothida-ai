# ஜோதிட AI - Tamil Astrology with AI

A modern Tamil astrology app with stock-market style visualizations and AI-powered predictions.

![Dashboard Preview](docs/dashboard-preview.png)

## 🎯 Features

- **Visual Dashboard** - Fortune shown like stock ticker with fluctuating scores
- **Planet Portfolio** - Your 9 planets displayed as investments with gains/losses
- **Time Energy Chart** - Candlestick-style hourly energy visualization
- **Marriage Matching** - Visual compatibility analysis with 10 Poruthams
- **AI Chatbot** - Ask questions in Tamil, get intelligent answers
- **Muhurtham Finder** - Find auspicious times with calendar heat map

## 🏗️ Tech Stack

### Backend
- FastAPI (Python)
- PySwisseph (Swiss Ephemeris)
- ChromaDB (Vector storage)
- LangChain (RAG)

### Frontend
- React 18 + Vite
- Tailwind CSS
- Recharts
- Framer Motion

### AI
- Tamil-LLaMA / Gemma
- Sentence Transformers
- RAG Pipeline

## 🚀 Quick Start

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000

## 📁 Project Structure

```
jothida-ai/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI app
│   │   ├── routers/          # API endpoints
│   │   └── services/         # Business logic
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/            # Page components
│   │   ├── components/       # Reusable components
│   │   └── utils/            # API, helpers
│   └── package.json
├── ai-training/
│   ├── data/                 # Training data
│   ├── scripts/              # Training scripts
│   └── models/               # Saved models
├── docs/                     # Documentation
├── CLAUDE_PROMPTS.md         # 🎯 Prompts for vibe coding!
└── README.md
```

## 🎨 Screenshots

| Dashboard | Matching | AI Chat |
|-----------|----------|---------|
| Stock-style scores | Radar compatibility | Voice Tamil input |

## 🤖 Vibe Coding with Claude

This project is designed for "vibe coding" with Claude in VS Code.

**See [CLAUDE_PROMPTS.md](CLAUDE_PROMPTS.md) for ready-to-use prompts!**

### Quick Start
1. Open project in VS Code
2. Install Claude extension
3. Copy a prompt from CLAUDE_PROMPTS.md
4. Let Claude build features!

## 📊 API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/panchangam/today` | Today's panchangam |
| `GET /api/panchangam/time-energy` | Hourly energy chart data |
| `POST /api/jathagam/generate` | Generate birth chart |
| `POST /api/matching/check` | Check marriage compatibility |
| `GET /api/muhurtham/find` | Find auspicious times |
| `POST /api/chat/message` | AI chat |

## 🌐 Localization

- Primary: Tamil (தமிழ்)
- Secondary: English

All UI text and AI responses support Tamil.

## 📱 Mobile Ready

- Responsive design for all screens
- PWA support (installable)
- Offline panchangam support
- Touch-optimized UI

## 🙏 Credits

- Swiss Ephemeris for astronomical calculations
- Tamil-LLaMA by Abhinand Balachandran
- VedAstro for reference implementations

## 📄 License

MIT License - See LICENSE file

---

Built with ❤️ for the Tamil community
