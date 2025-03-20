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

# Ensure all CSVs exist with the correct structure
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
        siri_solver_codes_df = pd.read_csv(SIRI_SOLVER_CODES_CSV)

        if not siri_solver_codes_df.empty and siri_solver_name in siri_solver_codes_df["name"].values:
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
        if not responses_df.empty and parent_code in responses_df["siri_solver_code"].values:
            st.subheader("📖 Siri Solver's Field Trip Report")
            siri_solver_responses = responses_df[responses_df["siri_solver_code"] == parent_code]
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

# 🔬 Why Apollo Science Park for Uwazi Unit 2?
st.subheader("🔬 Why Apollo Science Park for Uwazi Unit 2?")
st.write(
    "**Unit 2 of Uwazi focuses on Exploring the Scientific World**. "
    "Apollo Science Park allows Siri Solvers to engage with **real-world problem-solving** "
    "through **STEM activities, robotics, AI, astronomy, and hands-on science experiments**! "
    "This connects to the **Siri MaP** by helping Siri Solvers discover their strengths in logic, reasoning, and innovation."
)

# 🎮 Gamification Instructions
st.subheader("🎮 How to Earn Points & Rewards")
st.write("""
- **🏆 Umeme Points** → First to arrive earns the most points!  
- **📸 Activity Photos** → Upload photos of your favorite activities.  
- **🎭 Activity Ratings** → Give feedback on what you enjoyed the most.  
- **📝 Reflections** → Share your best moments, learning takeaways, and how it connects to your future!  
- **🎖 XP & Badges** → Earn **Explorer, Scientist, and Innovator** badges based on engagement!  
""")

# 🏁 Arrival Check-In
st.subheader("🏁 Arrival Check-In & Photo Upload")
if "siri_solver_code" in st.session_state:
    siri_solver_code = st.session_state["siri_solver_code"]
    arrival_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    uploaded_photo = st.file_uploader("📸 Upload your arrival photo", type=["jpg", "png", "jpeg"])

    if uploaded_photo:
        file_path = os.path.join("apollo_photos", f"{siri_solver_code}_{uploaded_photo.name}")
        with open(file_path, "wb") as f:
            f.write(uploaded_photo.getbuffer())

        checkin_df = pd.read_csv(CHECKIN_CSV)
        new_entry = pd.DataFrame({"siri_solver_code": [siri_solver_code], "name": [st.session_state["siri_solver_code"]], "arrival_time": [arrival_time]})
        checkin_df = pd.concat([checkin_df, new_entry], ignore_index=True)
        checkin_df.to_csv(CHECKIN_CSV, index=False)

        st.success("✅ Arrival Check-In Recorded!")

# 🏆 Leaderboard (Umeme Points)
st.subheader("🏆 Umeme Points Leaderboard ⚡")
checkin_df = pd.read_csv(CHECKIN_CSV)
if "arrival_time" in checkin_df.columns and not checkin_df.empty:
    checkin_df["arrival_time"] = pd.to_datetime(checkin_df["arrival_time"])  # Ensure datetime format
    checkin_df = checkin_df.sort_values(by="arrival_time", ascending=True)
    st.dataframe(checkin_df)
else:
    st.warning("No check-ins yet. Be the first to check in!")

# 🎭 Activity Selection & Ratings
st.subheader("🎭 Choose Your Adventure")
activities = [
    "Robotics Lab", "Astronomy Observation", "Biology and Ecology Center",
    "Physics Experiments", "AI & Coding Workshop", "Chemistry Lab", "Engineering Zone"
]
selected_activities = st.multiselect("Select all activities:", activities)

# Activity Ratings & Photos
activity_photos = {}
activity_ratings = {}
for activity in selected_activities:
    activity_photos[activity] = st.file_uploader(f"📸 Upload your photo from {activity}", type=["jpg", "png", "jpeg"], key=activity)
    activity_ratings[activity] = st.slider(f"Rate {activity} (1-5)", 1, 5, 3, key=f"rating_{activity}")

# 📝 Reflection Questions
st.subheader("📝 Post-Trip Reflection")
favorite_moment = st.text_area("What was your **best moment** at Apollo Science Park?")
career_connection = st.text_area("How did today's experience **inspire your future career**?")
learning_takeaway = st.text_area("What is **one big thing** you learned today?")

# 📸 Group Album
st.subheader("📸 Apollo Science Park Group Album")
image_files = os.listdir("apollo_photos")
if image_files:
    for img in image_files:
        st.image(os.path.join("apollo_photos", img), caption=img, use_column_width=True)
else:
    st.warning("No photos uploaded yet.")
