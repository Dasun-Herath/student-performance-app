import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Student Performance Analyzer", layout="wide")

# 🎨 PRO UI STYLE
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}
.main {
    background-color: rgba(0,0,0,0);
}
.card {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 0px 10px rgba(0,0,0,0.5);
    margin-bottom: 20px;
}
.title {
    text-align: center;
    color: #4CAF50;
    font-size: 40px;
}
</style>
""", unsafe_allow_html=True)

# 🎓 TITLE
st.markdown("<h1 class='title'>🎓 AI Student Performance Analyzer</h1>", unsafe_allow_html=True)

# 🧠 SESSION
if "students" not in st.session_state:
    st.session_state.students = []

# 📌 SIDEBAR
st.sidebar.header("📊 Student Info")
name = st.sidebar.text_input("Student Name")
goal = st.sidebar.number_input("🎯 Target Average", 0, 100, 75)

# 📚 Study Hours
study_hours = st.slider("📚 Study Hours", 0, 10, 2)

# 📥 INPUTS
st.markdown("### 📥 Enter Marks")

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

    # 🤖 Prediction
    predicted = avg + (study_hours * 2)

    # 🎯 Save
    st.session_state.students.append({
        "Name": name if name else "Unknown",
        "Average": avg,
        "Grade": grade
    })

    # 🧾 RESULT CARD
    st.markdown(f"""
    <div class="card">
    <h2>📊 Results for {name if name else "Student"}</h2>
    <p>Average: {round(avg,2)}</p>
    <p>Predicted Score: {round(predicted,2)}</p>
    <p>Grade: {grade}</p>
    <p>Rank: {rank}</p>
    <p>Weak Subject: 🔴 {weak}</p>
    <p>Strong Subject: 🟢 {strong}</p>
    </div>
    """, unsafe_allow_html=True)

    # 🎯 Goal
    if avg >= goal:
        st.success("🎉 Goal Achieved!")
    else:
        st.warning("Keep working towards your goal!")

    # 📈 Progress
    st.progress(int(avg))

    # 📊 Chart
    df = pd.DataFrame({"Subjects": subjects, "Marks": marks})
    st.bar_chart(df.set_index("Subjects"))

    # 🥧 Pie
    fig, ax = plt.subplots()
    ax.pie(marks, labels=subjects, autopct='%1.1f%%')
    st.pyplot(fig)

# 📋 Records
if st.session_state.students:
    st.markdown("## 📋 Student Records")
    df_all = pd.DataFrame(st.session_state.students)
    st.dataframe(df_all)

    top = df_all.loc[df_all["Average"].idxmax()]
    st.success(f"🏆 Top Performer: {top['Name']} ({round(top['Average'],2)})")

# 📊 Dataset
st.markdown("## 📊 Dataset Analysis")

file = st.file_uploader("Upload CSV", type=["csv"])

if file:
    df = pd.read_csv(file)
    st.dataframe(df.head())

    if "Average" in df.columns:
        st.bar_chart(df["Average"])

# 🧾 FOOTER
st.markdown("---")
st.markdown("✨ Final AI Project | Developed by Dasun")
