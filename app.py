import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Student Performance Analyzer", layout="wide")

st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🎓 AI Student Performance Analyzer</h1>", unsafe_allow_html=True)

# SESSION
if "students" not in st.session_state:
    st.session_state.students = []

if "progress" not in st.session_state:
    st.session_state.progress = {}

# SIDEBAR
st.sidebar.header("📊 Student Info")
name = st.sidebar.text_input("Student Name")
goal = st.sidebar.number_input("🎯 Target Average", 0, 100, 75)

study_hours = st.slider("📚 Study Hours", 0, 10, 2)

# INPUT
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

# BUTTON
if st.button("🚀 Analyze Performance"):

    marks = [maths, science, english, sinhala, history, ict]
    subjects = ["Maths","Science","English","Sinhala","History","ICT"]

    avg = sum(marks) / len(marks)
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

    # Rank
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

    - Average: {round(avg,2)}
    - Predicted: {round(predicted,2)}
    - Grade: {grade}
    - Rank: {rank}
    - Weak Subject: 🔴 {weak}
    - Strong Subject: 🟢 {strong}
    """)

    # Goal
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

    # 📚 STUDY PLAN (NEW 🔥)
    st.subheader("📚 Personalized Study Plan")

    study_plan = {
        "Maths": {
            "plan": "Day 1: Algebra\nDay 2: Geometry\nDay 3: Past Papers",
            "link": "https://www.youtube.com/results?search_query=maths+basics"
        },
        "Science": {
            "plan": "Day 1: Theory\nDay 2: Diagrams\nDay 3: Revision",
            "link": "https://www.youtube.com/results?search_query=science+lessons"
        },
        "English": {
            "plan": "Day 1: Reading\nDay 2: Writing\nDay 3: Grammar",
            "link": "https://www.youtube.com/results?search_query=english+grammar"
        },
        "Sinhala": {
            "plan": "Day 1: Grammar\nDay 2: Essays\nDay 3: Reading",
            "link": "https://www.youtube.com/results?search_query=sinhala+lessons"
        },
        "History": {
            "plan": "Day 1: Events\nDay 2: Dates\nDay 3: Revision",
            "link": "https://www.youtube.com/results?search_query=history+lessons"
        },
        "ICT": {
            "plan": "Day 1: Theory\nDay 2: Practical\nDay 3: Revision",
            "link": "https://www.youtube.com/results?search_query=ict+lessons"
        }
    }

    plan = study_plan.get(weak)

    if plan:
        st.write(f"### 🔴 Focus on: {weak}")
        st.write(plan["plan"])
        st.markdown(f"[🎥 Watch Lessons]({plan['link']})")

    # Charts
    st.progress(int(avg))

    df = pd.DataFrame({"Subjects": subjects, "Marks": marks})
    st.bar_chart(df.set_index("Subjects"))

    fig, ax = plt.subplots()
    ax.pie(marks, labels=subjects, autopct='%1.1f%%')
    st.pyplot(fig)

# PROGRESS TRACKER
st.markdown("## 📈 Student Progress Tracker")

if name and name in st.session_state.progress:
    data = st.session_state.progress[name]

    dfp = pd.DataFrame({
        "Attempt": list(range(1, len(data)+1)),
        "Average": data
    })

    st.line_chart(dfp.set_index("Attempt"))

# RECORDS
if st.session_state.students:
    st.markdown("## 📋 Student Records")
    df_all = pd.DataFrame(st.session_state.students)
    st.dataframe(df_all)

# FOOTER
st.markdown("---")
st.markdown("🚀 Final AI Project | Dasun")
