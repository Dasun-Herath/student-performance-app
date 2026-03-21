hart(df["Average"])

# 🧾 FOOTER
st.markdown("---")import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Student Performance Analyzer", layout="wide")

# 🎓 TITLE
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🎓 AI Student Performance Analyzer</h1>", unsafe_allow_html=True)

# 🧠 SESSION STATE
if "students" not in st.session_state:
    st.session_state.students = []

if "progress" not in st.session_state:
    st.session_state.progress = {}

# 📌 SIDEBAR
st.sidebar.header("📊 Student Info")
name = st.sidebar.text_input("Student Name")
goal = st.sidebar.number_input("🎯 Target Average", 0, 100, 75)

# 📚 Study Hours
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
if st.button("🚀 Analyze"):

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

    # 🤖 Prediction
    predicted = avg + (study_hours * 2)

    # 📊 SAVE STUDENT
    st.session_state.students.append({
        "Name": name if name else "Unknown",
        "Average": avg,
        "Grade": grade
    })

    # 📈 SAVE PROGRESS (NEW 🔥)
    if name:
        if name not in st.session_state.progress:
            st.session_state.progress[name] = []
        st.session_state.progress[name].append(avg)

    # 📊 RESULTS
    st.markdown(f"""
    ## 📊 Results for {name if name else "Student"}

    - Average: {round(avg,2)}
    - Predicted: {round(predicted,2)}
    - Grade: {grade}
    - Rank: {rank}
    - Weak: 🔴 {weak}
    - Strong: 🟢 {strong}
    """)

    # 🎯 Goal
    if avg >= goal:
        st.success("🎉 Goal Achieved!")
    else:
        st.warning("Keep working!")

    # 📈 Progress bar
    st.progress(int(avg))

    # 📊 Bar chart
    df = pd.DataFrame({"Subjects": subjects, "Marks": marks})
    st.bar_chart(df.set_index("Subjects"))

    # 🥧 Pie chart
    fig, ax = plt.subplots()
    ax.pie(marks, labels=subjects, autopct='%1.1f%%')
    st.pyplot(fig)

# 📈 PROGRESS TRACKER DISPLAY (NEW 🔥)
st.markdown("## 📈 Student Progress Tracker")

if name and name in st.session_state.progress:
    progress_data = st.session_state.progress[name]

    df_progress = pd.DataFrame({
        "Attempt": list(range(1, len(progress_data)+1)),
        "Average": progress_data
    })

    st.line_chart(df_progress.set_index("Attempt"))

# 📋 STUDENT RECORDS
if st.session_state.students:
    st.markdown("## 📋 Student Records")
    df_all = pd.DataFrame(st.session_state.students)
    st.dataframe(df_all)

    top = df_all.loc[df_all["Average"].idxmax()]
    st.success(f"🏆 Top Performer: {top['Name']} ({round(top['Average'],2)})")

# 🧾 FOOTER
st.markdown("---")
st.markdown("🚀 Final AI Project | Dasun")
