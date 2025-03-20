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
SIRI_SOLVER_CODES_CSV = "siri_solvers_codes.csv"

# Function to initialize CSVs with headers if they are empty
def initialize_csv(file_path, columns):
    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
        df = pd.DataFrame(columns=columns)
        df.to_csv(file_path, index=False)

# Initialize CSVs
initialize_csv(RESPONSES_CSV, ["siri_solver_code", "name", "activities", "ratings", "favorite_moment",
                               "career_connection", "learning_takeaway", "xp_points", "badges", "photos"])
initialize_csv(CHECKIN_CSV, ["siri_solver_code", "name", "arrival_time"])
initialize_csv(SIRI_SOLVER_CODES_CSV, ["siri_solver_code", "name"])

# Sidebar Role Selection
st.sidebar.subheader("🔑 Select Your Role")
role = st.sidebar.selectbox("Who are you?", ["Siri Solver", "CSE", "Admin", "Parent"])

if role == "Siri Solver":
    st.sidebar.subheader("🧠 Enter Your Name to Start")
    siri_solver_name = st.sidebar.text_input("Enter your name")

    if siri_solver_name:
        # Generate unique code if new Siri Solver
        siri_solver_codes_df = pd.read_csv(SIRI_SOLVER_CODES_CSV)
        
        if siri_solver_name in siri_solver_codes_df["name"].values:
            siri_solver_code = siri_solver_codes_df[siri_solver_codes_df["name"] == siri_solver_name]["siri_solver_code"].values[0]
        else:
            siri_solver_code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
            new_siri_solver = pd.DataFrame({"siri_solver_code": [siri_solver_code], "name": [siri_solver_name]})
            new_siri_solver.to_csv(SIRI_SOLVER_CODES_CSV, mode="a", index=False, header=False)

        st.session_state["siri_solver_code"] = siri_solver_code
        st.success(f"Welcome, {siri_solver_name}! Your access code: **{siri_solver_code}** (Share with a parent if needed)")

elif role == "Parent":
    st.sidebar.subheader("👨‍👩‍👧 Enter Siri Solver's Code")
    parent_code = st.sidebar.text_input("Enter the Siri Solver’s code")

    if st.sidebar.button("View Siri Solver Report"):
        responses_df = pd.read_csv(RESPONSES_CSV)
        siri_solver_responses = responses_df[responses_df["siri_solver_code"] == parent_code]

        if not siri_solver_responses.empty:
            st.subheader("📖 Siri Solver's Field Trip Report")
            st.dataframe(siri_solver_responses.drop(columns=["siri_solver_code"]))
        else:
            st.error("No report found for this Siri Solver code.")

elif role in ["CSE", "Admin"]:
    if st.sidebar.button("View All Reports"):
        responses_df = pd.read_csv(RESPONSES_CSV)
        if not responses_df.empty:
            st.subheader("📊 All Siri Solver Reports")
            st.dataframe(responses_df.drop(columns=["siri_solver_code"]))
        else:
            st.warning("No data available yet.")

# Why Apollo Science Park for Uwazi Unit 2
st.subheader("🔬 Why Apollo Science Park for Uwazi Unit 2?")
st.write(
    "**Unit 2 of Uwazi focuses on Exploring the Scientific World**. "
    "Apollo Science Park allows Siri Solvers to engage with **real-world problem-solving** "
    "through **STEM activities, robotics, AI, astronomy, and hands-on science experiments**! "
    "This connects to the **Siri MaP** by helping Siri Solvers discover their strengths in logic, reasoning, and innovation."
)

# If logged in as Siri Solver, continue with trip activities
if "siri_solver_code" in st.session_state:
    siri_solver_code = st.session_state["siri_solver_code"]
    siri_solver_name = siri_solver_codes_df[siri_solver_codes_df["siri_solver_code"] == siri_solver_code]["name"].values[0]

    # Arrival Check-In
    st.subheader("🏁 Arrival Check-In & Photo Upload")
    arrival_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    uploaded_photo = st.file_uploader("📸 Upload your arrival photo", type=["jpg", "png", "jpeg"])

    if uploaded_photo:
        file_path = os.path.join("apollo_photos", f"{siri_solver_code}_{uploaded_photo.name}")
        with open(file_path, "wb") as f:
            f.write(uploaded_photo.getbuffer())

        checkin_data = pd.DataFrame({"siri_solver_code": [siri_solver_code], "name": [siri_solver_name], "arrival_time": [arrival_time]})
        checkin_data.to_csv(CHECKIN_CSV, mode="a", index=False, header=False)
        st.success("✅ Arrival Check-In Recorded!")

    # Activity Feedback
    st.subheader("🎭 Choose Your Adventure")
    activities = [
        "Robotics Lab", "Astronomy Observation", "Biology and Ecology Center",
        "Physics Experiments", "AI & Coding Workshop", "Chemistry Lab", "Engineering Zone"
    ]
    selected_activities = st.multiselect("Select all activities:", activities)
    
    # Photo Uploads for Each Activity
    activity_photos = {}
    for activity in selected_activities:
        activity_photos[activity] = st.file_uploader(f"📸 Upload your photo from {activity}", type=["jpg", "png", "jpeg"], key=activity)

    # Reflection Questions
    st.subheader("📝 Post-Trip Reflection")
    favorite_moment = st.text_area("What was your **best moment** at Apollo Science Park?")
    career_connection = st.text_area("How did today's experience **inspire your future career**?")
    learning_takeaway = st.text_area("What is **one big thing** you learned today?")

    # XP & Badge System
    xp_points = len(selected_activities) * 10
    badges = []
    if len(selected_activities) >= 3:
        badges.append("🎖 Curious Explorer")
    if "Physics Experiments" in selected_activities:
        badges.append("🔬 Future Scientist")
    if "AI & Coding Workshop" in selected_activities:
        badges.append("💡 Master Innovator")

    # Submit feedback
    if st.button("🚀 Submit Experience!"):
        response_data = pd.DataFrame(
            {"siri_solver_code": [siri_solver_code], "name": [siri_solver_name], "activities": [", ".join(selected_activities)],
             "favorite_moment": [favorite_moment], "career_connection": [career_connection], "learning_takeaway": [learning_takeaway],
             "xp_points": [xp_points], "badges": [", ".join(badges)]})
        response_data.to_csv(RESPONSES_CSV, mode="a", index=False, header=False)
        st.success("🎉 Your trip experience has been saved!")

# 🏆 Leaderboard
st.subheader("🏆 Umeme Points Leaderboard ⚡")
checkin_df = pd.read_csv(CHECKIN_CSV)
checkin_df = checkin_df.sort_values(by="arrival_time", ascending=True)
st.dataframe(checkin_df)

# 📸 Group Album
st.subheader("📸 Apollo Science Park Group Album")
for img in os.listdir("apollo_photos"):
    st.image(os.path.join("apollo_photos", img), caption=img, use_column_width=True)
