import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Student Performance Analyzer", layout="wide")

# 🔐 LOGIN SYSTEM
users = {
    "admin": "1234",
    "student": "pass"
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Login to Continue")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.success("Login Successful ✅")
            st.rerun()
        else:
            st.error("Invalid Username or Password ❌")

    st.stop()

# 🔓 LOGOUT
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

# 🎓 TITLE
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🎓 AI Student Performance Analyzer</h1>", unsafe_allow_html=True)

# 🧠 SESSION
if "students" not in st.session_state:
    st.session_state.students = []

if "progress" not in st.session_state:
    st.session_state.progress = {}

# 📌 SIDEBAR
st.sidebar.header("📊 Student Info")
name = st.sidebar.text_input("Student Name")
goal = st.sidebar.number_input("🎯 Target Average", 0, 100, 75)

study_hours = st.slider("📚 Study Hours", 0, 10, 2)

# 📥 INPUT
st.write("### Enter Marks")

col1, col2 = st.columns(2)

with col1:
    maths = st.number_input("Maths", 0, 100)
    science = st.number_input("Science", 0, 100)
    english = st.number_input("English", 0, 100)

with col2:
    sinhala = st.number_input("Sinhala", 0, 100)
    history = st.number_input("History", 0, 100)
    ict = st.number_input("ICT", 0, 100)

# 🔘 BUTTON
if st.button("🚀 Analyze Performance"):

    marks = [maths, science, english, sinhala, history, ict]
    subjects = ["Maths","Science","English","Sinhala","History","ICT"]

    avg = sum(marks) / len(marks)
    weak = subjects[marks.index(min(marks))]
    strong = subjects[marks.index(max(marks))]

    # 🎯 Grade
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

    # 🏆 Rank
    if avg >= 85:
        rank = "🥇 Top Performer"
    elif avg >= 70:
        rank = "🥈 Good Performer"
    elif avg >= 55:
        rank = "🥉 Average Performer"
    else:
        rank = "⚠️ Needs Improvement"

    predicted = avg + (study_hours * 2)

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
    st.markdown(f"""
    ## 📊 Results for {name if name else "Student"}

    - **Average:** {round(avg,2)}
    - **Predicted Score:** {round(predicted,2)}
    - **Grade:** {grade}
    - **Rank:** {rank}
    - **Weak Subject:** 🔴 {weak}
    - **Strong Subject:** 🟢 {strong}
    """)

    # GOAL
    if avg >= goal:
        st.success("🎉 Goal Achieved!")
    else:
        st.warning("Keep working!")

    # ALERT
    st.subheader("⚠️ Performance Alert System")

    if avg < 40:
        st.error("🚨 High Risk Student!")
    elif avg < 55:
        st.warning("⚠️ Below Average")
    elif avg >= 75:
        st.success("🎉 Excellent!")
    else:
        st.info("👍 Good")

    # 📚 STUDY PLAN
    st.subheader("📚 Personalized Study Plan")

    study_plan = {
        "Maths": {"plan": "Algebra → Geometry → Past Papers", "link": "https://www.youtube.com/results?search_query=maths+lessons"},
        "Science": {"plan": "Theory → Diagrams → Revision", "link": "https://www.youtube.com/results?search_query=science+lessons"},
        "English": {"plan": "Reading → Writing → Grammar", "link": "https://www.youtube.com/results?search_query=english+grammar"},
        "Sinhala": {"plan": "Grammar → Essays → Reading", "link": "https://www.youtube.com/results?search_query=sinhala+lessons"},
        "History": {"plan": "Events → Dates → Revision", "link": "https://www.youtube.com/results?search_query=history+lessons"},
        "ICT": {"plan": "Theory → Practical → Revision", "link": "https://www.youtube.com/results?search_query=ict+lessons"}
    }

    if weak in study_plan:
        st.write(f"🔴 Focus: {weak}")
        st.write(study_plan[weak]["plan"])
        st.markdown(f"[🎥 Watch Videos]({study_plan[weak]['link']})")

    # 📊 CHARTS
    st.progress(int(avg))

    df = pd.DataFrame({"Subjects": subjects, "Marks": marks})
    st.bar_chart(df.set_index("Subjects"))

    fig, ax = plt.subplots()
    ax.pie(marks, labels=subjects, autopct='%1.1f%%')
    st.pyplot(fig)

# 📈 PROGRESS TRACKER
st.markdown("## 📈 Student Progress Tracker")

if name and name in st.session_state.progress:
    data = st.session_state.progress[name]

    dfp = pd.DataFrame({
        "Attempt": list(range(1, len(data)+1)),
        "Average": data
    })

    st.line_chart(dfp.set_index("Attempt"))

# 📋 RECORDS
if st.session_state.students:
    st.markdown("## 📋 Student Records")
    df_all = pd.DataFrame(st.session_state.students)
    st.dataframe(df_all)

    top = df_all.loc[df_all["Average"].idxmax()]
    st.success(f"🏆 Top Performer: {top['Name']} ({round(top['Average'],2)})")

    csv = df_all.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Data", csv, "students.csv", "text/csv")

# 📊 DATASET
st.markdown("## 📊 Dataset Analysis")

file = st.file_uploader("Upload CSV", type=["csv"])

if file:
    df = pd.read_csv(file)
    st.dataframe(df.head())

    if "Average" in df.columns:
        st.bar_chart(df["Average"])

# FOOTER
st.markdown("---")
st.markdown("🚀 Final AI Project | Developed by Dasun")
