import streamlit as st
import pandas as pd
import pyrebase
from openai import OpenAI

st.set_page_config(page_title="Student Analyzer", layout="centered")

# 🔥 OPENAI API (replace key)
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🔥 FIREBASE CONFIG (replace yours)
firebaseConfig = {
    "apiKey": "YOUR_KEY",
    "authDomain": "YOUR_DOMAIN",
    "databaseURL": "YOUR_DB_URL",
    "projectId": "YOUR_ID",
    "storageBucket": "YOUR_BUCKET",
    "messagingSenderId": "XXX",
    "appId": "XXX"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

# SESSION
if "user" not in st.session_state:
    st.session_state.user = None

# MENU
menu = ["Login", "Signup"]
choice = st.sidebar.selectbox("Account", menu)

# SIGNUP
if choice == "Signup":
    st.title("Create Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Signup"):
        try:
            auth.create_user_with_email_and_password(email, password)
            st.success("Account created ✅")
        except:
            st.error("Signup failed ❌")

# LOGIN
if choice == "Login":
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.session_state.user = user
            st.success("Login success ✅")
        except:
            st.error("Login failed ❌")

# AFTER LOGIN
if st.session_state.user:

    st.title("🎓 Student Performance Analyzer")

    # SESSION STORAGE
    if "progress" not in st.session_state:
        st.session_state.progress = {}

    if "subject_progress" not in st.session_state:
        st.session_state.subject_progress = {}

    # INPUT
    name = st.text_input("Student Name")
    study_hours = st.slider("Study Hours", 0, 10, 2)

    maths = st.number_input("Maths", 0, 100)
    science = st.number_input("Science", 0, 100)
    english = st.number_input("English", 0, 100)
    sinhala = st.number_input("Sinhala", 0, 100)
    history = st.number_input("History", 0, 100)
    ict = st.number_input("ICT", 0, 100)

    if st.button("🚀 Analyze"):

        marks = [maths, science, english, sinhala, history, ict]
        subjects = ["Maths","Science","English","Sinhala","History","ICT"]

        avg = sum(marks)/len(marks)
        weak = subjects[marks.index(min(marks))]
        strong = subjects[marks.index(max(marks))]

        # 🎯 Exam readiness
        readiness = (avg * 0.7) + (study_hours * 5)
        readiness = max(0, min(100, readiness))

        # 🎮 Gamification
        points = int(avg)
        if avg >= 85:
            badge = "🏆 Gold"
        elif avg >= 70:
            badge = "🥈 Silver"
        elif avg >= 55:
            badge = "🥉 Bronze"
        else:
            badge = "📘 Beginner"

        # SAVE LOCAL PROGRESS
        if name:
            st.session_state.progress.setdefault(name, []).append(avg)

            st.session_state.subject_progress.setdefault(name, {
                "Maths":[], "Science":[], "English":[],
                "Sinhala":[], "History":[], "ICT":[]
            })

            st.session_state.subject_progress[name]["Maths"].append(maths)
            st.session_state.subject_progress[name]["Science"].append(science)
            st.session_state.subject_progress[name]["English"].append(english)
            st.session_state.subject_progress[name]["Sinhala"].append(sinhala)
            st.session_state.subject_progress[name]["History"].append(history)
            st.session_state.subject_progress[name]["ICT"].append(ict)

        # SAVE FIREBASE
        db.child("students").push({
            "name": name,
            "maths": maths,
            "science": science,
            "english": english,
            "average": avg
        })

        # RESULTS
        st.subheader("📊 Results")
        st.write(f"Average: {round(avg,2)}")
        st.write(f"Weak: {weak}")
        st.write(f"Strong: {strong}")

        st.subheader("🎯 Exam Readiness")
        st.write(f"{round(readiness,2)}%")
        st.progress(int(readiness))

        st.subheader("🎮 Gamification")
        st.write(f"Points: {points}")
        st.write(f"Badge: {badge}")

        df = pd.DataFrame({"Subjects": subjects, "Marks": marks})
        st.bar_chart(df.set_index("Subjects"))

    # 📈 PROGRESS
    if name in st.session_state.progress:
        st.subheader("📈 Overall Progress")
        st.line_chart(st.session_state.progress[name])

    if name in st.session_state.subject_progress:
        st.subheader("📊 Subject-wise Progress")
        df_sub = pd.DataFrame(st.session_state.subject_progress[name])
        st.line_chart(df_sub)

    # 🤖 REAL AI CHATBOT
    st.subheader("🤖 AI Study Assistant")

    user_question = st.text_input("Ask anything about studies...")

    if user_question:
        with st.spinner("Thinking... 🤖"):
            try:
                response = client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful student tutor."},
                        {"role": "user", "content": user_question}
                    ]
                )

                answer = response.choices[0].message.content
                st.success(answer)

            except:
                st.error("AI Error ❌ Check API key")

    st.markdown("---")
    st.write("🚀 Developed by Dasun")
