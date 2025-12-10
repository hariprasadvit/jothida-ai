# 🎯 Claude Prompts for Vibe Coding - ஜோதிட AI

Use these prompts with Claude (Opus) in VS Code to continue building the app.
Copy-paste the relevant prompt section and let Claude do the magic!

---

## 🚀 STARTUP PROMPTS

### Initial Context (Use this first in every session)
```
I'm building a Tamil astrology app called "ஜோதிட AI" with:
- Backend: FastAPI + Python + PySwisseph (Swiss Ephemeris)
- Frontend: React + Vite + Tailwind + Recharts
- AI: RAG with ChromaDB + Tamil-LLaMA/Gemma

The app has a "stock market" style UI where:
- Daily fortune is shown like a stock ticker (fluctuating score)
- Planets are displayed as a portfolio with gains/losses
- Time periods (Rahu Kalam, Nalla Neram) shown as candlestick charts
- Marriage matching shows compatibility like a financial analysis

Current project structure is in the workspace. Help me build features.
```

---

## 🔧 BACKEND PROMPTS

### 1. Complete the Panchangam Calculator
```
Look at backend/app/services/panchangam_calculator.py

Complete the implementation:
1. Add accurate Tamil month calculation from Sun longitude
2. Implement proper Gowri Panchangam for Nalla Neram
3. Add festival detection (Pongal, Diwali, Tamil New Year)
4. Calculate Abhijit Muhurtham timing
5. Add unit tests

Use PySwisseph for calculations. Follow existing code style.
```

### 2. Build Jathagam Generator
```
Create backend/app/services/jathagam_generator.py

Build a complete birth chart generator:
1. Calculate Lagna (Ascendant) from birth time and location
2. Generate Rasi chart (12 houses with planet placements)
3. Generate Navamsa chart
4. Calculate Vimshottari Dasha periods
5. Detect Yogas (Gajakesari, Raja Yoga, etc.)
6. Calculate planet strengths (simplified Shadbala)

Return data in a format ready for visual charts.
Input: birth date, time, place (lat/lon)
Output: JSON with all chart data
```

### 3. Build Matching Calculator
```
Create backend/app/services/matching_calculator.py

Implement Tamil marriage matching (10 Poruthams):
1. Dinam (Tara) Porutham
2. Ganam Porutham  
3. Mahendra Porutham
4. Stree Deergha Porutham
5. Yoni Porutham
6. Rasi Porutham
7. Rasi Adhipathi Porutham
8. Vasiya Porutham
9. Rajju Porutham
10. Vedha Porutham

Also check:
- Chevvai Dosham (Manglik)
- Nadi Dosham

Each porutham should return:
- Score (0-100)
- Status (excellent/good/warning/critical)
- Tamil explanation
- AI insight

Use the nakshatra/rasi matching tables from traditional texts.
```

### 4. Build Muhurtham Finder
```
Create backend/app/services/muhurtham_finder.py

Find auspicious times for events:
1. Filter by Tithi (avoid Rikta tithis: 4, 9, 14)
2. Filter by Nakshatra (use Shubha nakshatras)
3. Avoid Rahu Kalam, Yamagandam
4. Consider user's birth nakshatra
5. Check planetary positions

For each muhurtham slot return:
- Date and time range
- Quality score (0-100)
- Contributing factors
- Any conflicts/warnings

Support event types: marriage, griha_pravesam, vehicle, business, travel, general
```

### 5. Enhance AI Chat Service
```
Look at backend/app/services/ai_chat.py

Enhance with:
1. Connect to ChromaDB for knowledge retrieval
2. Use sentence-transformers for Tamil embeddings
3. Integrate with Ollama (Tamil-LLaMA) or API
4. Add conversation memory
5. Generate rich responses with data for UI cards
6. Support both Tamil and English queries

The response should include:
- message: Main response text in Tamil
- data: Structured data for UI (charts, time slots, scores)
- insight: AI observation in a highlighted box
- action: Optional action button

Handle intents: nalla_neram, rahu_kalam, rasipalan, career, love, health, muhurtham
```

