import streamlit as st
import pandas as pd
import sqlite3
import datetime
import random
from gtts import gTTS
import io

# -----------------------------------------------------------------------------
# 1. DATABASE SYSTEM (SQLite Persistency)
# -----------------------------------------------------------------------------
DB_FILE = "eduverse_advanced.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            subject TEXT,
            score INTEGER,
            total INTEGER,
            grade TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_quiz_score(subject, score, total, grade):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO quiz_results (timestamp, subject, score, total, grade) VALUES (?, ?, ?, ?, ?)",
              (datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), subject, score, total, grade))
    conn.commit()
    conn.close()

def get_quiz_scores():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM quiz_results ORDER BY id DESC", conn)
    conn.close()
    return df

init_db()

# -----------------------------------------------------------------------------
# 2. ADVANCED STYLING & ULTRA REALISTIC UI/UX (CSS)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="EduVerse AI - Enterprise Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 50%, #0F172A 100%);
        color: #F8FAFC;
    }

    /* Impressive Hero Banner Card */
    .hero-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 28px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        margin-bottom: 25px;
    }

    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38BDF8 0%, #818CF8 50%, #F472B6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    
    .hero-sub {
        font-size: 1.1rem;
        color: #94A3B8;
        font-weight: 600;
    }

    /* Custom Unique Feature Panels */
    .feature-card {
        background: rgba(30, 41, 59, 0.7);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 20px;
    }

    /* Custom Navigation Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0B0F19 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    .nav-header {
        font-size: 1.6rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38BDF8, #818CF8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .badge-status {
        background: rgba(56, 189, 248, 0.15);
        color: #38BDF8 !important;
        padding: 6px 14px;
        border-radius: 30px;
        font-weight: 700;
        font-size: 0.85rem;
        display: inline-block;
        border: 1px solid rgba(56, 189, 248, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. SIDEBAR NAVIGATION PANE
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("<div class='nav-header'>🎓 EduVerse AI</div>", unsafe_allow_html=True)
    st.caption("Advanced Autonomous Learning Suite")
    st.divider()
    
    st.markdown("<p style='font-weight: 700; font-size: 0.85rem; color: #64748B !important; text-transform: uppercase;'>Workspaces Navigation Pane</p>", unsafe_allow_html=True)
    
    navigation = st.radio(
        "Select Workspace",
        [
            "🧠 Multi-Persona AI Tutor",
            "⚡ Instant Doubt & Formula Solver",
            "🎙️ Audio Lecture Engine",
            "📝 Exam Simulator & Assessment",
            "🎴 Smart Flashcards Generator",
            "📊 Analytics Dashboard & Audit"
        ],
        label_visibility="collapsed"
    )
    
    st.divider()
    st.markdown("<span class='badge-status'>● Offline Engine Active</span>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# HERO HEADER WITH IMAGE INTEGRATION
# -----------------------------------------------------------------------------
c_head, c_img = st.columns([2, 1])

with c_head:
    st.markdown(f"""
    <div class='hero-card'>
        <div class='hero-title'>EduVerse AI Platform</div>
        <div class='hero-sub'>Active Workspace ✦ <b>{navigation}</b></div>
        <p style='color: #64748B; margin-top: 10px;'>Next-generation AI learning hub with real-time database logging and interactive UI components.</p>
    </div>
    """, unsafe_allow_html=True)

with c_img:
    st.image("https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1000&auto=format&fit=crop", 
             caption="EduVerse AI Visual Canvas", use_column_width=True)

# -----------------------------------------------------------------------------
# MODULE 1: MULTI-PERSONA AI TUTOR
# -----------------------------------------------------------------------------
if navigation == "🧠 Multi-Persona AI Tutor":
    st.markdown("""
    <div class='feature-card'>
        <h3 style='color:#38BDF8;'>🧠 Multi-Persona Socratic AI Tutor</h3>
        <p>Choose an AI learning persona tailored to your preferred learning style.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_p, col_c = st.columns([1, 2.5])
    
    with col_p:
        persona = st.selectbox("Select Learning Mode:", [
            "🧠 Socratic Guide",
            "👶 ELI5 (Explain Like I'm 5)",
            "👨‍🏫 University Professor"
        ])
        
    with col_c:
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = [
                {"role": "assistant", "content": "Welcome! Select a persona on the left and enter any topic to begin."}
            ]
            
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
                
        if prompt := st.chat_input("Ask a question..."):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)
                
            reply = f"Persona: **{persona}** | Responding to **'{prompt}'**: Here is the key insight..."
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            with st.chat_message("assistant"):
                st.write(reply)

# -----------------------------------------------------------------------------
# MODULE 2: INSTANT DOUBT & FORMULA SOLVER
# -----------------------------------------------------------------------------
elif navigation == "⚡ Instant Doubt & Formula Solver":
    st.markdown("""
    <div class='feature-card'>
        <h3 style='color:#818CF8;'>⚡ Multi-Disciplinary Doubt & Solution Engine</h3>
        <p>Step-by-step mathematical proofs and logic breakdowns.</p>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns([1, 1])
    with c1:
        subject = st.selectbox("Select Subject", ["Mathematics", "Physics", "Computer Science"])
        query = st.text_area("State your problem:", "Calculate integral of x^2 * sin(x)")
        solve_btn = st.button("🚀 Solve Problem", use_container_width=True)
        
    with c2:
        if solve_btn and query.strip():
            st.success("✅ Solution Rendered")
            st.latex(r"\int x^2 \sin(x) \, dx = -x^2 \cos(x) + 2x \sin(x) + 2\cos(x) + C")

# -----------------------------------------------------------------------------
# MODULE 3: AUDIO LECTURE ENGINE
# -----------------------------------------------------------------------------
elif navigation == "🎙️ Audio Lecture Engine":
    st.markdown("""
    <div class='feature-card'>
        <h3 style='color:#F472B6;'>🎙️ Autonomous Audio Lecture Generator</h3>
        <p>Convert lesson scripts into audio lectures using local Text-to-Speech.</p>
    </div>
    """, unsafe_allow_html=True)
    
    script = st.text_area("Lesson Script:", "Welcome to EduVerse. AI is transforming personal learning environments.")
    if st.button("▶️ Generate Audio Lecture", use_container_width=True):
        tts = gTTS(text=script, lang="en")
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        st.audio(fp, format="audio/mp3")

# -----------------------------------------------------------------------------
# MODULE 4: EXAM SIMULATOR
# -----------------------------------------------------------------------------
elif navigation == "📝 Exam Simulator & Assessment":
    st.markdown("""
    <div class='feature-card'>
        <h3 style='color:#34D399;'>📝 Interactive Exam Simulator</h3>
        <p>Timed exams with persistence logging in SQLite DB.</p>
    </div>
    """, unsafe_allow_html=True)
    
    topic = st.selectbox("Exam Subject", ["Data Structures", "Operating Systems", "Python"])
    if st.button("🚀 Submit Sample Score", use_container_width=True):
        score = random.randint(3, 5)
        log_quiz_score(topic, score, 5, "PASS ✅")
        st.success(f"Score Saved to SQLite Database: {score}/5")

# -----------------------------------------------------------------------------
# MODULE 5: SMART FLASHCARDS
# -----------------------------------------------------------------------------
elif navigation == "🎴 Smart Flashcards Generator":
    st.markdown("""
    <div class='feature-card'>
        <h3 style='color:#FBBF24;'>🎴 Automated Revision Deck</h3>
        <p>Interactive study flashcards for active recall.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("📌 Flashcard 1: What is Normalization?"):
        st.write("Process of organizing data in a database to reduce redundancy.")

# -----------------------------------------------------------------------------
# MODULE 6: ANALYTICS DASHBOARD
# -----------------------------------------------------------------------------
elif navigation == "📊 Analytics Dashboard & Audit":
    st.markdown("""
    <div class='feature-card'>
        <h3 style='color:#F59E0B;'>📊 Real-Time Analytics & Database Audit</h3>
        <p>Persistent logs from SQLite database.</p>
    </div>
    """, unsafe_allow_html=True)
    
    scores_df = get_quiz_scores()
    st.dataframe(scores_df, use_container_width=True)
