Peer Tutor Matcher

Peer Tutor Microservice is a project that I did as an intern at Turtil.co. It is a configurable, machine-learning-based system to match students with suitable peer tutors. Built with FastAPI, Scikit-learn, and containerized via Docker, this project uses simulated datasets for testing and demonstration. It predicts and ranks peer tutors in real time using RandomForestClassifier.

Features:

->Intelligent peer tutor matching based on:

       Tutor's karma points in requested topic

       College and branch match

       Tutor's recent activity

       Year of Study compatibility

       Machine learning probability score

-> Fully configurable via config.json

-> FastAPI-powered REST API

-> Docker-ready deployment

-> Dataset auto-regeneration with fresh timestamps

Project Structure:

├── .dockerignore                  - Excluded files for clean builds

├── Dockerfile                     - Docker container setup

├── README.md                      - Documentation

├── api_test_match                 - sample match test

├── config.json                    - Matching rules & model settings

├── feature_set.json               - Extracted feature set (optional)

├── main.py                        - FastAPI application

├── matcher.py                     - Tutor matching logic

├── model.pkl                      - Pre-trained ML model

├── requirements.txt               - Python dependencies

├── studentsdata.py             - Script to regenerate demo dataset

└── students.json                  - Peer tutor dataset (simulated)




Prerequisites:

-> Python 3.12+

-> Docker (optional, for containerized deployment)


Setup & Usage:

1. Clone the Repo

          git clone https://github.com/your-username/peer-tutor-matcher.git

          cd peer-tutor-matcher

2. Install Dependencies

          pip install -r requirements.txt

3. Regenerate Demo Dataset (Recommended)

          python student_dataset.py

   The dataset students.json uses simulated data with activity dates based on your system's current date.
   This ensures dates like last_helped_on remain within the max_inactive_days window defined in config.json.

4. Start the FastAPI Service

          uvicorn main:app --reload

    API accessible at:

    http://127.0.0.1:8000


Docker Deployment:

Build the Image:-

     docker build -t peer-tutor-matcher .

Run the Container:-

     docker run -d -p 8000:8000 peer-tutor-matcher

API Endpoints:

GET	/	Welcome -message

GET	/status	-Health check

GET	/peers	-Total available peer tutors

POST	/match-peer-tutors	-Recommend suitable peer tutors

Example Match Request:

     {
       "user_id": "stu_9202",
       "topic": "OS",
       "college": "PEC",
       "branch": "IT",
       "year": 2
     }

Example Response:

     {
       "user_id": "stu_9202",
       "matched_peers": [
         {
           "peer_id": "stu_2409",
           "name": "Aarav P",
           "college": "CVR College of Engineering",
           "karma_in_topic": 99,
           "match_score": 0.96,
           "predicted_help_probability": 0.96,
           "last_helped_on": "2025-06-15"
         },
         {
           "peer_id": "stu_2497",
           "name": "Karthik V",
           "college": "PEC",
           "karma_in_topic": 76,
           "match_score": 0.96,
           "predicted_help_probability": 0.96,
           "last_helped_on": "2025-06-16"
         },
         {
           "peer_id": "stu_2001",
           "name": "Aditi R",
           "college": "Mahindra Institute of Technology",
           "karma_in_topic": 91,
           "match_score": 0.94,
           "predicted_help_probability": 0.94,
           "last_helped_on": "2025-06-15"
         }
       ],
       "status": "success"
     }


Simulated Dataset Details:

->students.json contains generated peer tutor profiles

->Use student_dataset.py to regenerate this file with:

     Random peer profiles

     Random karma points per topic

     Recent last_helped_on dates respecting max_inactive_days

  This keeps test results relevant and prevents stale data.

Notes:

->All datasets are simulated — no real personal data used

->Logs such as features_log.csv generated during runtime for debugging


Technologies Used:

->FastAPI

->Scikit-learn 

->Pandas 

->Docker 

->Uvicorn

->Joblib

->Python 3.12 
