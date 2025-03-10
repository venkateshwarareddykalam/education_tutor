import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import json
import os

def save_calendar_data(calendar_data):
    """Save calendar data to a JSON file"""
    with open("calendar_data.json", "w") as f:
        json.dump(calendar_data, f)

def load_calendar_data():
    """Load calendar data from a JSON file"""
    if os.path.exists("calendar_data.json"):
        with open("calendar_data.json", "r") as f:
            return json.load(f)
    else:
        # Return empty calendar structure
        return {
            "events": []
        }

def generate_learning_schedule(topic, subject, days=7, start_date=None):
    """Generate a learning schedule for a topic"""
    if start_date is None:
        start_date = datetime.now().date()
    else:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    
    # Get existing calendar data
    calendar_data = load_calendar_data()
    
    # Get current user
    user_id = st.session_state.get("user_id", "default_user")
    
    # Generate subtopics and learning activities (in a real app, this would use AI)
    schedule = []
    
    for i in range(days):
        current_date = start_date + timedelta(days=i)
        date_str = current_date.strftime("%Y-%m-%d")
        
        # Create a learning event for this day
        event = {
            "date": date_str,
            "user_id": user_id,
            "topic": topic,
            "subject": subject,
            "subtopic": f"Part {i+1} of {topic}",
            "description": f"Study session for {topic} - Day {i+1}",
            "duration": 60,  # minutes
            "completed": False,
            "points": 10,
            "difficulty": "Medium"
        }
        
        # Add to schedule
        schedule.append(event)
        calendar_data["events"].append(event)
    
    # Save updated calendar
    save_calendar_data(calendar_data)
    
    return schedule

def render_calendar_page():
    """Render the calendar page in the app"""
    st.title("Learning Calendar")
    
    # Tab for viewing calendar and creating new schedule
    tab1, tab2 = st.tabs(["View Calendar", "Create Learning Schedule"])
    
    with tab1:
        # Calendar view
        calendar_data = load_calendar_data()
        
        if not calendar_data["events"]:
            st.info("No learning events scheduled yet. Create a new learning schedule to get started!")
        else:
            # Get user's events
            user_id = st.session_state.get("user_id", "default_user")
            user_events = [event for event in calendar_data["events"] if event["user_id"] == user_id]
            
            # Group by date
            events_by_date = {}
            for event in user_events:
                date = event["date"]
                if date not in events_by_date:
                    events_by_date[date] = []
                events_by_date[date].append(event)
            
            # Display calendar
            st.subheader("Your Learning Schedule")
            
            # Date range selector
            today = datetime.now().date()
            start_date = st.date_input("From date", today)
            end_date = st.date_input("To date", today + timedelta(days=14))
            
            # Create a date range
            date_range = []
            current_date = start_date
            while current_date <= end_date:
                date_range.append(current_date)
                current_date += timedelta(days=1)
            
            # Display events for each date
            for date in date_range:
                date_str = date.strftime("%Y-%m-%d")
                date_display = date.strftime("%A, %B %d, %Y")
                
                if date_str in events_by_date:
                    with st.expander(f"📅 {date_display} ({len(events_by_date[date_str])} events)"):
                        for idx, event in enumerate(events_by_date[date_str]):
                            cols = st.columns([3, 1, 1])
                            with cols[0]:
                                st.markdown(f"**{event['topic']}**: {event['subtopic']}")
                                st.markdown(f"_{event['description']}_")
                            with cols[1]:
                                st.markdown(f"**Subject:** {event['subject']}")
                                st.markdown(f"**Duration:** {event['duration']} min")
                            with cols[2]:
                                if st.checkbox("Mark Complete", value=event["completed"], key=f"complete_{date_str}_{idx}"):
                                    # Update completion status
                                    event_idx = calendar_data["events"].index(event)
                                    calendar_data["events"][event_idx]["completed"] = True
                                    
                                    # Award points if newly completed
                                    if not event["completed"]:
                                        st.session_state.points = st.session_state.get("points", 0) + event["points"]
                                        st.success(f"🎉 You earned {event['points']} points!")
                                    
                                    # Save updated calendar
                                    save_calendar_data(calendar_data)
                                
                                st.markdown(f"**Points:** {event['points']}")
                            st.markdown("---")
                else:
                    st.markdown(f"📅 {date_display} - No events scheduled")
    
    with tab2:
        # Create new learning schedule
        st.subheader("Create a New Learning Schedule")
        
        topic = st.text_input("Topic you want to learn")
        subject = st.selectbox("Subject Area", [
            "Mathematics", "Science", "History", "Language Arts", 
            "Computer Science", "Geography", "Economics", "Physics", 
            "Chemistry", "Biology", "Literature", "Philosophy"
        ])
        days = st.slider("Number of days", 1, 30, 7)
        start_date = st.date_input("Start date", datetime.now().date())
        
        if st.button("Generate Learning Schedule"):
            if topic and subject:
                schedule = generate_learning_schedule(
                    topic, 
                    subject, 
                    days=days, 
                    start_date=start_date.strftime("%Y-%m-%d")
                )
                
                # Show the generated schedule
                st.success(f"Created a {days}-day learning schedule for {topic}!")
                
                # Preview the schedule
                schedule_df = pd.DataFrame(schedule)
                schedule_df = schedule_df[["date", "subtopic", "description", "duration", "points"]]
                st.dataframe(schedule_df)
            else:
                st.warning("Please enter a topic and subject to generate a schedule.")

