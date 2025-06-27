from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import json
import logging
from matcher import TutorMatcher

logging.basicConfig(level=logging.INFO)

# Setup
with open("data/students.json", "r") as f:
    peer_profiles = json.load(f)

with open("config.json", "r") as f:
    settings = json.load(f)

model_file = settings.get("model_output_path", "model/model.pkl")
model = joblib.load(model_file)

matcher = TutorMatcher(model, peer_profiles, settings)

# FastAPI application
app = FastAPI(title="Peer Tutor Matcher")

class StudentRequest(BaseModel):
    user_id: str
    topic: str
    college: str
    branch: str
    year: int

@app.get("/")
def index():
    return {"message": "Peer Tutor Matching Service active."}

@app.get("/status")
def status_check():
    return {"status": "operational"}

@app.get("/peers")
def list_peers():
    return {"total_peers": len(peer_profiles)}

@app.post("/match-peer-tutors")
def find_matches(request: StudentRequest):
    logging.info(f"Received matching request from user: {request.user_id}")
    results = matcher.recommend(request)
    logging.info(f"Total matches found: {len(results['matched_peers'])}")
    return results