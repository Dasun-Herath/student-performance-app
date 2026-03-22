import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 📱 Mobile UI
st.set_page_config(page_title="Student Analyzer", layout="centered")

# 🔐 LOGIN
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

# 🔓 Logout
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

# 🔥 NEW SUBJECT PROGRESS
if "subject_progress" not in st.session_state:
    st.session_state.subject_progress = {}

# INPUT
st.write("### Enter Marks")

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

    # SAVE GENERAL DATA
    st.session_state.students.append({
        "Name": name if name else "Unknown",
        "Average": avg
    })

    # 📈 SAVE TOTAL PROGRESS
    if name:
        if name not in st.session_state.progress:
            st.session_state.progress[name] = []
        st.session_state.progress[name].append(avg)

    # 📊 SAVE SUBJECT PROGRESS
    if name:
        if name not in st.session_state.subject_progress:
            st.session_state.subject_progress[name] = {
                "Maths": [],
                "Science": [],
                "English": [],
                "Sinhala": [],
                "History": [],
                "ICT": []
            }

        st.session_state.subject_progress[name]["Maths"].append(maths)
        st.session_state.subject_progress[name]["Science"].append(science)
        st.session_state.subject_progress[name]["English"].append(english)
        st.session_state.subject_progress[name]["Sinhala"].append(sinhala)
        st.session_state.subject_progress[name]["History"].append(history)
        st.session_state.subject_progress[name]["ICT"].append(ict)

    # RESULTS
    st.write("## Results")
    st.write(f"Average: {round(avg,2)}")
    st.write(f"Weak: {weak}")
    st.write(f"Strong: {strong}")

    # 🎯 Readiness
    st.subheader("Exam Readiness")
    st.write(f"{round(readiness,2)}%")
    st.progress(int(readiness))

    # 🎮 Gamification
    st.subheader("Gamification")
    st.write(f"Points: {points}")
    st.write(f"Badge: {badge}")

    # 📚 Study Tip
    st.subheader("Study Tip")
    st.write(f"Focus more on {weak}")

    # Chart
    df = pd.DataFrame({"Subjects": subjects, "Marks": marks})
    st.bar_chart(df.set_index("Subjects"))

# 📈 TOTAL PROGRESS
st.markdown("## 📈 Overall Progress")

if name and name in st.session_state.progress:
    st.line_chart(st.session_state.progress[name])

# 📊 SUBJECT PROGRESS (NEW 🔥)
st.markdown("## 📊 Subject-wise Progress")

if name and name in st.session_state.subject_progress:
    df_sub = pd.DataFrame(st.session_state.subject_progress[name])
    st.line_chart(df_sub)

# 🧑‍🏫 ADMIN DASHBOARD
if st.session_state.user == "admin":
    st.write("## Admin Dashboard")

    if st.session_state.students:
        df_all = pd.DataFrame(st.session_state.students)

        st.write("Class Average:", round(df_all["Average"].mean(),2))

        top = df_all.loc[df_all["Average"].idxmax()]
        st.write("Top Performer:", top["Name"])

        weak_students = df_all[df_all["Average"] < 50]
        st.write("Weak Students:")
        st.dataframe(weak_students)

# 🤖 AI CHATBOT
st.markdown("## 🤖 AI Assistant")

q = st.text_input("Ask question")

if q:
    if "math" in q.lower():
        st.write("Practice maths daily.")
    elif "english" in q.lower():
        st.write("Improve vocabulary.")
    elif "science" in q.lower():
        st.write("Revise with diagrams.")
    else:
        st.write("Study regularly and stay focused.")

# FOOTER
st.markdown("---")
st.write("🚀 Developed by Dasun")
