import streamlit as st
import pandas as pd
import datetime
import os
import random
import string

# Ensure directories exist
if not os.path.exists("apollo_photos"):
    os.makedirs("apollo_photos")

# CSV File Setup
RESPONSES_CSV = "siri_solvers_responses.csv"
CHECKIN_CSV = "siri_solvers_checkins.csv"
STUDENT_CODES_CSV = "siri_solvers_student_codes.csv"

# Function to initialize CSVs with headers if they are empty
def initialize_csv(file_path, columns):
    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
        df = pd.DataFrame(columns=columns)
        df.to_csv(file_path, index=False)

# Initialize CSVs
initialize_csv(RESPONSES_CSV, ["student_code", "name", "activities", "ratings", "favorite_moment",
                               "career_connection", "learning_takeaway", "skills", "xp_points", "badges"])
initialize_csv(CHECKIN_CSV, ["student_code", "name", "arrival_time"])
initialize_csv(STUDENT_CODES_CSV, ["student_code", "name"])

# Sidebar Role Selection
st.sidebar.subheader("🔑 Select Your Role")
role = st.sidebar.selectbox("Who are you?", ["Siri Solver", "CSE", "Admin", "Parent"])

if role == "Siri Solver":
    st.sidebar.subheader("👦 Enter Your Name to Start")
    student_name = st.sidebar.text_input("Enter your name")

    if student_name:
        # Generate unique code if the student is new
        student_codes_df = pd.read_csv(STUDENT_CODES_CSV)
        
        if student_name in student_codes_df["name"].values:
            student_code = student_codes_df[student_codes_df["name"] == student_name]["student_code"].values[0]
        else:
            student_code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
            new_student = pd.DataFrame({"student_code": [student_code], "name": [student_name]})
            new_student.to_csv(STUDENT_CODES_CSV, mode="a", index=False, header=False)

        st.session_state["student_code"] = student_code
        st.success(f"Welcome, {student_name}! Your access code: **{student_code}** (Share with a parent if needed)")

elif role == "Parent":
    st.sidebar.subheader("👨‍👩‍👧 Enter Student's Code")
    parent_code = st.sidebar.text_input("Enter the student’s code")

    if st.sidebar.button("View Student Report"):
        responses_df = pd.read_csv(RESPONSES_CSV)
        student_responses = responses_df[responses_df["student_code"] == parent_code]

        if not student_responses.empty:
            st.subheader("📖 Student's Field Trip Report")
            st.dataframe(student_responses.drop(columns=["student_code"]))
        else:
            st.error("No report found for this student code.")

elif role in ["CSE", "Admin"]:
    if st.sidebar.button("View All Student Reports"):
        responses_df = pd.read_csv(RESPONSES_CSV)
        if not responses_df.empty:
            st.subheader("📊 All Student Reports")
            st.dataframe(responses_df.drop(columns=["student_code"]))
        else:
            st.warning("No data available yet.")

# Why Apollo Science Park for Uwazi Unit 2
st.subheader("🔬 Why Apollo Science Park for Uwazi Unit 2?")
st.write(
    "**Unit 2 of Uwazi focuses on Exploring the Scientific World**. "
    "Apollo Science Park allows Siri Solvers to engage with **real-world problem-solving** "
    "through **STEM activities, robotics, AI, astronomy, and hands-on science experiments**! "
    "This connects to the **Siri MaP** by helping students discover their strengths in logic, reasoning, and innovation."
)

# If logged in as Student, continue with trip activities
if "student_code" in st.session_state:
    student_code = st.session_state["student_code"]
    student_name = student_codes_df[student_codes_df["student_code"] == student_code]["name"].values[0]

    # Arrival Check-In
    st.subheader("🏁 Arrival Check-In & Photo Upload")
    arrival_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    uploaded_photo = st.file_uploader("📸 Upload your arrival photo", type=["jpg", "png", "jpeg"])

    if uploaded_photo:
        file_path = os.path.join("apollo_photos", f"{student_code}_{uploaded_photo.name}")
        with open(file_path, "wb") as f:
            f.write(uploaded_photo.getbuffer())

        checkin_data = pd.DataFrame({"student_code": [student_code], "name": [student_name], "arrival_time": [arrival_time]})
        checkin_data.to_csv(CHECKIN_CSV, mode="a", index=False, header=False)
        st.success("✅ Arrival Check-In Recorded!")

    # Activity Feedback
    st.subheader("🎭 Choose Your Adventure")
    activities = [
        "Robotics Lab", "Astronomy Observation", "Biology and Ecology Center",
        "Physics Experiments", "AI & Coding Workshop", "Chemistry Lab", "Engineering Zone"
    ]
    selected_activities = st.multiselect("Select all activities:", activities)
    activity_ratings = {activity: st.slider(f"Rate {activity} (1-5)", 1, 5, 3) for activity in selected_activities}

    # Reflection Questions
    st.subheader("📝 Post-Trip Reflection")
    favorite_moment = st.text_area("What was your **best moment** at Apollo Science Park?")
    career_connection = st.text_area("How did today's experience **inspire your future career**?")
    learning_takeaway = st.text_area("What is **one big thing** you learned today?")

    # XP & Badge System
    xp_points = len(selected_activities) * 10 + len(selected_skills) * 5
    badges = []
    if len(selected_activities) >= 3:
        badges.append("🎖 Curious Explorer")
    if "Scientific Inquiry" in selected_skills:
        badges.append("🔬 Future Scientist")
    if "Innovation" in selected_skills and "AI & Coding Workshop" in selected_activities:
        badges.append("💡 Master Innovator")

    # Submit feedback
    if st.button("🚀 Submit Experience!"):
        response_data = pd.DataFrame(
            {"student_code": [student_code], "name": [student_name], "activities": [", ".join(selected_activities)],
             "ratings": [str(activity_ratings)], "favorite_moment": [favorite_moment],
             "career_connection": [career_connection], "learning_takeaway": [learning_takeaway],
             "skills": [", ".join(selected_skills)], "xp_points": [xp_points], "badges": [", ".join(badges)]})
        response_data.to_csv(RESPONSES_CSV, mode="a", index=False, header=False)
        st.success("🎉 Your trip experience has been saved!")

# Group Album
st.subheader("📸 Apollo Science Park Group Album")
image_files = os.listdir("apollo_photos")
if image_files:
    for img in image_files:
        st.image(os.path.join("apollo_photos", img), caption=img, use_column_width=True)
else:
    st.warning("No photos uploaded yet.")
