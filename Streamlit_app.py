import streamlit as st

import pandas as pd

import random



# Title

st.title("🎮 Siri Solvers: Apollo Science Park Adventure")



# Introduction

st.write(

    "🌟 Welcome to the **Siri Solvers Gamified Field Trip Experience!** "

    "Earn **XP points**, unlock **badges**, and track your **learning journey** as you explore science and technology! 🚀"

)



# List of activities at Apollo Science Park (customizable)

activities = [

    "Robotics Lab",

    "Astronomy Observation",

    "Biology and Ecology Center",

    "Physics Experiments",

    "AI & Coding Workshop",

    "Chemistry Lab",

    "Engineering and Innovation Zone"

]



# Data collection

st.subheader("🎭 Choose Your Adventure: What Activities Did You Enjoy?")

selected_activities = st.multiselect(

    "Select all activities that you found exciting:", activities

)



activity_ratings = {}

for activity in selected_activities:

    activity_ratings[activity] = st.slider(

        f"Rate your experience in {activity} (1 = Not Exciting, 5 = Super Fun!)", 1, 5, 3

    )



# Feedback on experiences

st.subheader("📝 Describe Your Most Exciting Moment!")

favorite_moment = st.text_area("What was the **best part** of your adventure at Apollo Science Park?")



# Map strengths to Siri MaP

st.subheader("🔬 What Skills Did You Improve? (Siri MaP)")

skills = [

    "Problem Solving",

    "Critical Thinking",

    "Creativity",

    "Teamwork",

    "Communication",

    "Logical Reasoning",

    "Innovation",

    "Scientific Inquiry"

]

selected_skills = st.multiselect("Select all skills you feel you used today:", skills)



# Gamification: XP Points Calculation

xp_points = len(selected_activities) * 10 + len(selected_skills) * 5



# Badge System

badges = []

if len(selected_activities) >= 3:

    badges.append("🎖 Curious Explorer")  # Rated at least 3 activities

if "Scientific Inquiry" in selected_skills:

    badges.append("🔬 Future Scientist")  # Selected Scientific Inquiry as a skill

if "Innovation" in selected_skills and "AI & Coding Workshop" in selected_activities:

    badges.append("💡 Master Innovator")  # Enjoyed AI & Coding Workshop and Innovation

if len(selected_activities) == len(activities):

    badges.append("🌍 Science Park Champion")  # Explored everything



# Bonus Challenge: Spin-the-Wheel

bonus_challenges = [

    "Find one real-world application of a science experiment you saw today and write about it!",

    "Teach a friend or family member something cool you learned today!",

    "Draw or sketch an invention inspired by today’s visit!",

    "Write a short sci-fi story about a future where one of today's technologies changes the world!",

    "Design a poster that encourages more students to explore STEM fields!"

]

bonus_challenge = random.choice(bonus_challenges)



# Submit feedback

if st.button("🚀 Submit My Adventure!"):

    # Save feedback

    feedback_data = pd.DataFrame(

        {

            "Activities Enjoyed": [", ".join(selected_activities)],

            "Ratings": [activity_ratings],

            "Favorite Moment": [favorite_moment],

            "Skills Improved": [", ".join(selected_skills)],

            "XP Earned": [xp_points],

            "Badges": [", ".join(badges)],

        }

    )



    # Save to CSV (or database in production)

    feedback_data.to_csv("siri_solvers_feedback.csv", mode="a", index=False, header=False)



    st.success("🎉 Adventure Logged! You've earned XP and badges!")



    # Show XP, badges, and bonus challenge

    st.subheader("🎮 Your Adventure Stats")

    st.write(f"⭐ **XP Points Earned:** {xp_points}")

    st.write("🏅 **Badges Unlocked:** " + (", ".join(badges) if badges else "No badges yet! Keep exploring!"))

    st.write(f"🎰 **Bonus Challenge:** {bonus_challenge}")



# Display past feedback (if any)

st.subheader("🏆 Leaderboard & Insights")

try:

    past_feedback = pd.read_csv("siri_solvers_feedback.csv")

    st.dataframe(past_feedback)

except FileNotFoundError:

    st.write("No feedback has been collected yet. Be the first to log your adventure!")



# Next Steps Section

st.subheader("🔭 What's Next?")

st.write(

    "Based on what you enjoyed and excelled at, check your **Siri MaP** for recommended clubs and learning paths! "

    "Keep exploring, keep solving, and keep growing! 🚀"

)
