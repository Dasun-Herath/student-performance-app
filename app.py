import streamlit as st
import pandas as pd
import pyrebase

st.set_page_config(page_title="Student App", layout="centered")

# Firebase config
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

# Session
if "page" not in st.session_state:
    st.session_state.page = "login"

if "user" not in st.session_state:
    st.session_state.user = None

# ================= LOGIN =================
if st.session_state.page == "login":

    st.title("🔐 Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.session_state.user = user
            st.session_state.page = "app"
            st.success("Login success ✅")
            st.rerun()
        except Exception as e:
            st.error("Login failed")

    if st.button("Go to Signup"):
        st.session_state.page = "signup"

# ================= SIGNUP =================
elif st.session_state.page == "signup":

    st.title("📝 Signup")

    email = st.text_input("New Email")
    password = st.text_input("New Password", type="password")

    if st.button("Create Account"):
        try:
            auth.create_user_with_email_and_password(email, password)
            st.success("Account created ✅")
        except Exception:
            st.error("Signup failed")

    if st.button("Back to Login"):
        st.session_state.page = "login"

# ================= APP =================
elif st.session_state.page == "app":

    st.title("🎓 Student Performance Analyzer")

    if st.button("Logout"):
        st.session_state.page = "login"
        st.session_state.user = None
        st.rerun()

    # Inputs
    name = st.text_input("Student Name")
    study_hours = st.slider("Study Hours", 0, 10, 2)

    maths = st.number_input("Maths", 0, 100)
    science = st.number_input("Science", 0, 100)
    english = st.number_input("English", 0, 100)
    sinhala = st.number_input("Sinhala", 0, 100)
    history = st.number_input("History", 0, 100)
    ict = st.number_input("ICT", 0, 100)

    # ================= ANALYZE =================
    if st.button("Analyze"):

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
        elif avg >= 50:
            grade = "C"
        else:
            grade = "F"

        # Results
        st.subheader("📊 Results")
        st.write("Average:", round(avg,2))
        st.write("Grade:", grade)
        st.write("Weak Subject:", weak)
        st.write("Strong Subject:", strong)

        # Smart Alerts
        st.subheader("⚠️ Smart Alerts")
        if avg < 50:
            st.error("Very low performance")
        elif avg < 65:
            st.warning("Can improve")
        else:
            st.success("Good performance")

        if min(marks) < 40:
            st.warning(f"Improve {weak}")

        if study_hours < 2:
            st.warning("Increase study hours")

        # Study Plan
        st.subheader("📚 Study Plan")
        if study_hours <= 2:
            st.write(f"Focus 1 hour on {weak}")
        elif study_hours <= 5:
            st.write(f"2 hours on {weak}, 1 hour on {strong}")
        else:
            st.write("Practice papers and revision")

        # YouTube
        st.subheader("🎥 Learning Resources")
        youtube_links = {
            "Maths": "https://www.youtube.com/results?search_query=maths",
            "Science": "https://www.youtube.com/results?search_query=science",
            "English": "https://www.youtube.com/results?search_query=english",
            "Sinhala": "https://www.youtube.com/results?search_query=sinhala",
            "History": "https://www.youtube.com/results?search_query=history",
            "ICT": "https://www.youtube.com/results?search_query=ict"
        }
        st.markdown(f"[Learn {weak}]({youtube_links.get(weak)})")

        # Save
        if name.strip() == "":
            st.error("Enter student name")
        else:
            try:
                db.child("students").push({
                    "name": name,
                    "average": avg
                })
                st.success("Saved ✅")
            except:
                st.error("Save failed")

        # Chart
        df = pd.DataFrame({
            "Subjects": subjects,
            "Marks": marks
        })
        st.bar_chart(df.set_index("Subjects"))

    # ================= LEADERBOARD =================
    st.subheader("🏆 Leaderboard")

    try:
        data = db.child("students").get()
        records = []

        if data.each():
            for item in data.each():
                val = item.val()
                if val.get("name"):
                    records.append(val)

        if records:
            df = pd.DataFrame(records)
            df = df.sort_values(by="average", ascending=False)

            df.index += 1
            st.dataframe(df)

            st.subheader("🥇 Top 3")
            for i, row in df.head(3).iterrows():
                st.write(f"{row['name']} - {round(row['average'],2)}")

        else:
            st.info("No data yet")

    except:
        st.error("Leaderboard error")

    # ================= PROGRESS =================
    st.subheader("📈 Progress")

    try:
        if records:
            df_progress = pd.DataFrame(records)
            st.line_chart(df_progress["average"])
    except:
        st.error("Progress error")