# Define gamification constants
LEVELS = {
    1: {"points": 0, "title": "Beginner Learner"},
    2: {"points": 100, "title": "Eager Student"},
    3: {"points": 250, "title": "Knowledge Seeker"},
    4: {"points": 500, "title": "Academic Explorer"},
    5: {"points": 1000, "title": "Scholar"},
    6: {"points": 2000, "title": "Master Scholar"},
    7: {"points": 3500, "title": "Intellectual"},
    8: {"points": 5000, "title": "Knowledge Master"},
    9: {"points": 7500, "title": "Wisdom Keeper"},
    10: {"points": 10000, "title": "Education Virtuoso"}
}

ACHIEVEMENTS = [
    {"id": "first_question", "name": "First Question", "description": "Asked your first question", "points": 10, "icon": "🎯"},
    {"id": "streak_3", "name": "Three-Day Streak", "description": "Used the app for 3 consecutive days", "points": 30, "icon": "🔥"},
    {"id": "streak_7", "name": "Weekly Scholar", "description": "Used the app for 7 consecutive days", "points": 100, "icon": "🔥"},
    {"id": "first_schedule", "name": "Planner", "description": "Created your first learning schedule", "points": 25, "icon": "📅"},
    {"id": "complete_schedule", "name": "Follow Through", "description": "Completed all events in a learning schedule", "points": 150, "icon": "✅"},
    {"id": "subject_master", "name": "Subject Enthusiast", "description": "Asked 10 questions in the same subject", "points": 50, "icon": "📚"},
    {"id": "night_owl", "name": "Night Owl", "description": "Studied late at night (after 10 PM)", "points": 15, "icon": "🦉"},
    {"id": "early_bird", "name": "Early Bird", "description": "Studied early in the morning (before 8 AM)", "points": 15, "icon": "🐦"},
    {"id": "weekend_warrior", "name": "Weekend Warrior", "description": "Studied on both Saturday and Sunday in the same weekend", "points": 40, "icon": "⚔️"}
]

def save_user_data(user_data):
    """Save user gamification data to a JSON file"""
    with open("user_gamification_data.json", "w") as f:
        json.dump(user_data, f)

def load_user_data():
    """Load user gamification data from a JSON file"""
    if os.path.exists("user_gamification_data.json"):
        with open("user_gamification_data.json", "r") as f:
            return json.load(f)
    else:
        # Return default user data structure
        return {
            "users": {}
        }

def get_user_data(user_id="default_user"):
    """Get gamification data for a specific user"""
    data = load_user_data()
    
    if user_id not in data["users"]:
        # Initialize new user
        data["users"][user_id] = {
            "points": 0,
            "level": 1,
            "achievements": [],
            "streak": {
                "current": 0,
                "longest": 0,
                "last_active": None
            },
            "subjects": {},
            "questions_asked": 0,
            "schedules_created": 0,
            "schedules_completed": 0,
            "last_updated": datetime.now().strftime("%Y-%m-%d")
        }
        save_user_data(data)
    
    return data["users"][user_id]

