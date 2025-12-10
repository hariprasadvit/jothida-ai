# AI Training Setup for ஜோதிட AI

## Overview

This directory contains scripts and data for training/fine-tuning the Tamil astrology AI.

## Approach

### Option 1: RAG (Retrieval Augmented Generation) - Recommended for MVP
No training needed! Just:
1. Build knowledge base from Tamil astrology texts
2. Use embeddings (sentence-transformers)
3. Store in ChromaDB
4. Query with Tamil-LLaMA or Gemma

### Option 2: Fine-tuning (For Production)
Fine-tune Tamil-LLaMA on astrology-specific data.

## Directory Structure

```
ai-training/
├── data/
│   ├── raw/                 # Raw text files
│   ├── processed/           # Cleaned JSON/JSONL
│   └── embeddings/          # Vector embeddings
├── scripts/
│   ├── prepare_data.py      # Data preprocessing
│   ├── build_kb.py          # Build knowledge base
│   ├── train.py             # Fine-tuning script
│   └── evaluate.py          # Evaluation
├── models/
│   └── checkpoints/         # Saved model checkpoints
└── notebooks/
    └── exploration.ipynb    # Data exploration
```

## Data Sources

### Tamil Astrology Texts (Public Domain)
1. Archive.org - Search "தமிழ் ஜோதிடம்"
2. Tamil Virtual Academy
3. Project Madurai

### Structured Data
1. VedAstro - 15,000 celebrity birth charts
2. Generate synthetic Q&A pairs

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Prepare data
python scripts/prepare_data.py

# 3. Build knowledge base
python scripts/build_kb.py

# 4. Test RAG
python scripts/test_rag.py "இன்று நல்ல நேரம் எப்போது?"
```

## Knowledge Base Topics

- Panchangam calculations
- Nakshatra characteristics
- Rasi predictions
- Porutham matching rules
- Dosham analysis
- Muhurtham selection
- Dasha interpretation
- Gochara effects
- Pariharam (remedies)
