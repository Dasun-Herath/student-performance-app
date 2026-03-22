import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 📱 Mobile Friendly Config
st.set_page_config(page_title="Student Analyzer", layout="centered")

# 🔐 LOGIN SYSTEM
users = {"admin": "1234", "student": "pass"}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = ""

if not st.session_state.logged_in:
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.session_state.user = username
            st.success("Login Success ✅")
            st.rerun()
        else:
            st.error("Invalid Login ❌")

    st.stop()

# 🔓 LOGOUT
if st.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user = ""
    st.rerun()

# 🎓 TITLE
st.markdown("<h2 style='text-align: center;'>📱 Student Performance App</h2>", unsafe_allow_html=True)

# SESSION STORAGE
if "students" not in st.session_state:
    st.session_state.students = []

if "progress" not in st.session_state:
    st.session_state.progress = {}

# INPUT
st.write("### 📱 Enter Your Marks")

name = st.text_input("Student Name")
study_hours = st.slider("Study Hours", 0, 10, 2)
goal = st.number_input("Target Average", 0, 100, 75)

maths = st.number_input("Maths", 0, 100)
science = st.number_input("Science", 0, 100)
english = st.number_input("English", 0, 100)
sinhala = st.number_input("Sinhala", 0, 100)
history = st.number_input("History", 0, 100)
ict = st.number_input("ICT", 0, 100)

# ANALYZE
if st.button("🚀 Analyze"):

    marks = [maths, science, english, sinhala, history, ict]
    subjects = ["Maths","Science","English","Sinhala","History","ICT"]

    avg = sum(marks)/len(marks)
    weak = subjects[marks.index(min(marks))]
    strong = subjects[marks.index(max(marks))]

    # Grade
    if avg >= 75:
        grade = "A"
    elif avg >= 65:
        grade = "B"
    elif avg >= 55:
        grade = "C"
    elif avg >= 40:
        grade = "S"
    else:
        grade = "F"

    # 🎯 Exam Readiness
    readiness = (avg * 0.7) + (study_hours * 5)
    if avg < 50:
        readiness -= 10
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

    # SAVE
    st.session_state.students.append({
        "Name": name if name else "Unknown",
        "Average": avg,
        "Grade": grade
    })

    if name:
        if name not in st.session_state.progress:
            st.session_state.progress[name] = []
        st.session_state.progress[name].append(avg)

    # RESULTS
    st.write("## 📊 Results")
    st.write(f"Average: {round(avg,2)}")
    st.write(f"Grade: {grade}")
    st.write(f"Weak: {weak}")
    st.write(f"Strong: {strong}")

    # 🎯 Readiness
    st.subheader("🎯 Exam Readiness")
    st.write(f"{round(readiness,2)}%")
    st.progress(int(readiness))

    # 🎮 Gamification
    st.subheader("🎮 Gamification")
    st.write(f"Points: {points}")
    st.write(f"Badge: {badge}")

    # 📚 Study Plan
    st.subheader("📚 Study Plan")
    st.write(f"Focus on: {weak}")

    # 📊 Chart
    df = pd.DataFrame({"Subjects": subjects, "Marks": marks})
    st.bar_chart(df.set_index("Subjects"))

# 📈 Progress Tracker
if name and name in st.session_state.progress:
    st.line_chart(st.session_state.progress[name])

# 🧑‍🏫 Admin Dashboard
if st.session_state.user == "admin":
    st.write("## 🧑‍🏫 Admin Dashboard")

    if st.session_state.students:
        df_all = pd.DataFrame(st.session_state.students)

        st.write("Class Average:", round(df_all["Average"].mean(),2))

        top = df_all.loc[df_all["Average"].idxmax()]
        st.write("Top Performer:", top["Name"])

        weak_students = df_all[df_all["Average"] < 50]
        st.write("Weak Students:")
        st.dataframe(weak_students)

# 🤖 AI Chatbot
st.markdown("## 🤖 AI Assistant")

q = st.text_input("Ask study question")

if q:
    if "math" in q.lower():
        st.write("Practice daily maths problems.")
    elif "english" in q.lower():
        st.write("Improve reading and vocabulary.")
    else:
        st.write("Stay focused and study regularly.")

# FOOTER
st.markdown("---")
st.write("🚀 Developed by Dasun")
