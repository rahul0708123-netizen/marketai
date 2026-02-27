# ⚡ MarketAI Suite
**AI-Powered Sales & Marketing Platform** | Hackathon Build

Built with: **Streamlit** + **Groq API** (LLaMA 3.3 70B)

---

## 🚀 Quick Start (2 minutes)

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the app
```bash
streamlit run app.py
```

### 3. Open browser → `http://localhost:8501`

### 4. Enter your Groq API Key in the sidebar
Get a free key at: https://console.groq.com

---

## 🎯 Features

| Feature | Description |
|---|---|
| 📢 **Campaign Generator** | Full marketing strategy: campaign objectives, 5 content ideas, 3 ad copy variations, CTAs |
| 🎯 **Sales Pitch Generator** | Personalized B2B pitch: 30-sec elevator, value prop, differentiators, objection handling, CTA |
| 📊 **Lead Scoring** | BANT analysis: 0-100 score, BANT breakdown, conversion probability %, next actions |

---

## 🧪 Test Cases (from brief)

**Campaign Test:**
- Product: `AI-powered email marketing platform`
- Audience: `Marketing managers, mid-size e-commerce companies, budget-conscious`
- Platform: `LinkedIn + Instagram`

**Pitch Test:**
- Product: `Cloud-based inventory management system`
- Persona: `Operations Director, Fortune 500 retail company, scaling across 500 stores`
- Industry: `Retail / E-commerce` | Size: `Fortune 500`

**Lead Scoring Test:**
- Lead: `Sarah Johnson`
- Budget: `$150,000 annual software budget, can approve deals up to $50,000`
- Need: `Improving customer retention by 20%, reducing churn`
- Urgency: `Board of directors requested solution by end of Q3, high priority`

---

## 🏗️ Architecture

```
app.py          ← Single-file Streamlit app
requirements.txt ← groq + streamlit only

Flow:
User Input → Streamlit UI → Groq API (LLaMA 3.3 70B) → Parsed Response → Display
```

---

## 📁 Project Structure
```
marketai_suite/
├── app.py           # Main application (all features)
├── requirements.txt # Dependencies
└── README.md        # This file
```
