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

st.sidebar.markdown("---")
st.sidebar.info("Fill marks and click Analyze")

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

    # 🎯 Performance
    if avg >= 80:
        performance = "Excellent"
    elif avg >= 65:
        performance = "Good"
    elif avg >= 50:
        performance = "Average"
    else:
        performance = "Needs Improvement"

    # 🧠 Advice
    if avg < 50:
        advice = "Study more and focus on basics."
    elif avg < 65:
        advice = "Practice past papers."
    else:
        advice = "Keep up the good work!"

    # 📊 RESULTS
    st.markdown(f"""
    ## 📊 Results for {name if name else "Student"}

    - **Average Score:** {round(avg,2)}
    - **Performance:** {performance}
    - **Weak Subject:** 🔴 {weak}
    - **Strong Subject:** 🟢 {strong}
    """)

    # 📈 Progress
    st.progress(int(avg))

    # 🎨 Message
    if performance == "Excellent":
        st.success("🌟 Excellent Work!")
    elif performance == "Good":
        st.info("👍 Good Job!")
    else:
        st.warning("⚠️ Need Improvement")

    # 📊 Bar Chart
    df = pd.DataFrame({
        "Subjects": subjects,
        "Marks": marks
    })
    st.markdown("### 📈 Bar Chart")
    st.bar_chart(df.set_index("Subjects"))

    # 🥧 Pie Chart
    st.markdown("### 🥧 Subject Distribution")
    fig, ax = plt.subplots()
    ax.pie(marks, labels=subjects, autopct='%1.1f%%')
    st.pyplot(fig)

    # 💡 Advice
    st.success(f"📌 Advice: {advice}")

    # 📥 Download
    result_text = f"""
Name: {name}
Average: {avg}
Performance: {performance}
Weak Subject: {weak}
Strong Subject: {strong}
Advice: {advice}
"""
    st.download_button("📥 Download Report", result_text)

# 🧾 FOOTER
st.markdown("---")
st.markdown("👨‍💻 Developed by Dasun | AI Project")
