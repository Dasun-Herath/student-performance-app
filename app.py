import streamlit as st
import pandas as pd
import pyrebase
from openai import OpenAI

st.set_page_config(page_title="Student Analyzer", layout="centered")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

firebaseConfig = {
    "apiKey": "AIzaSyC6OCrNCf-ETEejrair_J-wHnsYspOOk1I",
    "authDomain": "your-app.firebaseapp.com",
    "databaseURL": "https://student-app-3f444-default-rtdb.firebaseio.com/",
    "projectId": "student-app-3f444",
    "storageBucket": "your-app.appspot.com",
    "messagingSenderId": "477856584881",
    "appId": "XXX"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

if "user" not in st.session_state:
    st.session_state.user = None

menu = ["Login", "Signup"]
choice = st.sidebar.selectbox("Account", menu)

# SIGNUP
if choice == "Signup":
    st.title("Signup")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Create Account"):
        try:
            auth.create_user_with_email_and_password(email, password)
            st.success("Account created ✅")
        except Exception as e:
            st.error(e)

# LOGIN
if choice == "Login":
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.session_state.user = user
            st.success("Login success ✅")
        except Exception as e:
            st.error(e)

# AFTER LOGIN
if st.session_state.user:

    st.title("🎓 Student Performance Analyzer")

    name = st.text_input("Student Name")
    study_hours = st.slider("Study Hours", 0, 10, 2)

    maths = st.number_input("Maths", 0, 100)
    science = st.number_input("Science", 0, 100)
    english = st.number_input("English", 0, 100)
    sinhala = st.number_input("Sinhala", 0, 100)
    history = st.number_input("History", 0, 100)
    ict = st.number_input("ICT", 0, 100)

    if st.button("Analyze"):

        if name.strip() == "":
    st.error("❌ Please enter student name")
else:
    db.child("students").push({
        "name": name,
        "average": avg
    })
    
        marks = [maths, science, english, sinhala, history, ict]
        subjects = ["Maths","Science","English","Sinhala","History","ICT"]

        avg = sum(marks) / len(marks)

        weak = subjects[marks.index(min(marks))]
        strong = subjects[marks.index(max(marks))]

        st.subheader("📊 Results")
        st.write(f"Average: {round(avg,2)}")
        st.write(f"Weak Subject: {weak}")
        st.write(f"Strong Subject: {strong}")

        # 🚨 Smart Alerts
        st.subheader("⚠️ Smart Alerts")

        if avg < 50:
            st.error("🚨 Your performance is very low!")
        elif avg < 65:
            st.warning("⚠️ You can improve more.")
        else:
            st.success("✅ Good performance!")

        if min(marks) < 40:
            st.warning(f"⚠️ Improve {weak}")

        if study_hours < 2:
            st.warning("⏰ Increase study hours")

        # 📚 Study Plan
        st.subheader("📚 Study Plan")

        plan = []

        if study_hours <= 2:
            plan.append(f"Focus 1 hour on {weak}")
            plan.append("Revise basics")
        elif study_hours <= 5:
            plan.append(f"Spend 2 hours on {weak}")
            plan.append(f"1 hour on {strong}")
        else:
            plan.append(f"Deep study 3 hours on {weak}")
            plan.append("Practice papers")

        for p in plan:
            st.write("✅ " + p)

        # 🎥 YouTube Links
        st.subheader("🎥 Learning Resources")

        youtube_links = {
            "Maths": "https://www.youtube.com/results?search_query=maths+lessons",
            "Science": "https://www.youtube.com/results?search_query=science+lessons",
            "English": "https://www.youtube.com/results?search_query=english+grammar",
            "Sinhala": "https://www.youtube.com/results?search_query=sinhala+lessons",
            "History": "https://www.youtube.com/results?search_query=history+lessons",
            "ICT": "https://www.youtube.com/results?search_query=ict+lessons"
        }

        link = youtube_links.get(weak)

        st.write(f"📺 Learn {weak}:")
        st.markdown(f"[Click here to watch]({link})")

        # Firebase save
        try:
            db.child("students").push({
                "name": name,
                "average": avg
            })
            st.success("Saved to Firebase ✅")
        except Exception as e:
            st.error(e)

        df = pd.DataFrame({
            "Subjects": subjects,
            "Marks": marks
        })
        st.bar_chart(df.set_index("Subjects"))

    # 📈 Progress Tracker
    st.subheader("📈 Progress Tracker")

    try:
        data = db.child("students").get()
        records = []

        if data.each():
            for item in data.each():
                records.append(item.val())

        if records:
            df_progress = pd.DataFrame(records)
            st.line_chart(df_progress["average"])
        else:
            st.info("No data yet")

    except Exception as e:
        st.error(e)

    # 🏆 LEADERBOARD (FIXED)

st.subheader("🏆 Student Leaderboard")

try:
    data = db.child("students").get()
    records = []

    if data.each():
        for item in data.each():
            val = item.val()

            # ❗ FILTER empty names
            if val.get("name") and val.get("name") != "":
                records.append(val)

    if records:
        df_leaderboard = pd.DataFrame(records)

        df_leaderboard = df_leaderboard.sort_values(by="average", ascending=False)

        st.dataframe(df_leaderboard)

        st.subheader("🥇 Top 3 Students")

        top3 = df_leaderboard.head(3)

        for i, row in top3.iterrows():
            st.write(f"🏅 {row['name']} - {round(row['average'],2)}")

    else:
        st.info("No valid leaderboard data")

except Exception as e:
    st.error(e)
    # 🤖 AI Chatbot
    st.subheader("🤖 AI Assistant")

    question = st.text_input("Ask a question")

    if question:
        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You are a tutor."},
                    {"role": "user", "content": question}
                ]
            )
            st.success(response.choices[0].message.content)
        except Exception as e:
            st.error(e)
