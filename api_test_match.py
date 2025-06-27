import requests

# Correct URL of your FastAPI server
url = "http://localhost:8000/match-peer-tutors"

# Example student request data
data = {
    "user_id": "stu_9202",
    "topic": "OS",
    "college": "PCE",
    "branch": "IT",
    "year": 2
}

# Send POST request to the API
try:
    response = requests.post(url, json=data)
    print("Status Code:", response.status_code)
    print("Response JSON:")
    print(response.json())
except Exception as e:
    print("Error connecting to API:", str(e))