def update_streak():
    """Update user streak based on activity today"""
    user_id = st.session_state.get("user_id", "default_user")
    user_data = get_user_data(user_id)
    
    today = datetime.now().date()
    last_active_str = user_data["streak"]["last_active"]
    
    if last_active_str:
        last_active = datetime.strptime(last_active_str, "%Y-%m-%d").date()
        days_diff = (today - last_active).days
        
        if days_diff == 1:
            # Consecutive day
            user_data["streak"]["current"] += 1
            user_data["streak"]["longest"] = max(user_data["streak"]["current"], user_data["streak"]["longest"])
            
            # Check for streak achievements
            if user_data["streak"]["current"] == 3:
                award_achievement(user_id, "streak_3")
            if user_data["streak"]["current"] == 7:
                award_achievement(user_id, "streak_7")
                
        elif days_diff > 1:
            # Streak broken
            user_data["streak"]["current"] = 1
        # If days_diff == 0, it's the same day, don't change streak
    else:
        # First day using the app
        user_data["streak"]["current"] = 1
    
    user_data["streak"]["last_active"] = today.strftime("%Y-%m-%d")
    
    # Update data
    data = load_user_data()
    data["users"][user_id] = user_data
    save_user_data(data)
    
    return user_data["streak"]["current"]

def award_points(user_id, points, reason=""):
    """Award points to a user and check for level-ups"""
    user_data = get_user_data(user_id)
    
    # Add points
    old_points = user_data["points"]
    user_data["points"] += points
    
    # Check for level-up
    old_level = user_data["level"]
    for level in sorted(LEVELS.keys(), reverse=True):
        if user_data["points"] >= LEVELS[level]["points"]:
            user_data["level"] = level
            break
    
    # Update user data
    data = load_user_data()
    data["users"][user_id] = user_data
    save_user_data(data)
    
    level_up = old_level < user_data["level"]
    
    return {
        "points_added": points,
        "new_total": user_data["points"],
        "level_up": level_up,
        "new_level": user_data["level"],
        "level_title": LEVELS[user_data["level"]]["title"]
    }

def award_achievement(user_id, achievement_id):
    """Award an achievement to a user"""
    user_data = get_user_data(user_id)
    
    # Check if already awarded
    if achievement_id in user_data["achievements"]:
        return None
    
    # Find achievement
    achievement = next((a for a in ACHIEVEMENTS if a["id"] == achievement_id), None)
    if not achievement:
        return None
    
    # Award achievement
    user_data["achievements"].append(achievement_id)
    
    # Update user data
    data = load_user_data()
    data["users"][user_id] = user_data
    save_user_data(data)
    
    # Award points for achievement
    result = award_points(user_id, achievement["points"], f"Achievement: {achievement['name']}")
    
    # Return achievement details
    return {
        "achievement": achievement,
        "points_result": result
    }

def track_question_asked(user_id, subject):
    """Track when a user asks a question"""
    user_data = get_user_data(user_id)
    
    # First question achievement
    if user_data["questions_asked"] == 0:
        award_achievement(user_id, "first_question")
    
    # Track subject-specific questions
    if subject not in user_data["subjects"]:
        user_data["subjects"][subject] = 0
    user_data["subjects"][subject] += 1
    
    # Subject master achievement
    if user_data["subjects"][subject] == 10:
        award_achievement(user_id, "subject_master")
    
    # Increment question count
    user_data["questions_asked"] += 1
    
    # Night owl / early bird achievements
    current_hour = datetime.now().hour
    if current_hour >= 22 or current_hour < 3:
        award_achievement(user_id, "night_owl")
    elif current_hour >= 5 and current_hour < 8:
        award_achievement(user_id, "early_bird")
    
    # Weekend warrior tracking
    today = datetime.now().strftime("%A")
    if today in ["Saturday", "Sunday"]:
        user_data["weekend_days"] = user_data.get("weekend_days", [])
        if today not in user_data["weekend_days"]:
            user_data["weekend_days"].append(today)
        
        if len(set(user_data["weekend_days"])) >= 2:
            award_achievement(user_id, "weekend_warrior")
            # Reset weekend tracking
            user_data["weekend_days"] = []
    
    # Update user data
    data = load_user_data()
    data["users"][user_id] = user_data
    save_user_data(data)
    
    # Award points for asking a question
    return award_points(user_id, 5, "Asked a question")

