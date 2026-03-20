import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Student Performance Analyzer", layout="centered")

st.title("🎓 AI Student Performance Analyzer")

st.write("Enter your marks:")

# Input fields
maths = st.number_input("Mathematics", 0, 100)
science = st.number_input("Science", 0, 100)
english = st.number_input("English", 0, 100)
sinhala = st.number_input("Sinhala", 0, 100)
history = st.number_input("History", 0, 100)
ict = st.number_input("ICT", 0, 100)

if st.button("Analyze Performance"):

    marks = [maths, science, english, sinhala, history, ict]
    subjects = ["Maths","Science","English","Sinhala","History","ICT"]

    avg = sum(marks) / len(marks)

    weak = subjects[marks.index(min(marks))]
    strong = subjects[marks.index(max(marks))]

    # Performance category
    if avg >= 80:
        performance = "Excellent"
    elif avg >= 65:
        performance = "Good"
    elif avg >= 50:
        performance = "Average"
    else:
        performance = "Needs Improvement"

    # AI Advice
    advice_dict = {
        "Maths": "Practice maths problems daily.",
        "Science": "Revise concepts with diagrams.",
        "English": "Improve reading and vocabulary.",
        "Sinhala": "Practice grammar and writing.",
        "History": "Study important events.",
        "ICT": "Improve practical skills."
    }

    advice = advice_dict.get(weak, "Keep practicing.")

    # Results
    st.subheader("📊 Results")
    st.write(f"**Average Score:** {round(avg,2)}")
    st.write(f"**Performance:** {performance}")
    st.write(f"**Weak Subject:** {weak}")
    st.write(f"**Strong Subject:** {strong}")

    # Progress bar
    st.subheader("Progress")
    st.progress(int(avg))

    # Performance message
    if performance == "Excellent":
        st.success("Excellent Work! 🎉")
    elif performance == "Good":
        st.info("Good Job 👍")
    else:
        st.warning("Need Improvement ⚠️")

    # Chart
    st.subheader("📈 Subject Performance")
    df_chart = pd.DataFrame({
        "Subjects": subjects,
        "Marks": marks
    })
    st.bar_chart(df_chart.set_index("Subjects"))

    # Final advice upgrade
    if avg < 50:
        final_advice = "Study more and focus on basics."
    elif avg < 65:
        final_advice = "Practice past papers."
    else:
        final_advice = "Keep up the good work!"

    st.success(f"📌 Advice: {final_advice}")

    # Download report
    result_text = f"""
Average: {avg}
Performance: {performance}
Weak Subject: {weak}
Strong Subject: {strong}
Advice: {final_advice}
"""

    st.download_button("📥 Download Report", result_text)
    st.markdown("""
    <style>
    .main {
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
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🎓 Student Performance Analyzer</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

with col1:
    maths = st.number_input("Mathematics", 0, 100)
    science = st.number_input("Science", 0, 100)
    english = st.number_input("English", 0, 100)

with col2:
    sinhala = st.number_input("Sinhala", 0, 100)
    history = st.number_input("History", 0, 100)
    ict = st.number_input("ICT", 0, 100)
    st.markdown(f"""
### 📊 Results

- **Average Score:** {round(avg,2)}
- **Performance:** {performance}
- **Weak Subject:** 🔴 {weak}
- **Strong Subject:** 🟢 {strong}
""")
    st.markdown("### 📈 Performance Chart")
st.bar_chart(df_chart.set_index("Subjects"))

