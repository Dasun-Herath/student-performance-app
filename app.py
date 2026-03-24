import streamlit as st
import pandas as pd
import pyrebase
from openai import OpenAI

st.set_page_config(page_title="Student Analyzer", layout="centered")

# OpenAI API
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Firebase Config (REPLACE WITH YOURS)
firebaseConfig = {
    "apiKey": "AIzaSyC6OCrNCf-ETEejrair_J-wHnsYspOOk1I",
    "authDomain": "your-app.firebaseapp.com",
    "databaseURL": "https://student-app-3f444-default-rtdb.firebaseio.com/
:",
    "projectId": "student-app-3f444",
    "storageBucket": "your-app.appspot.com",
    "messagingSenderId": "477856584881",
    "appId": "XXX"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

# Session
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

        marks = [maths, science, english, sinhala, history, ict]
        subjects = ["Maths","Science","English","Sinhala","History","ICT"]

        avg = sum(marks) / len(marks)

        weak = subjects[marks.index(min(marks))]
        strong = subjects[marks.index(max(marks))]

        st.subheader("📊 Results")
        st.write(f"Average: {round(avg,2)}")
        st.write(f"Weak Subject: {weak}")
        st.write(f"Strong Subject: {strong}")

        # Firebase save
        try:
            db.child("students").push({
                "name": name,
                "average": avg
            })
            st.success("Saved to Firebase ✅")
        except Exception as e:
            st.error(e)

        # Chart
        df = pd.DataFrame({
            "Subjects": subjects,
            "Marks": marks
        })
        st.bar_chart(df.set_index("Subjects"))

    # AI Chatbot
    st.subheader("🤖 AI Study Assistant")

    question = st.text_input("Ask a question")

    if question:
        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful tutor."},
                    {"role": "user", "content": question}
                ]
            )
            st.success(response.choices[0].message.content)
        except Exception as e:
            st.error(e)
