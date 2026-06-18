"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
}

# Additional activities: sports, artistic, and intellectual
activities.update({
    "Soccer Club": {
        "description": "Team soccer practice and inter-school matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": []
    },
    "Swimming Team": {
        "description": "Swim training and competitions for all levels",
        "schedule": "Mondays and Wednesdays, 5:00 PM - 6:30 PM",
        "max_participants": 16,
        "participants": []
    },
    "Drama Club": {
        "description": "Acting workshops and school play production",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 25,
        "participants": []
    },
    "Art Workshop": {
        "description": "Painting, drawing, and mixed media sessions",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": []
    },
    "Robotics Club": {
        "description": "Build and program robots; participate in competitions",
        "schedule": "Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 12,
        "participants": []
    },
    "Debate Team": {
        "description": "Practice public speaking and competitive debating",
        "schedule": "Mondays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": []
    }
})


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Prevent duplicate signups
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")

    # Prevent exceeding max participants
    if len(activity["participants"]) >= activity.get("max_participants", float("inf")):
        raise HTTPException(status_code=400, detail="Activity is full")

    # Validate student is not already signed up
    
    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