---

## 🎨 FRONTEND PROMPTS

### 1. Build API Integration Layer
```
Create frontend/src/utils/api.js

Build API client with:
1. Axios instance with base URL
2. Functions for all backend endpoints:
   - getPanchangam(date, lat, lon)
   - getTimeEnergy(date)
   - getWeekForecast()
   - generateJathagam(birthDetails)
   - checkMatching(bride, groom)
   - findMuhurtham(eventType, dateRange)
   - sendChatMessage(message, context)
3. Error handling
4. Loading states
5. Caching with React Query

Use TypeScript-style JSDoc for type hints.
```

### 2. Build Reusable Chart Components
```
Create frontend/src/components/charts/

Build these reusable components using Recharts:
1. ScoreGauge - Radial gauge for overall scores
2. EnergyChart - Area chart for hourly energy levels  
3. WeekSparkline - Mini line chart for 7-day trend
4. PlanetBar - Horizontal bar with planet strength
5. CompatibilityRadar - Radar chart for matching
6. TimelineChart - Horizontal timeline for Dasha/events

Each should:
- Accept data via props
- Use the app's color scheme (amber/purple/slate)
- Animate on load
- Be responsive
```

### 3. Build Rasi Chart Component
```
Create frontend/src/components/RasiChart.jsx

Build a traditional South Indian style Rasi chart:
1. Square grid with 12 houses
2. Show planet symbols in correct houses
3. Highlight Lagna
4. Support both Rasi and Navamsa
5. Click on house to show details
6. Animate planet placements

Use SVG or Canvas for the chart.
Accept data: { houses: [{planets: [...], isLagna: bool}] }
```

### 4. Build Voice Input Component
```
Create frontend/src/components/VoiceInput.jsx

Build voice input for Tamil:
1. Use Web Speech API (SpeechRecognition)
2. Set language to 'ta-IN' (Tamil)
3. Show listening animation (sound waves)
4. Display interim results
5. Handle errors gracefully
6. Fallback for unsupported browsers

Props: onResult(text), onError(error)
```

### 5. Build Calendar Heat Map
```
Create frontend/src/components/CalendarHeatMap.jsx

Build a month calendar with color-coded days:
1. Show Tamil month name
2. Each day cell colored by score (green/yellow/red)
3. Show festivals and special days
4. Tap day to see details
5. Swipe to change months
6. Show current day highlight

Accept data: [{date, score, festivals, warnings}]
```

### 6. Connect Dashboard to Backend
```
Look at frontend/src/pages/Dashboard.jsx

Currently using mock data. Connect to real backend:
1. Use React Query to fetch panchangam data
2. Fetch time energy for the chart
3. Fetch week forecast
4. Add pull-to-refresh
5. Show loading skeletons
6. Handle errors with retry
7. Cache data appropriately

Keep the existing visual design, just replace mock data.
```

---

## 🤖 AI TRAINING PROMPTS

### 1. Generate Training Data
```
I need to create a training dataset for Tamil astrology chatbot.

Generate 100 Q&A pairs in Tamil covering:
- Panchangam queries (tithi, nakshatra, timing)
- Daily/weekly predictions
- Career advice
- Love/relationship guidance  
- Health predictions
- Muhurtham queries
- Dosham explanations
- Remedy suggestions

Format as JSON:
[
  {
    "instruction": "Question in Tamil",
    "input": "Optional context",
    "output": "Answer in Tamil"
  }
]

Make answers detailed but concise. Include astrological reasoning.
Vary the question styles (formal, casual, specific, general).
```

### 2. Build RAG Pipeline
```
Create ai-training/scripts/rag_pipeline.py

Build a complete RAG pipeline:
1. Load Tamil astrology texts from data/raw/
2. Chunk texts (500 tokens, 50 overlap)
3. Generate embeddings (paraphrase-multilingual-MiniLM-L12-v2)
4. Store in ChromaDB
5. Create retrieval function
6. Build prompt template for Tamil-LLaMA
7. Test with sample queries

Include:
- Hybrid search (semantic + keyword)
- Reranking
- Source citation
```

