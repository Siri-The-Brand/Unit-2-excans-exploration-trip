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
USER_CSV = "siri_solvers_users.csv"
RESPONSES_CSV = "siri_solvers_responses.csv"
CHECKIN_CSV = "siri_solvers_checkins.csv"

# Function to initialize CSVs with headers if they are empty
def initialize_csv(file_path, columns):
    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
        df = pd.DataFrame(columns=columns)
        df.to_csv(file_path, index=False)

# Initialize CSVs with proper headers
initialize_csv(USER_CSV, ["name", "role", "student_code"])
initialize_csv(RESPONSES_CSV, ["student_code", "activities", "ratings", "favorite_moment",
                               "career_connection", "learning_takeaway", "skills", "xp_points", "badges"])
initialize_csv(CHECKIN_CSV, ["student_code", "arrival_time"])

# User Login / Management
st.sidebar.subheader("🔑 Login / Register")

role = st.sidebar.selectbox("Select Your Role", ["Student", "CSE", "Admin", "Parent"])

if role == "Siri Solver":
    student_name = st.sidebar.text_input("Enter Your Name")
    if st.sidebar.button("Register / Login"):
        student_code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        users_df = pd.read_csv(USER_CSV)
        
        if student_name in users_df["name"].values:
            student_code = users_df[users_df["name"] == student_name]["student_code"].values[0]
        else:
            new_user = pd.DataFrame({"name": [student_name], "role": ["Student"], "student_code": [student_code]})
            new_user.to_csv(USER_CSV, mode="a", index=False, header=False)

        st.session_state["student_code"] = student_code
        st.success(f"Logged in as {student_name}. Parent Code: **{student_code}**")

elif role == "Parent":
    parent_code = st.sidebar.text_input("Enter Siri Solver's Code")
    if st.sidebar.button("View Siri Solvers Report"):
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

# If logged in as Student, proceed with trip activities
if "student_code" in st.session_state:
    student_code = st.session_state["student_code"]

    # Arrival Check-In
    st.subheader("🏁 Arrival Check-In & Photo Upload")
    arrival_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    uploaded_photo = st.file_uploader("📸 Upload your arrival photo", type=["jpg", "png", "jpeg"])

    if uploaded_photo:
        file_path = os.path.join("apollo_photos", f"{student_code}_{uploaded_photo.name}")
        with open(file_path, "wb") as f:
            f.write(uploaded_photo.getbuffer())

        checkin_data = pd.DataFrame({"student_code": [student_code], "arrival_time": [arrival_time]})
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

    # Skills Mapping (Siri MaP)
    st.subheader("🔬 What Skills Did You Improve?")
    skills = ["Problem Solving", "Critical Thinking", "Creativity", "Teamwork", "Communication", "Logical Reasoning",
              "Innovation", "Scientific Inquiry"]
    selected_skills = st.multiselect("Select all skills:", skills)

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
            {"student_code": [student_code], "activities": [", ".join(selected_activities)],
             "ratings": [str(activity_ratings)], "favorite_moment": [favorite_moment],
             "career_connection": [career_connection], "learning_takeaway": [learning_takeaway],
             "skills": [", ".join(selected_skills)], "xp_points": [xp_points], "badges": [", ".join(badges)]})
        response_data.to_csv(RESPONSES_CSV, mode="a", index=False, header=False)
        st.success("🎉 Your trip experience has been saved!")

    # Display Student Dashboard
    st.subheader("📊 Your Field Trip Report")
    responses_df = pd.read_csv(RESPONSES_CSV)
    student_responses = responses_df[responses_df["student_code"] == student_code]
    if not student_responses.empty:
        st.dataframe(student_responses.drop(columns=["student_code"]))
    else:
        st.warning("No records found yet.")

# Leaderboard
st.subheader("🏆 Umeme Points Leaderboard ⚡")
try:
    checkin_df = pd.read_csv(CHECKIN_CSV)
    checkin_df = checkin_df.sort_values(by="arrival_time", ascending=True)
    st.dataframe(checkin_df)
except pd.errors.EmptyDataError:
    st.write("No check-ins yet. Be the first to check in!")

# Group Album Section
st.subheader("📸 Apollo Science Park Group Album")
image_files = os.listdir("apollo_photos")
if image_files:
    for img in image_files:
        st.image(os.path.join("apollo_photos", img), caption=img, use_column_width=True)
else:
    st.warning("No photos uploaded yet.")
