import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Student Performance Analyzer", layout="wide")

# 🎨 STYLE
st.markdown("""
    <style>
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

# 🧠 SESSION STATE
if "students" not in st.session_state:
    st.session_state.students = []

# 📌 SIDEBAR
st.sidebar.header("📊 Student Info")
name = st.sidebar.text_input("Enter Student Name")

# 🎯 Goal Setting (NEW)
goal = st.sidebar.number_input("🎯 Target Average", 0, 100, 75)

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

    # 🤖 AI Prediction (NEW)
    predicted = avg + (study_hours * 2)

    # 📊 Save student
    st.session_state.students.append({
        "Name": name if name else "Unknown",
        "Average": avg,
        "Grade": grade,
        "Rank": rank
    })

    # 📊 Results
    st.markdown(f"""
    ## 📊 Results for {name if name else "Student"}

    - **Average:** {round(avg,2)}
    - **Predicted Next Score:** {round(predicted,2)}
    - **Grade:** {grade}
    - **Rank:** {rank}
    - **Weak Subject:** 🔴 {weak}
    - **Strong Subject:** 🟢 {strong}
    """)

    # 🎯 Goal Check (NEW)
    if avg >= goal:
        st.success("🎉 Goal Achieved!")
    else:
        st.warning("Keep working to reach your goal!")

    # 📈 Progress
    st.progress(int(avg))

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

# 📋 Student Records
if st.session_state.students:
    st.markdown("## 📋 Student Records")
    df_all = pd.DataFrame(st.session_state.students)
    st.dataframe(df_all)

    # 🏆 Top performer
    top = df_all.loc[df_all["Average"].idxmax()]
    st.success(f"🏆 Top Performer: {top['Name']} ({round(top['Average'],2)})")

    # 📥 Download
    csv = df_all.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Data", csv, "students.csv", "text/csv")

# 📊 DATASET DASHBOARD (NEW 🔥)
st.markdown("## 📊 Dataset Analysis")

uploaded_file = st.file_uploader("Upload CSV Dataset", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.write("### Preview")
    st.dataframe(df.head())

    if "Average" in df.columns:
        st.write("### Average Distribution")
        st.bar_chart(df["Average"])

# 🧾 FOOTER
st.markdown("---")
st.markdown("👨‍💻 Developed by Dasun | AI Project")
