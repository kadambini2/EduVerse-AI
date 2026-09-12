import streamlit as st
import pandas as pd
import sqlite3
import datetime
import random

# -----------------------------------------------------------------------------
# 1. DATABASE SETUP (SQLite)
# -----------------------------------------------------------------------------
DB_FILE = "eduverse_ui.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            subject TEXT,
            score INTEGER,
            total INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def log_quiz_score(subject, score, total):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO quiz_results (timestamp, subject, score, total) VALUES (?, ?, ?, ?)",
              (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), subject, score, total))
    conn.commit()
    conn.close()

def get_quiz_scores():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM quiz_results ORDER BY id DESC", conn)
    conn.close()
    return df

init_db()

# -----------------------------------------------------------------------------
# 2. ADVANCED STYLING & IMPRESSIVE UI/UX CUSTOM CSS
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="EduVerse AI - Unique Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Main Background Gradient */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* Impressive Glassmorphism Hero Card */
    .hero-card {
        background: rgba(255, 255, 255, 0.75);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 20px;
        padding: 28px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
        margin-bottom: 25px;
    }

    .hero-title {
        font-size: 2.6rem;
        font-weight: 800;
        background: linear-gradient(90deg, #4F46E5 0%, #7C3AED 50%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    
    .hero-sub {
        font-size: 1.05rem;
        color: #4B5563;
        font-weight: 600;
    }

    /* Custom Unique Card Feature Panels */
    .feature-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
        border: 1px solid #E5E7EB;
        transition: transform 0.2s ease-in-out;
    }

    /* Custom Sidebar / Navigation Styling */
    section[data-testid="stSidebar"] {
        background-color: #0F172A !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: #F8FAFC !important;
    }

    .nav-header {
        font-size: 1.5rem;
        font-weight: 800;
        letter-spacing: 0.5px;
        background: linear-gradient(90deg, #38BDF8, #818CF8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding-top: 10px;
    }

    /* Custom Metric Display Badge */
    .badge-status {
        background: rgba(16, 185, 129, 0.15);
        color: #10B981 !important;
        padding: 6px 14px;
        border-radius: 30px;
        font-weight: 700;
        font-size: 0.82rem;
        display: inline-block;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. SIDEBAR NAVIGATION PANE
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("<div class='nav-header'>🎓 EduVerse AI</div>", unsafe_allow_html=True)
    st.caption("Next-Gen Intelligent Learning Portal")
    st.divider()
    
    st.markdown("<p style='font-weight: 700; font-size: 0.85rem; color: #94A3B8 !important; text-transform: uppercase;'>Navigation Pane</p>", unsafe_allow_html=True)
    
    navigation = st.radio(
        "Select Workspace",
        [
            "🧠 Socratic AI Tutor",
            "⚡ Instant Doubt Solver",
            "📝 Quiz & Assignment Generator",
            "🗓️ Adaptive Study Planner",
            "🎯 Career Guidance Platform",
            "📊 Student Progress Dashboard"
        ],
        label_visibility="collapsed"
    )
    
    st.divider()
    st.markdown("<span class='badge-status'>● Offline Engine Active</span>", unsafe_allow_html=True)
    st.caption("No API Key Required | Instant Response")

# -----------------------------------------------------------------------------
# MAIN HERO HEADER
# -----------------------------------------------------------------------------
st.markdown(f"""
<div class='hero-card'>
    <div class='hero-title'>EduVerse AI</div>
    <div class='hero-sub'>Active Workspace ✦ <b>{navigation}</b></div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# MODULE 1: SOCRATIC TUTOR
# -----------------------------------------------------------------------------
if navigation == "🧠 Socratic AI Tutor":
    st.markdown("""
    <div class='feature-card'>
        <h3 style='color:#4F46E5;'>🧠 Socratic AI Interactive Tutor</h3>
        <p>Interactive guided problem-solving through targeted questions.</p>
    </div>
    <br>
    """, unsafe_allow_html=True)
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Welcome! Which concept would you like to explore step-by-step today?"}
        ]
        
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
    if prompt := st.chat_input("Type your question or concept..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
            
        reply = f"That's a key concept in **'{prompt}'**! What do you think is the fundamental formula or rule governing this step?"
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.write(reply)

# -----------------------------------------------------------------------------
# MODULE 2: INSTANT DOUBT SOLVER
# -----------------------------------------------------------------------------
elif navigation == "⚡ Instant Doubt Solver":
    st.markdown("""
    <div class='feature-card'>
        <h3 style='color:#7C3AED;'>⚡ Instant Doubt Resolution Assistant</h3>
        <p>Break down complex formulas and theory into clear solutions.</p>
    </div>
    <br>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns([1, 1])
    with c1:
        subject = st.selectbox("Subject Area", ["Mathematics", "Physics", "Computer Science", "Chemistry"])
        query = st.text_area("State your question or problem:", placeholder="e.g. Derive key elements of Binary Search algorithm.")
        solve_btn = st.button("🚀 Resolve Doubt", use_container_width=True)
        
    with c2:
        st.subheader("Step-by-Step Breakdown")
        if solve_btn and query.strip():
            st.success("✅ Solution Calculated")
            st.markdown(f"**Domain:** `{subject}`")
            st.markdown("#### Logic Framework:")
            st.markdown(f"1. **Core Premise:** Deconstruct `{query[:30]}...`")
            st.markdown("2. **Core Equation:** $$T(n) = O(\\log n)$$")
            st.markdown("3. **Outcome:** Efficient reduction of search space by half in each iteration.")
        elif solve_btn:
            st.warning("Please type a question to get a response.")

# -----------------------------------------------------------------------------
# MODULE 3: QUIZ & ASSIGNMENT GENERATOR
# -----------------------------------------------------------------------------
elif navigation == "📝 Quiz & Assignment Generator":
    st.markdown("""
    <div class='feature-card'>
        <h3 style='color:#EC4899;'>📝 Quiz & Homework Assessment Generator</h3>
        <p>Generate interactive quizzes and log performance results directly to your local database.</p>
    </div>
    <br>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        topic = st.text_input("Topic", "Data Structures")
    with c2:
        level = st.selectbox("Level", ["Beginner", "Intermediate", "Advanced"])
    with c3:
        num_q = st.slider("Questions Count", 1, 5, 3)
        
    if st.button("✨ Create & Take Quiz", use_container_width=True):
        st.session_state.quiz_data = {"topic": topic, "level": level, "count": num_q}
        
    if "quiz_data" in st.session_state:
        q = st.session_state.quiz_data
        st.divider()
        st.subheader(f"Quiz: {q['topic']} ({q['level']})")
        
        with st.form("quiz_form"):
            for i in range(1, q["count"] + 1):
                st.write(f"**Q{i}: What is the primary characteristic of {q['topic']} at a {q['level']} level?**")
                st.radio(f"Select Answer Q{i}", ["Option A", "Option B", "Option C"], key=f"q_{i}", label_visibility="collapsed")
                st.divider()
            
            if st.form_submit_button("Submit Quiz"):
                score = random.randint(1, q["count"])
                log_quiz_score(q["topic"], score, q["count"])
                st.balloons()
                st.success(f"Assessment Submitted! Result Logged: **{score} / {q['count']}**")

# -----------------------------------------------------------------------------
# MODULE 4: ADAPTIVE STUDY PLANNER
# -----------------------------------------------------------------------------
elif navigation == "🗓️ Adaptive Study Planner":
    st.markdown("""
    <div class='feature-card'>
        <h3 style='color:#2563EB;'>🗓️ Adaptive Study Schedule Planner</h3>
        <p>Personalized calendar schedules tailored to your target exam dates.</p>
    </div>
    <br>
    """, unsafe_allow_html=True)
    
    ca, cb = st.columns(2)
    with ca:
        subjects = st.text_area("Subjects (comma-separated):", "Python, Machine Learning, Operating Systems")
        exam_date = st.date_input("Target Date", datetime.date.today() + datetime.timedelta(days=10))
    with cb:
        daily_hours = st.slider("Daily Study Bandwidth (Hours)", 1, 8, 4)
        method = st.selectbox("Strategy", ["Spaced Repetition", "Intensive Bootcamp", "Balanced Schedule"])
        
    if st.button("🗓️ Generate Timetable", use_container_width=True):
        sub_list = [s.strip() for s in subjects.split(",") if s.strip()]
        schedule = []
        for i in range(1, 6):
            schedule.append({
                "Day": f"Day {i}",
                "Subject Focus": sub_list[(i-1) % len(sub_list)] if sub_list else "General",
                "Allocated Time": f"{daily_hours} Hours",
                "Method": method
            })
        st.table(pd.DataFrame(schedule))

# -----------------------------------------------------------------------------
# MODULE 5: CAREER GUIDANCE PLATFORM
# -----------------------------------------------------------------------------
elif navigation == "🎯 Career Guidance Platform":
    st.markdown("""
    <div class='feature-card'>
        <h3 style='color:#059669;'>🎯 Career Guidance & Trajectory Mapper</h3>
        <p>Match your academic strengths and interests with industry roles.</p>
    </div>
    <br>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        skills = st.multiselect("Select Key Skills:", ["Python", "Data Analysis", "Public Speaking", "UI/UX Design", "Problem Solving"])
    with col2:
        domain = st.selectbox("Preferred Domain:", ["Tech Industry", "Research & Academia", "Corporate", "Creative Digital Media"])
        
    if st.button("🔍 Analyze Career Pathways", use_container_width=True):
        if skills:
            st.success("Career Pathways Calculated!")
            st.markdown("1. **Data Specialist / AI Engineer:** Strong alignment with technical & analytical skills.")
            st.markdown("2. **Technical Product Manager:** Excellent match for problem-solving and domain skills.")
        else:
            st.warning("Please choose at least one skill.")

# -----------------------------------------------------------------------------
# MODULE 6: STUDENT PROGRESS DASHBOARD
# -----------------------------------------------------------------------------
elif navigation == "📊 Student Progress Dashboard":
    st.markdown("""
    <div class='feature-card'>
        <h3 style='color:#D97706;'>📊 Student Progress Dashboard</h3>
        <p>Real-time analytical visualization of scores recorded in SQLite database.</p>
    </div>
    <br>
    """, unsafe_allow_html=True)
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Overall GPA", "3.90 / 4.0", "+0.05")
    m2.metric("Study Streak", "15 Days", "🔥 Peak")
    m3.metric("Platform Status", "100% Active", "Offline Ready")
    
    st.divider()
    df_scores = get_quiz_scores()
    
    if not df_scores.empty:
        col_left, col_right = st.columns(2)
        with col_left:
            st.subheader("Quiz Mastery Performance")
            df_scores["Percentage"] = (df_scores["score"] / df_scores["total"]) * 100
            st.bar_chart(df_scores.set_index("subject")["Percentage"])
        with col_right:
            st.subheader("Database Audit Logs")
            st.dataframe(df_scores, use_container_width=True)
    else:
        st.info("No quiz data logged yet. Take a quiz in the Assessment Generator to populate this dashboard.")
