import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Student Performance Analyzer", layout="wide")

# 🎨 STYLE
st.markdown("""
    <style>
    body {
        background-color: #0E1117;
        color: white;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# 🎓 TITLE
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🎓 AI Student Performance Analyzer</h1>", unsafe_allow_html=True)

# 📌 SIDEBAR
st.sidebar.header("📊 Student Info")
name = st.sidebar.text_input("Enter Student Name")

# 📚 Study Hours
study_hours = st.slider("📚 Daily Study Hours", 0, 10, 2)

# 📥 INPUTS
st.write("### Enter your marks")

col1, col2 = st.columns(2)

with col1:
    maths = st.number_input("Mathematics", 0, 100)
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

    # 🎯 Grade Prediction
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

    # 🎯 Performance
    if avg >= 80:
        performance = "Excellent"
    elif avg >= 65:
        performance = "Good"
    elif avg >= 50:
        performance = "Average"
    else:
        performance = "Needs Improvement"

    # 🏆 NEW FEATURE — Ranking System
    if avg >= 85:
        rank = "🥇 Top Performer"
    elif avg >= 70:
        rank = "🥈 Good Performer"
    elif avg >= 55:
        rank = "🥉 Average Performer"
    else:
        rank = "⚠️ Needs Improvement"

    # 📊 Class Average
    class_avg = 60

    # 📊 Results
    st.markdown(f"""
    ## 📊 Results for {name if name else "Student"}

    - **Average Score:** {round(avg,2)}
    - **Grade:** {grade}
    - **Performance:** {performance}
    - **Rank:** {rank}
    - **Weak Subject:** 🔴 {weak}
    - **Strong Subject:** 🟢 {strong}
    - **Class Average:** {class_avg}
    """)

    # 📈 Comparison
    if avg > class_avg:
        st.success("🎉 You are ABOVE class average!")
    elif avg == class_avg:
        st.info("😐 You are EXACTLY at class average.")
    else:
        st.warning("⚠️ You are BELOW class average. Try to improve!")

    # 📈 Progress
    st.progress(int(avg))

    # 📚 Study Advice
    if study_hours < 2:
        st.warning("Increase study time!")
    elif study_hours < 4:
        st.info("Good, but can improve.")
    else:
        st.success("Great study habit!")

    # 🔥 Weak Subject Suggestions
    resources = {
        "Maths": "📘 Practice maths problems daily.",
        "Science": "🔬 Use diagrams and experiments.",
        "English": "📖 Improve reading and writing.",
        "Sinhala": "✍️ Practice grammar.",
        "History": "📅 Study timelines.",
        "ICT": "💻 Practice computer skills."
    }

    st.info(f"📚 Suggestion for {weak}: {resources.get(weak)}")

    # 📊 Chart
    df = pd.DataFrame({
        "Subjects": subjects,
        "Marks": marks
    })
    st.bar_chart(df.set_index("Subjects"))

    # 🥧 Pie Chart
    fig, ax = plt.subplots()
    ax.pie(marks, labels=subjects, autopct='%1.1f%%')
    st.pyplot(fig)

    # 📥 Download
    result_text = f"""
Name: {name}
Average: {avg}
Grade: {grade}
Performance: {performance}
Rank: {rank}
Class Average: {class_avg}
Weak Subject: {weak}
Strong Subject: {strong}
"""
    st.download_button("📥 Download Report", result_text)

# 🧾 FOOTER
st.markdown("---")
st.markdown("👨‍💻 Developed by Dasun | AI Project")