def render_gamification_dashboard():
    """Render the gamification dashboard in the app"""
    st.title("Learning Progress")
    
    # Get user data
    user_id = st.session_state.get("user_id", "default_user")
    user_data = get_user_data(user_id)
    
    # Display level and points in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Level", f"{user_data['level']} - {LEVELS[user_data['level']]['title']}")
    
    with col2:
        # Calculate points to next level
        current_level = user_data["level"]
        points_needed = 0
        if current_level < max(LEVELS.keys()):
            next_level = current_level + 1
            points_needed = LEVELS[next_level]["points"] - user_data["points"]
        
        st.metric("Points", user_data["points"], 
                 delta=f"{points_needed} to level {current_level + 1}" if points_needed > 0 else "Max level!")
    
    with col3:
        st.metric("Streak", f"{user_data['streak']['current']} days", 
                 delta=f"Longest: {user_data['streak']['longest']}")
    
    # Progress to next level
    if current_level < max(LEVELS.keys()):
        next_level_points = LEVELS[current_level + 1]["points"]
        current_level_points = LEVELS[current_level]["points"]
        progress = (user_data["points"] - current_level_points) / (next_level_points - current_level_points)
        
        st.progress(progress)
        st.caption(f"{user_data['points']} / {next_level_points} points to Level {current_level + 1}")
    
    # Stats and achievements tabs
    tab1, tab2 = st.tabs(["Learning Stats", "Achievements"])
    
    with tab1:
        # Learning statistics
        st.subheader("Your Learning Journey")
        
        # Display stats
        stats_col1, stats_col2 = st.columns(2)
        
        with stats_col1:
            st.metric("Questions Asked", user_data["questions_asked"])
            st.metric("Schedules Created", user_data.get("schedules_created", 0))
        
        with stats_col2:
            st.metric("Schedules Completed", user_data.get("schedules_completed", 0))
            
            # Calculate completion rate
            completion_rate = 0
            if user_data.get("schedules_created", 0) > 0:
                completion_rate = (user_data.get("schedules_completed", 0) / user_data.get("schedules_created", 0)) * 100
            st.metric("Completion Rate", f"{completion_rate:.1f}%")
        
        # Subject breakdown
        if user_data["subjects"]:
            st.subheader("Subjects Explored")
            
            import pandas as pd
            import matplotlib.pyplot as plt
            
            # Create DataFrame from subjects
            subjects_df = pd.DataFrame({
                "Subject": list(user_data["subjects"].keys()),
                "Questions": list(user_data["subjects"].values())
            })
            
            subjects_df = subjects_df.sort_values("Questions", ascending=False)
            
            # Display table
            st.dataframe(subjects_df)
            
            # Display chart
            fig, ax = plt.subplots()
            bars = ax.bar(subjects_df["Subject"], subjects_df["Questions"])
            ax.set_ylabel("Questions Asked")
            ax.set_title("Questions per Subject")
            plt.xticks(rotation=45, ha="right")
            st.pyplot(fig)
    
    with tab2:
        # Achievements section
        st.subheader("Your Achievements")
        
        # Organize achievements: earned vs. available
        earned_achievements = [a for a in ACHIEVEMENTS if a["id"] in user_data["achievements"]]
        available_achievements = [a for a in ACHIEVEMENTS if a["id"] not in user_data["achievements"]]
        
        # Display earned achievements
        if earned_achievements:
            st.write("Completed:")
            for achievement in earned_achievements:
                with st.container():
                    cols = st.columns([1, 6, 2])
                    with cols[0]:
                        st.markdown(f"<h3 style='text-align: center;'>{achievement['icon']}</h3>", unsafe_allow_html=True)
                    with cols[1]:
                        st.markdown(f"**{achievement['name']}**")
                        st.caption(achievement['description'])
                    with cols[2]:
                        st.markdown(f"<div style='background-color: #4CAF50; color: white; padding: 5px 10px; border-radius: 10px; text-align: center;'>+{achievement['points']} pts</div>", unsafe_allow_html=True)
        else:
            st.info("You haven't earned any achievements yet. Keep learning to unlock them!")
        
        # Display available achievements
        if available_achievements:
            st.write("Available:")
            for achievement in available_achievements:
                with st.container():
                    cols = st.columns([1, 6, 2])
                    with cols[0]:
                        st.markdown(f"<h3 style='text-align: center; opacity: 0.5;'>{achievement['icon']}</h3>", unsafe_allow_html=True)
                    with cols[1]:
                        st.markdown(f"**{achievement['name']}**")
                        st.caption(achievement['description'])
                    with cols[2]:
                        st.markdown(f"<div style='background-color: #888; color: white; padding: 5px 10px; border-radius: 10px; text-align: center;'>+{achievement['points']} pts</div>", unsafe_allow_html=True)