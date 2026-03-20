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
        "Maths": "Practice maths problems daily and improve problem solving skills.",
        "Science": "Revise science concepts and use diagrams for better understanding.",
        "English": "Improve reading, writing, and vocabulary skills.",
        "Sinhala": "Practice grammar and essay writing regularly.",
        "History": "Study timelines and important events.",
        "ICT": "Improve practical and computer skills."
    }

    advice = advice_dict.get(weak, "Keep practicing all subjects.")

    # Results
    st.subheader("📊 Results")
    st.write(f"**Average Score:** {round(avg,2)}")
    st.write(f"**Performance:** {performance}")
    st.write(f"**Weak Subject:** {weak}")
    st.write(f"**Strong Subject:** {strong}")

    st.success(f"📌 Advice: {advice}")

    # Chart
    st.subheader("📈 Subject Performance")
    df_chart = pd.DataFrame({
        "Subjects": subjects,
        "Marks": marks
    })

    st.bar_chart(df_chart.set_index("Subjects"))
    st.subheader("Progress")
st.progress(int(avg))
if performance == "Excellent":
    st.success("Excellent Work! 🎉")
elif performance == "Good":
    st.info("Good Job 👍")
else:
    st.warning("Need Improvement ⚠️")
    import pandas as pd

df_chart = pd.DataFrame({
    "Subjects": subjects,
    "Marks": marks
})

st.bar_chart(df_chart.set_index("Subjects"))
if avg < 50:
    advice = "You should study more and focus on basics."
elif avg < 65:
    advice = "Practice past papers and improve weak areas."
else:
    advice = "Keep up the good work!"
    result_text = f"""
Average: {avg}
Performance: {performance}
Weak Subject: {weak}
Strong Subject: {strong}
Advice: {advice}
"""

st.download_button("📥 Download Report", result_text)
