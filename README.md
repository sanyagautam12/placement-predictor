🎯 Placement Predictor
A machine learning web application that predicts a student's placement chances based on academic, technical, and soft skills.

Live Demo
[Coming Soon – Deploying via Render/Netlify]

Features
Predicts whether a student is likely to be placed or not

Takes input such as:
Age, Gender, Department, CGPA
Internships, Projects, Certifications
Technical skills (Python, DSA, WebDev, ML)
Communication skills, Problem-solving, Extracurriculars

Displays:
Prediction result and placement probability
Feature input overview plot
Suggestions for improvement
Option to load sample student profiles

ML Model
Algorithm: RandomForest Classifier

Trained On: Synthetic (or custom) student dataset

Model File: model/placement_model.pkl

Project Structure
placement-predictor/
├── app.py
├── train_model.py
├── model/
│   └── placement_model.pkl
├── static/
│   ├── css/style.css
│   └── js/main.js
├── templates/
│   └── index.html
├── utils/
│   └── preprocessing.py
├── requirements.txt
└── README.md

Future Improvements
Deploy the app online (Render/Netlify)
Add user authentication
Store predictions in a database
Add admin panel to track analytics

Author
Sanya Gautam
GitHub: sanyagautam12
Portfolio: Coming Soon

Show Your Support
If you like this project, please star ⭐ the repo and share it with your friends!