### 3. Fine-tune Tamil Model
```
Create ai-training/scripts/finetune.py

Script to fine-tune Tamil-LLaMA on astrology data:
1. Load base model (abhinand/tamil-llama-7b-instruct-v0.2)
2. Load training data from data/processed/
3. Use LoRA for efficient fine-tuning
4. Training config:
   - Learning rate: 2e-5
   - Epochs: 3
   - Batch size: 4
   - Max length: 512
5. Save checkpoints
6. Evaluate on held-out set

Use Hugging Face transformers + PEFT.
```

---

## 🐛 DEBUGGING PROMPTS

### Fix Calculation Issues
```
I'm getting incorrect [tithi/nakshatra/rahu kalam] calculations.

Current code: [paste code]
Expected: [expected result]
Actual: [actual result]

Help me debug. Consider:
1. Ayanamsha correction (Lahiri)
2. Timezone handling
3. Julian day conversion
4. Coordinate system
```

### Fix UI Issues
```
The [component name] is not rendering correctly.

Current code: [paste code]
Expected behavior: [describe]
Actual behavior: [describe]

Browser: [Chrome/Safari/Firefox]
Screen size: [mobile/desktop]

Help me fix the issue. Check for:
1. Tailwind class conflicts
2. Responsive breakpoints
3. State management
4. Animation issues
```

---

## 📱 MOBILE OPTIMIZATION PROMPTS

### Convert to React Native
```
I want to convert this React web app to React Native.

Current web component: [paste component]

Convert to React Native with:
1. Replace HTML elements with RN components
2. Use StyleSheet instead of Tailwind
3. Replace Recharts with react-native-svg-charts
4. Handle safe areas
5. Add haptic feedback
6. Optimize for performance
```

### Add PWA Features
```
Make the web app installable as PWA:

1. Create manifest.json with:
   - Tamil app name
   - Theme colors (amber/purple)
   - Icons for all sizes
   
2. Create service worker for:
   - Offline panchangam (cache API responses)
   - Background sync for notifications
   - Push notifications for Rahu Kalam alerts

3. Add install prompt UI
```

---

## 🎯 FEATURE PROMPTS

### Add Push Notifications
```
Implement push notifications for:
1. Morning panchangam briefing (6 AM)
2. Rahu Kalam start warning (15 min before)
3. Festival reminders
4. Personalized predictions

Backend: Use Firebase Cloud Messaging
Frontend: Use Web Push API

Create:
- backend/app/services/notifications.py
- frontend/src/utils/notifications.js
```

### Add Offline Support
```
Make the app work offline:

1. Cache today's panchangam data
2. Store user profile in IndexedDB
3. Queue chat messages for sync
4. Show offline indicator
5. Sync when back online

Use:
- React Query's offline support
- Service Worker for API caching
- IndexedDB for user data
```

---

## 🔄 ITERATION PROMPTS

### Quick Fix
```
[Paste error message or describe issue]

Fix this quickly. Just give me the corrected code.
```

### Improve This
```
[Paste code]

Make this better:
- More performant
- Cleaner code
- Better error handling
- Add comments in Tamil where helpful
```

### Add Feature
```
Current code: [paste]

Add: [describe feature]

Keep existing functionality. Just add the new feature.
```

---

## 💡 TIPS FOR VIBE CODING

1. **Start sessions with context** - Always paste the initial context prompt first

2. **Be specific** - Include file names, line numbers, and exact error messages

3. **Iterate fast** - Ask for small changes, test, repeat

4. **Use Tamil comments** - Ask Claude to add Tamil comments for astrology logic

5. **Test incrementally** - Build one feature at a time

6. **Save working states** - Commit to git frequently

7. **Ask for explanations** - If you don't understand the astrology logic, ask!

---

## 🏃 QUICK START COMMANDS

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend  
cd frontend
npm install
npm run dev

# AI Training
cd ai-training
pip install langchain chromadb sentence-transformers
python scripts/build_kb.py
```

---

Happy vibe coding! 🎉
