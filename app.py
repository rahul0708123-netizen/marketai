import streamlit as st
import os
import re
import json
from groq import Groq

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MarketAI Suite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Dark background */
.stApp {
    background: #0a0a0f;
    color: #e8e6f0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0f0f1a !important;
    border-right: 1px solid #1e1e35;
}
[data-testid="stSidebar"] * { color: #c8c5d8 !important; }

/* Header styles */
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 3.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a78bfa, #38bdf8, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    margin-bottom: 0.5rem;
}
.hero-sub {
    font-size: 1.1rem;
    color: #7c7a90;
    font-weight: 300;
    margin-bottom: 2rem;
}

/* Feature cards */
.feature-card {
    background: linear-gradient(135deg, #13131f, #1a1a2e);
    border: 1px solid #2a2a45;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
}
.feature-card:hover { border-color: #a78bfa; }
.feature-card h3 {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #e8e6f0;
    margin: 0.5rem 0 0.3rem;
}
.feature-card p { font-size: 0.85rem; color: #7c7a90; margin: 0; }
.feature-icon { font-size: 2rem; }

/* Result box */
.result-box {
    background: #13131f;
    border: 1px solid #2a2a45;
    border-left: 4px solid #a78bfa;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    white-space: pre-wrap;
    font-size: 0.95rem;
    line-height: 1.8;
    color: #d4d2e0;
}

/* Score gauge */
.score-display {
    text-align: center;
    padding: 2rem;
    background: linear-gradient(135deg, #13131f, #1a1a2e);
    border-radius: 16px;
    border: 1px solid #2a2a45;
}
.score-number {
    font-family: 'Syne', sans-serif;
    font-size: 5rem;
    font-weight: 800;
    line-height: 1;
}
.score-label {
    font-size: 1rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-top: 0.5rem;
}

/* Pill badges */
.badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin: 0.2rem;
}
.badge-hot { background: #ff4444; color: white; }
.badge-warm { background: #f97316; color: white; }
.badge-lukewarm { background: #eab308; color: black; }
.badge-cold { background: #3b82f6; color: white; }

/* Streamlit overrides */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #2563eb);
    color: white;
    border: none;
    border-radius: 10px;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.95rem;
    padding: 0.6rem 2rem;
    letter-spacing: 0.03em;
    transition: opacity 0.2s;
    width: 100%;
}
.stButton > button:hover { opacity: 0.85; }

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: #13131f !important;
    border: 1px solid #2a2a45 !important;
    border-radius: 10px !important;
    color: #e8e6f0 !important;
}
.stTextArea > div > div > textarea { min-height: 100px; }

label { color: #a8a6bc !important; font-size: 0.875rem !important; }

/* Section headers */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: #e8e6f0;
    margin-bottom: 0.25rem;
}
.section-desc { color: #7c7a90; font-size: 0.9rem; margin-bottom: 1.5rem; }

/* Divider */
.divider {
    border: none;
    border-top: 1px solid #1e1e35;
    margin: 1.5rem 0;
}

/* API key input special styling */
.api-box {
    background: #1a0a2e;
    border: 1px solid #4a2a7e;
    border-radius: 12px;
    padding: 1rem 1.5rem;
    margin-bottom: 1.5rem;
}

/* Card-style nav buttons */
[data-testid="stButton"]:has(button[data-testid="baseButton-secondary"]) button,
button[key="nav_campaign"], button[key="nav_pitch"], button[key="nav_lead"] {
    background: linear-gradient(135deg, #13131f, #1a1a2e) !important;
}

div[data-testid="stColumn"] .stButton > button {
    background: linear-gradient(135deg, #13131f, #1a1a2e) !important;
    border: 1px solid #2a2a45 !important;
    border-radius: 16px !important;
    text-align: left !important;
    min-height: 190px !important;
    white-space: pre-wrap !important;
    line-height: 1.5 !important;
    font-size: 0.9rem !important;
    font-weight: 400 !important;
    padding: 1.5rem !important;
    letter-spacing: normal !important;
}
div[data-testid="stColumn"] .stButton > button:hover {
    border-color: #a78bfa !important;
    transform: translateY(-3px) !important;
    opacity: 1 !important;
}
div[data-testid="stColumn"] .stButton > button:first-line {
    font-size: 2rem !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Helper: Groq Client ──────────────────────────────────────────────────────
def get_groq_client(api_key: str):
    return Groq(api_key=api_key)

def call_groq(api_key: str, system_prompt: str, user_prompt: str, temperature: float = 0.7) -> str:
    try:
        client = get_groq_client(api_key)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            max_tokens=2048
        )
        raw = response.choices[0].message.content
        # Clean markdown artifacts
        raw = re.sub(r'\*\*(.*?)\*\*', r'\1', raw)
        return raw.strip()
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ─── Feature Functions ────────────────────────────────────────────────────────

def generate_campaign(api_key, product, audience, platform):
    system = (
        "You are an expert marketing strategist specializing in digital campaigns. "
        "Generate structured, actionable marketing campaigns with specific, measurable recommendations."
    )
    user = f"""Generate a comprehensive marketing campaign strategy for:

PRODUCT: {product}
TARGET AUDIENCE: {audience}
PLATFORM(S): {platform}

Structure your response clearly with these sections:

1. CAMPAIGN OBJECTIVES (2-3 SMART goals)

2. CONTENT IDEAS (exactly 5 targeted ideas with brief description each)

3. AD COPY VARIATIONS (exactly 3 compelling variations optimized for {platform})

4. CALL-TO-ACTION SUGGESTIONS (3 specific CTAs tailored to {platform} user behavior)

5. BUDGET ALLOCATION RECOMMENDATION

Keep it practical and immediately actionable."""
    return call_groq(api_key, system, user)


def generate_pitch(api_key, product, persona, industry, company_size):
    system = (
        "You are an elite B2B sales coach who crafts pitches that close Fortune 500 deals. "
        "Create personalized, compelling sales pitches that address specific pain points."
    )
    user = f"""Create a personalized sales pitch for:

PRODUCT/SOLUTION: {product}
CUSTOMER PERSONA: {persona}
INDUSTRY: {industry}
COMPANY SIZE: {company_size}

Structure your response with:

1. 30-SECOND ELEVATOR PITCH
(Concise, attention-grabbing opening for first contact)

2. VALUE PROPOSITION
(Clear statement of the unique business value and ROI)

3. KEY DIFFERENTIATORS
(3-4 advantages that directly address this persona's pain points vs. alternatives)

4. OBJECTION HANDLING
(2 likely objections with confident responses)

5. CALL-TO-ACTION
(Specific next step to move this deal forward)

Make it feel personal, not generic."""
    return call_groq(api_key, system, user)


def score_lead(api_key, lead_name, budget, need, urgency, notes=""):
    system = (
        "You are a sales qualification expert using BANT methodology (Budget, Authority, Need, Timeline). "
        "Analyze leads objectively and provide data-driven scores. Always return a JSON block followed by detailed reasoning."
    )
    user = f"""Qualify and score this sales lead using BANT framework:

LEAD NAME: {lead_name}
BUDGET: {budget}
BUSINESS NEED: {need}
URGENCY/TIMELINE: {urgency}
ADDITIONAL NOTES: {notes if notes else "None"}

SCORING CRITERIA (0-100 scale):
- Budget (0-25 pts): Budget size, authority to approve, alignment with solution pricing
- Need (0-25 pts): Pain point severity, solution fit, business impact
- Urgency (0-25 pts): Timeline urgency, project priority, trigger events  
- Authority (0-25 pts): Decision-making power, stakeholder influence

First output a JSON block exactly like this:
```json
{{"score": <number>, "probability": <number>, "budget_score": <number>, "need_score": <number>, "urgency_score": <number>, "authority_score": <number>}}
```

Then provide:
SCORE REASONING:
(Explain each dimension score and overall assessment)

RECOMMENDED NEXT ACTIONS:
(3 specific actions the sales team should take immediately)

RISK FACTORS:
(2-3 things that could derail this deal)"""
    return call_groq(api_key, system, user, temperature=0.4)


def parse_lead_score(result: str):
    """Extract JSON scores from Groq response."""
    try:
        match = re.search(r'```json\s*(\{.*?\})\s*```', result, re.DOTALL)
        if match:
            data = json.loads(match.group(1))
            return data, result.replace(match.group(0), "").strip()
    except:
        pass
    # Fallback: try to find score manually
    score_match = re.search(r'"score":\s*(\d+)', result)
    prob_match = re.search(r'"probability":\s*(\d+)', result)
    if score_match:
        return {"score": int(score_match.group(1)), "probability": int(prob_match.group(1)) if prob_match else 50}, result
    return None, result


def get_score_label(score):
    if score >= 90: return "🔥 HOT LEAD", "badge-hot", "#ff4444"
    if score >= 75: return "♨️ WARM LEAD", "badge-warm", "#f97316"
    if score >= 60: return "🌤 LUKEWARM", "badge-lukewarm", "#eab308"
    return "❄️ COLD LEAD", "badge-cold", "#3b82f6"

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 1rem 0;">
        <div style="font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:800;
             background:linear-gradient(135deg,#a78bfa,#38bdf8);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
            ⚡ MarketAI Suite
        </div>
        <div style="font-size:0.75rem;color:#7c7a90;margin-top:0.25rem;">Powered by Groq × LLaMA 3.3 70B</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")

    current = st.session_state.get("nav_page", "🏠 Dashboard")

    nav_items = [
        ("🏠 Dashboard", "🏠 Dashboard"),
        ("📢 Campaign Generator", "📢 Campaign Generator"),
        ("🎯 Sales Pitch", "🎯 Sales Pitch"),
        ("📊 Lead Scoring", "📊 Lead Scoring"),
    ]

    st.markdown("""
    <style>
    [data-testid="stSidebar"] .stRadio { display: none !important; }
    [data-testid="stSidebar"] .nav-link > button {
        background: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        color: #a8a6bc !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.95rem !important;
        font-weight: 400 !important;
        padding: 0.4rem 0.5rem !important;
        width: 100% !important;
        text-align: left !important;
        letter-spacing: normal !important;
        cursor: pointer !important;
        box-shadow: none !important;
    }
    [data-testid="stSidebar"] .nav-link > button:hover {
        color: #e8e6f0 !important;
        background: transparent !important;
        opacity: 1 !important;
        transform: none !important;
    }
    [data-testid="stSidebar"] .nav-link-active > button {
        color: #a78bfa !important;
        font-weight: 600 !important;
        background: transparent !important;
    }
    </style>
    """, unsafe_allow_html=True)

    for label, key in nav_items:
        is_active = current == key
        css_class = "nav-link-active" if is_active else "nav-link"
        st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
        if st.button(label, key=f"sidebar_{key}", use_container_width=True):
            st.session_state["nav_page"] = key
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    api_key = "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"  # 🔑 Replace with your actual key
    st.markdown("""
    <div style="font-size:0.75rem;color:#5a5870;line-height:1.6;">
        <strong style="color:#7c7a90;">Model:</strong> LLaMA 3.3 70B<br>
        <strong style="color:#7c7a90;">Provider:</strong> Groq Cloud<br>
        <strong style="color:#7c7a90;">Version:</strong> 1.0.0
    </div>
    """, unsafe_allow_html=True)

# ─── Pages ────────────────────────────────────────────────────────────────────

# ── DASHBOARD ──────────────────────────────────────────────────────────────────
page = st.session_state.get("nav_page", "🏠 Dashboard")

if page == "🏠 Dashboard":
    st.markdown("""
    <div class="hero-title">MarketAI Suite</div>
    <div class="hero-sub">AI-powered sales & marketing intelligence — generate campaigns, craft pitches, and qualify leads in seconds.</div>
    """, unsafe_allow_html=True)
    
    # Clickable cards via styled full-width buttons
    st.markdown("""
    <style>
    div[data-testid="stButton"] button[kind="secondary"],
    div[data-testid="stColumn"] .stButton > button {
        all: unset;
    }
    #nav_campaign, #nav_pitch, #nav_lead { display: none; }

    .card-btn-wrap button {
        background: linear-gradient(135deg, #13131f, #1a1a2e) !important;
        border: 1px solid #2a2a45 !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        width: 100% !important;
        text-align: left !important;
        cursor: pointer !important;
        color: #e8e6f0 !important;
        font-family: inherit !important;
        font-size: 1rem !important;
        font-weight: 400 !important;
        transition: border-color 0.2s, transform 0.15s !important;
        min-height: 180px !important;
        display: block !important;
        background-image: none !important;
        letter-spacing: normal !important;
    }
    .card-btn-wrap button:hover {
        border-color: #a78bfa !important;
        transform: translateY(-2px) !important;
        opacity: 1 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(
            "📢\n\nCampaign Generator\n\nGenerate full marketing campaigns with content ideas, ad copy variations, and platform-specific CTAs.",
            key="nav_campaign", use_container_width=True
        ):
            st.session_state["nav_page"] = "📢 Campaign Generator"
            st.rerun()
    
    with col2:
        if st.button(
            "🎯\n\nSales Pitch Generator\n\nCraft personalized B2B pitches with elevator pitch, value props, differentiators, and objection handling.",
            key="nav_pitch", use_container_width=True
        ):
            st.session_state["nav_page"] = "🎯 Sales Pitch"
            st.rerun()
    
    with col3:
        if st.button(
            "📊\n\nLead Scoring\n\nQualify and score leads using BANT methodology with conversion probability and next-step recommendations.",
            key="nav_lead", use_container_width=True
        ):
            st.session_state["nav_page"] = "📊 Lead Scoring"
            st.rerun()
    

    
    # Example scenarios
    with st.expander("📖 View Example Use Cases from the Hackathon Brief"):
        st.markdown("""
        **Scenario 1 — Marketing Campaign**  
        SaaS product for small business owners → LinkedIn campaign with 5 content ideas + 3 ad copy variations

        **Scenario 2 — Sales Pitch**  
        B2B enterprise software → Fortune 500 IT Director pitch with 30-sec elevator + value prop + CTAs

        **Scenario 3 — Lead Scoring**  
        Lead with $50K budget, immediate needs, high urgency → BANT score 0-100 + conversion probability
        """)

# ── CAMPAIGN GENERATOR ─────────────────────────────────────────────────────────
elif page == "📢 Campaign Generator":
    st.markdown("""
    <div class="section-title">📢 Campaign Generator</div>
    <div class="section-desc">Generate data-driven marketing campaigns tailored to your product, audience, and platform.</div>
    """, unsafe_allow_html=True)
    
    with st.form("campaign_form"):
        product = st.text_area(
            "Product / Service Description",
            placeholder="e.g. AI-powered email marketing platform that helps e-commerce brands automate personalized campaigns...",
            height=100
        )
        
        col1, col2 = st.columns(2)
        with col1:
            audience = st.text_area(
                "Target Audience",
                placeholder="e.g. Marketing managers at mid-size e-commerce companies, budget-conscious, 25-45 age range...",
                height=100
            )
        with col2:
            platform = st.selectbox(
                "Primary Platform(s)",
                ["LinkedIn", "Instagram", "LinkedIn + Instagram", "Facebook", "Twitter/X", 
                 "Google Ads", "TikTok", "Email Marketing", "Multi-channel"]
            )
        
        submitted = st.form_submit_button("⚡ Generate Campaign Strategy")
    
    if submitted:
        if not api_key:
            st.error("Please enter your Groq API key in the sidebar.")
        elif not product or not audience:
            st.warning("Please fill in both Product and Target Audience fields.")
        else:
            with st.spinner("🧠 Generating your campaign strategy..."):
                result = generate_campaign(api_key, product, audience, platform)
            
            st.markdown("<div style='font-family:Syne,sans-serif;font-size:1.1rem;font-weight:700;color:#a78bfa;margin:1rem 0 0.5rem;'>✅ Campaign Strategy Generated</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='result-box'>{result}</div>", unsafe_allow_html=True)
            
            # Copy button area
            st.download_button(
                "📥 Download Campaign",
                data=result,
                file_name=f"campaign_{product[:20].replace(' ','_')}.txt",
                mime="text/plain"
            )
            
            # Save to session history
            if "campaign_history" not in st.session_state:
                st.session_state.campaign_history = []
            st.session_state.campaign_history.append({
                "product": product[:40], "platform": platform, "result": result
            })
    
    # History
    if st.session_state.get("campaign_history"):
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        st.markdown("<div style='font-family:Syne,sans-serif;color:#5a5870;font-size:0.85rem;font-weight:600;letter-spacing:0.05em;'>PREVIOUS CAMPAIGNS</div>", unsafe_allow_html=True)
        for i, h in enumerate(reversed(st.session_state.campaign_history[-3:])):
            with st.expander(f"📋 {h['product']}... — {h['platform']}"):
                st.text(h['result'])

# ── SALES PITCH ────────────────────────────────────────────────────────────────
elif page == "🎯 Sales Pitch":
    st.markdown("""
    <div class="section-title">🎯 Sales Pitch Generator</div>
    <div class="section-desc">Create personalized, compelling B2B pitches that close deals.</div>
    """, unsafe_allow_html=True)
    
    with st.form("pitch_form"):
        col1, col2 = st.columns(2)
        with col1:
            product = st.text_input(
                "Product / Solution Name",
                placeholder="e.g. Cloud-based inventory management system"
            )
            industry = st.selectbox(
                "Target Industry",
                ["Technology / SaaS", "Retail / E-commerce", "Healthcare", "Finance / Banking",
                 "Manufacturing", "Professional Services", "Education", "Government", "Other"]
            )
        with col2:
            persona = st.text_area(
                "Customer Persona",
                placeholder="e.g. Operations Director at a Fortune 500 retail company scaling across 500 stores, focused on efficiency...",
                height=100
            )
            company_size = st.selectbox(
                "Company Size",
                ["Startup (1-50)", "SMB (51-500)", "Mid-market (501-5,000)", 
                 "Enterprise (5,000-50,000)", "Fortune 500 (50,000+)"]
            )
        
        submitted = st.form_submit_button("⚡ Generate Sales Pitch")
    
    if submitted:
        if not api_key:
            st.error("Please enter your Groq API key in the sidebar.")
        elif not product or not persona:
            st.warning("Please fill in Product and Customer Persona.")
        else:
            with st.spinner("🧠 Crafting your personalized pitch..."):
                result = generate_pitch(api_key, product, persona, industry, company_size)
            
            st.markdown("<div style='font-family:Syne,sans-serif;font-size:1.1rem;font-weight:700;color:#38bdf8;margin:1rem 0 0.5rem;'>✅ Sales Pitch Generated</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='result-box'>{result}</div>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    "📥 Download Pitch",
                    data=result,
                    file_name=f"pitch_{product[:20].replace(' ','_')}.txt",
                    mime="text/plain"
                )

# ── LEAD SCORING ───────────────────────────────────────────────────────────────
elif page == "📊 Lead Scoring":
    st.markdown("""
    <div class="section-title">📊 Lead Scoring</div>
    <div class="section-desc">Qualify and prioritize leads using AI-powered BANT analysis with conversion probability.</div>
    """, unsafe_allow_html=True)
    
    with st.form("lead_form"):
        col1, col2 = st.columns(2)
        with col1:
            lead_name = st.text_input("Lead Name / Company", placeholder="e.g. Sarah Johnson — Acme Corp")
            budget = st.text_area(
                "Budget Information",
                placeholder="e.g. $150,000 annual software budget, can approve deals up to $50,000...",
                height=80
            )
            urgency = st.text_area(
                "Urgency / Timeline",
                placeholder="e.g. Board requested solution by end of Q3, high priority initiative...",
                height=80
            )
        with col2:
            need = st.text_area(
                "Business Need",
                placeholder="e.g. Improving customer retention by 20%, reducing churn from 15% to 8%...",
                height=80
            )
            notes = st.text_area(
                "Additional Notes (optional)",
                placeholder="e.g. Decision maker confirmed, evaluating 3 vendors, previous demo went well...",
                height=80
            )
        
        submitted = st.form_submit_button("⚡ Score This Lead")
    
    if submitted:
        if not api_key:
            st.error("Please enter your Groq API key in the sidebar.")
        elif not lead_name or not budget or not need or not urgency:
            st.warning("Please fill in Lead Name, Budget, Need, and Urgency.")
        else:
            with st.spinner("🧠 Analyzing and scoring lead..."):
                result = score_lead(api_key, lead_name, budget, need, urgency, notes)
            
            scores, cleaned_result = parse_lead_score(result)
            
            # Score display
            if scores:
                score = scores.get("score", 0)
                probability = scores.get("probability", 0)
                label, badge_class, color = get_score_label(score)
                
                st.markdown("<br>", unsafe_allow_html=True)
                col1, col2, col3 = st.columns([1, 1, 1])
                
                with col1:
                    st.markdown(f"""
                    <div class="score-display">
                        <div class="score-number" style="color:{color};">{score}</div>
                        <div style="color:#7c7a90;font-size:0.8rem;margin:0.25rem 0;">OUT OF 100</div>
                        <div class="score-label" style="color:{color};">{label}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="score-display">
                        <div class="score-number" style="color:#34d399;">{probability}%</div>
                        <div style="color:#7c7a90;font-size:0.8rem;margin:0.25rem 0;">CONVERSION RATE</div>
                        <div class="score-label" style="color:#34d399;">PROBABILITY</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    budget_s = scores.get("budget_score", 0)
                    need_s = scores.get("need_score", 0)
                    urgency_s = scores.get("urgency_score", 0)
                    authority_s = scores.get("authority_score", 0)
                    
                    st.markdown(f"""
                    <div class="score-display" style="text-align:left;">
                        <div style="font-family:Syne,sans-serif;font-weight:700;color:#a8a6bc;margin-bottom:0.75rem;font-size:0.8rem;letter-spacing:0.05em;">BANT BREAKDOWN</div>
                        <div style="display:flex;justify-content:space-between;margin-bottom:0.4rem;">
                            <span style="color:#7c7a90;font-size:0.85rem;">💰 Budget</span>
                            <span style="color:#a78bfa;font-weight:600;">{budget_s}/25</span>
                        </div>
                        <div style="display:flex;justify-content:space-between;margin-bottom:0.4rem;">
                            <span style="color:#7c7a90;font-size:0.85rem;">🎯 Need</span>
                            <span style="color:#38bdf8;font-weight:600;">{need_s}/25</span>
                        </div>
                        <div style="display:flex;justify-content:space-between;margin-bottom:0.4rem;">
                            <span style="color:#7c7a90;font-size:0.85rem;">⚡ Urgency</span>
                            <span style="color:#34d399;font-weight:600;">{urgency_s}/25</span>
                        </div>
                        <div style="display:flex;justify-content:space-between;">
                            <span style="color:#7c7a90;font-size:0.85rem;">👤 Authority</span>
                            <span style="color:#f472b6;font-weight:600;">{authority_s}/25</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
            
            # Full reasoning
            st.markdown("<div style='font-family:Syne,sans-serif;font-size:1.1rem;font-weight:700;color:#34d399;margin:1rem 0 0.5rem;'>✅ Full Lead Assessment</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='result-box'>{cleaned_result}</div>", unsafe_allow_html=True)
            
            st.download_button(
                "📥 Download Lead Report",
                data=result,
                file_name=f"lead_{lead_name[:20].replace(' ','_')}.txt",
                mime="text/plain"
            )
            
            # Save history
            if "lead_history" not in st.session_state:
                st.session_state.lead_history = []
            if scores:
                st.session_state.lead_history.append({
                    "name": lead_name, "score": scores.get("score", 0), "prob": scores.get("probability", 0)
                })
    
    # Lead history table
    if st.session_state.get("lead_history"):
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        st.markdown("<div style='font-family:Syne,sans-serif;color:#5a5870;font-size:0.85rem;font-weight:600;letter-spacing:0.05em;'>LEAD PIPELINE</div>", unsafe_allow_html=True)
        
        cols = st.columns([3, 1, 1, 2])
        cols[0].markdown("<span style='color:#7c7a90;font-size:0.8rem;'>LEAD</span>", unsafe_allow_html=True)
        cols[1].markdown("<span style='color:#7c7a90;font-size:0.8rem;'>SCORE</span>", unsafe_allow_html=True)
        cols[2].markdown("<span style='color:#7c7a90;font-size:0.8rem;'>PROB</span>", unsafe_allow_html=True)
        cols[3].markdown("<span style='color:#7c7a90;font-size:0.8rem;'>STATUS</span>", unsafe_allow_html=True)
        
        for h in reversed(st.session_state.lead_history):
            label, _, color = get_score_label(h["score"])
            c = st.columns([3, 1, 1, 2])
            c[0].markdown(f"<span style='color:#e8e6f0;font-size:0.9rem;'>{h['name']}</span>", unsafe_allow_html=True)
            c[1].markdown(f"<span style='color:{color};font-weight:700;'>{h['score']}</span>", unsafe_allow_html=True)
            c[2].markdown(f"<span style='color:#34d399;'>{h['prob']}%</span>", unsafe_allow_html=True)
            c[3].markdown(f"<span style='color:{color};font-size:0.8rem;font-weight:600;'>{label}</span>", unsafe_allow_html=True)
