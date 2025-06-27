import json
import random
from datetime import datetime, timedelta

NAMES = [
    "Sushanth M", "Priya S", "Anil K", "Nisha R", "Ravi T", "Sushanth M", "Aditi R",
    "Karthik V", "Meera T", "Rohan K", "Sneha L", "Vikram J", "Aarav P", "Ananya K",
    "Devansh R", "Ishita M", "Nikhil S", "Rhea T", "Sanjay L"
]

TOPICS = [
    "DBMS", "AutoCAD", "Math", "Physics", "Chemistry", "Java", "OS", "CNS", "DS"
]

COLLEGES = [
    "CVR College of Engineering", "VNR Vignana Jyothi", "GITAM University",
    "MGIT", "JNTUH", "PEC", "RCE", "Mahindra Institute of Technology"
]

BRANCHES = [
    "CSE", "ECE", "EEE", "Mechanical", "Civil", "IT", "CSE-AIML", "CSE-CS", "CSE-DS"
]

YEARS = [1, 2, 3, 4]

TOTAL_PEERS = 500  # Number of peer profiles to generate

peers = []

for i in range(TOTAL_PEERS):
    peer = {
        "peer_id": f"stu_{2000 + i}",
        "name": random.choice(NAMES),
        "college": random.choice(COLLEGES),
        "branch": random.choice(BRANCHES),
        "year": random.choice(YEARS),
        "topics": {}
    }

    num_topics = random.randint(1, 5)  
    chosen_topics = random.sample(TOPICS, num_topics)

    for topic in chosen_topics:
        days_ago = random.randint(0, 30)  # Active within last 30 days
        last_helped_on = (datetime.today().date() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        karma = random.randint(0, 100)

        peer["topics"][topic] = {
            "karma": karma,
            "last_helped_on": last_helped_on
        }

    peers.append(peer)

# Save to students.json
with open("data/students.json", "w") as f:
    json.dump(peers, f, indent=2)

print(f"✅ Generated {TOTAL_PEERS} peer profiles to data/students.json")