import os
import json
import sqlite3
from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from google import genai
from google.genai import types

# -----------------------------------------------------------------------------
# 1. DATABASE SETUP & PERSISTENCE (SQLite)
# -----------------------------------------------------------------------------
DB_FILE = "eduverse.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Table for chat history
    c.execute('''
        CREATE TABLE IF NOT EXISTS chat_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            role TEXT,
            content TEXT
        )
    ''')
    # Table for student quiz scores & activity
    c.execute('''
        CREATE TABLE IF NOT EXISTS student_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            subject TEXT,
            score INTEGER,
            total INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def save_chat(role, content):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO chat_logs (timestamp, role, content) VALUES (?, ?, ?)",
              (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), role, content))
    conn.commit()
    conn.close()

def load_chats():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT role, content FROM chat_logs ORDER BY id ASC")
    rows = c.fetchall()
    conn.close()
    return [{"role": r[0], "content": r[1]} for r in rows]

def clear_db_chats():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM chat_logs")
    conn.commit()
    conn.close()

def log_score(subject, score, total):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO student_scores (timestamp, subject, score, total) VALUES (?, ?, ?, ?)",
              (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), subject, score, total))
    conn.commit()
    conn.close()

def get_scores():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM student_scores", conn)
    conn.close()
    return df

# Initialize DB on load
init_db()

# -----------------------------------------------------------------------------
# 2. STREAMLIT CONFIGURATION & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="EduVerse AI - All-in-One Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-title { font-size: 2.3rem; color: #1E88E5; font-weight: 800; text-align: center; margin-bottom: 0px; }
    .subtitle { font-size: 1.1rem; color: #555555; text-align: center; margin-bottom: 25px; }
    .card { background-color: #f8f9fa; border-radius: 10px; padding: 20px; border-left: 5px solid #1E88E5; margin-bottom: 15px; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { padding-left: 16px; padding-right: 16px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>🎓 EduVerse AI</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Unified AI-Powered Ecosystem for Personalized Learning & Teaching</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. GEMINI API SETUP
# -----------------------------------------------------------------------------
st.sidebar.title("⚙️ Global Settings")

# Retrieve API key from secrets, environment, or user input
api_key = st.sidebar.text_input("Gemini API Key:", type="password")
if not api_key:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
    elif os.environ.get("GEMINI_API_KEY"):
        api_key = os.environ.get("GEMINI_API_KEY")

client = None
if api_key:
    try:
        client = genai.Client(api_key=api_key)
        st.sidebar.success("✅ Gemini API Active")
    except Exception as e:
        st.sidebar.error(f"API Error: {e}")
else:
    st.sidebar.warning("⚠️ Enter Gemini API Key to enable AI features.")

MODEL_NAME = "gemini-2.5-flash"

# Sidebar Quick Actions
st.sidebar.divider()
st.sidebar.subheader("🗄️ Database Operations")
if st.sidebar.button("Reset Chat Logs"):
    clear_db_chats()
    st.session_state.chat_history = []
    st.sidebar.success("Chat history cleared from database!")
    st.rerun()

# -----------------------------------------------------------------------------
# 4. MODULE TABS
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🧠 AI Tutor", 
    "⚡ Doubt Solver", 
    "📝 Quiz & Assignments", 
    "🗓️ Study Planner", 
    "🎯 Career Pathways", 
    "📊 Progress Analytics"
])

# -----------------------------------------------------------------------------
# TAB 1: SOCRATIC TUTOR
# -----------------------------------------------------------------------------
with tab1:
    st.header("🧠 24/7 Socratic AI Tutor")
    st.caption("Guiding students step-by-step without revealing answers directly.")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = load_chats()
        
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
    if prompt := st.chat_input("Ask a question about Math, Science, History..."):
        # Display user message
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        save_chat("user", prompt)
        with st.chat_message("user"):
            st.write(prompt)
            
        if client:
            try:
                sys_instruct = (
                    "You are a helpful Socratic tutor. Never reveal the direct answer immediately. "
                    "Ask guiding questions to help the student derive the answer step-by-step. "
                    "Keep explanations clear, supportive, and concise."
                )
                
                formatted_contents = [
                    types.Content(
                        role="user" if m["role"] == "user" else "model",
                        parts=[types.Part.from_text(text=m["content"])]
                    ) for m in st.session_state.chat_history
                ]
                
                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=formatted_contents,
                    config=types.GenerateContentConfig(
                        system_instruction=sys_instruct,
                        temperature=0.7
                    )
                )
                
                bot_reply = response.text
                st.session_state.chat_history.append({"role": "model", "content": bot_reply})
                save_chat("model", bot_reply)
                with st.chat_message("assistant"):
                    st.write(bot_reply)
            except Exception as e:
                st.error(f"Generation error: {e}")
        else:
            st.error("Please add your Gemini API Key in the sidebar.")

# -----------------------------------------------------------------------------
# TAB 2: INSTANT DOUBT SOLVER
# -----------------------------------------------------------------------------
with tab2:
    st.header("⚡ Instant Doubt Resolution Assistant")
    st.caption("Upload images of equations, diagrams, or handwritten notes.")
    
    col_up, col_out = st.columns([1, 1])
    
    with col_up:
        uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
        extra_query = st.text_input("Additional Instructions (Optional):", value="Explain the core steps to solve this problem.")
        
        if uploaded_file:
            img = Image.open(uploaded_file)
            st.image(img, caption="Uploaded Homework / Diagram", use_container_width=True)
            
    with col_out:
        st.subheader("AI Analysis & Solution")
        if uploaded_file:
            if st.button("Analyze & Solve Doubt"):
                if client:
                    with st.spinner("Processing image and mathematical expressions..."):
                        try:
                            res = client.models.generate_content(
                                model=MODEL_NAME,
                                contents=[img, extra_query],
                                config=types.GenerateContentConfig(
                                    system_instruction="Read any text, formulas, or diagrams in the image. Provide a detailed step-by-step explanation using standard LaTeX formatting for math equations."
                                )
                            )
                            st.markdown(res.text)
                        except Exception as e:
                            st.error(f"Vision model error: {e}")
                else:
                    st.error("Please enter your API key.")
        else:
            st.info("Upload an image on the left to see the step-by-step breakdown.")

# -----------------------------------------------------------------------------
# TAB 3: QUIZ & ASSIGNMENT GENERATOR
# -----------------------------------------------------------------------------
with tab3:
    st.header("📝 Quiz & Assignment Generator")
    st.caption("Automated assessment creation for teachers and educators.")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        subject_input = st.text_input("Subject / Topic", "Newton's Laws of Motion")
    with c2:
        target_grade = st.selectbox("Grade Level", ["Elementary School", "Middle School", "High School", "Undergraduate"])
    with c3:
        num_q = st.slider("Number of Items", 1, 10, 4)
        
    content_format = st.radio("Output Type", ["Multiple Choice Quiz", "Short Answer Assignment", "Study Flashcards"], horizontal=True)
    
    if st.button("Generate Assessment Material"):
        if client:
            with st.spinner("Drafting curriculum content..."):
                prompt = (
                    f"Create a {content_format} on topic '{subject_input}' for {target_grade} level. "
                    f"Include {num_q} questions along with an explicit answer key and scoring criteria."
                )
                try:
                    res = client.models.generate_content(model=MODEL_NAME, contents=prompt)
                    st.success("Generation Complete!")
                    st.markdown(res.text)
                    
                    st.download_button(
                        label="📥 Download Markdown File",
                        data=res.text,
                        file_name=f"{subject_input.replace(' ', '_')}_assignment.md",
                        mime="text/markdown"
                    )
                except Exception as e:
                    st.error(f"Error generating assignment: {e}")
        else:
            st.error("Please input Gemini API key.")

# -----------------------------------------------------------------------------
# TAB 4: DYNAMIC STUDY PLANNER
# -----------------------------------------------------------------------------
with tab4:
    st.header("🗓️ Adaptive Study Planner")
    st.caption("Personalized schedule mapping spaced repetition and exam deadlines.")
    
    sp_col1, sp_col2 = st.columns(2)
    with sp_col1:
        topics_list = st.text_area("Topics to Study (comma-separated):", "Calculus Integrals, Data Structures, Linear Algebra")
        target_date = st.date_input("Target Exam / Completion Date")
    with sp_col2:
        daily_hours = st.slider("Daily Available Hours", 1, 12, 3)
        focus_type = st.selectbox("Primary Focus", ["Balanced Practice & Theory", "Exam Cramming", "Concept Mastery"])
        
    if st.button("Create Personalized Schedule"):
        if client:
            with st.spinner("Optimizing study time blocks..."):
                prompt = (
                    f"Generate a detailed study timetable leading to {target_date}. "
                    f"Topics: {topics_list}. Daily study limit: {daily_hours} hours. Focus: {focus_type}. "
                    "Include review intervals and break recommendations."
                )
                try:
                    res = client.models.generate_content(model=MODEL_NAME, contents=prompt)
                    st.markdown(res.text)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.error("API Key required.")

# -----------------------------------------------------------------------------
# TAB 5: CAREER GUIDANCE
# -----------------------------------------------------------------------------
with tab5:
    st.header("🎯 AI Career & Skill Pathways")
    st.caption("Align student strengths with current workforce opportunities.")
    
    cg_col1, cg_col2 = st.columns(2)
    with cg_col1:
        user_skills = st.text_area("Your Skills & Interests:", "Python programming, creative writing, statistics, project leading")
    with cg_col2:
        preferred_work = st.multiselect("Preferred Environment", ["Tech Startup", "Corporate Office", "Academic Research", "Remote Work", "Creative Agency"])
        
    if st.button("Generate Career Analysis"):
        if client:
            with st.spinner("Matching career vectors..."):
                prompt = (
                    f"Student Skills/Interests: {user_skills}. Preferred Environments: {', '.join(preferred_work)}. "
                    "Provide 3 tailored career paths. For each, outline: 1) Essential skills to learn, "
                    "2) Recommended degrees or certifications, and 3) Practical 6-month roadmap."
                )
                try:
                    res = client.models.generate_content(model=MODEL_NAME, contents=prompt)
                    st.markdown(res.text)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.error("API Key required.")

# -----------------------------------------------------------------------------
# TAB 6: PROGRESS ANALYTICS DASHBOARD
# -----------------------------------------------------------------------------
with tab6:
    st.header("📊 Student Progress Analytics")
    st.caption("Track mastery scores and log interactive test results into SQLite.")
    
    # Form to simulate logging new scores
    with st.expander("➕ Log Test Result (Teacher/Student)"):
        with st.form("score_form"):
            form_subj = st.selectbox("Subject", ["Mathematics", "Physics", "Computer Science", "Chemistry", "Literature"])
            form_score = st.number_input("Score Achieved", min_value=0, max_value=100, value=85)
            form_total = st.number_input("Total Possible", min_value=10, max_value=100, value=100)
            submitted = st.form_submit_button("Log Score to Database")
            if submitted:
                log_score(form_subj, form_score, form_total)
                st.success(f"Recorded score for {form_subj}!")
                
    # Load and render score data
    scores_df = get_scores()
    
    if not scores_df.empty:
        col_db_left, col_db_right = st.columns([1, 1])
        with col_db_left:
            st.subheader("Mastery Performance Chart")
            # Calculate percentage for native bar chart rendering
            chart_df = scores_df.copy()
            chart_df['Score (%)'] = (chart_df['score'] / chart_df['total']) * 100
            st.bar_chart(chart_df.set_index('subject')['Score (%)'])
            
        with col_db_right:
            st.subheader("Database Audit Table")
            st.dataframe(scores_df, use_container_width=True)
    else:
        st.info("No test scores recorded yet. Expand the box above to add entries.")
