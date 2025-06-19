import random
from flask import Flask, render_template, request, jsonify
import joblib  # Change from pickle to joblib
import numpy as np
import base64
import io
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Load the trained model
model_path = os.path.join(os.path.dirname(__file__), "model", "placement_model.pkl")
model = joblib.load(model_path)  # Use joblib.load instead of pickle.load

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract form data
        name = request.form.get('name')
        age = int(request.form['age'])

        # Encode gender
        gender_map = {'M': 0, 'F': 1, 'O': 2}
        gender = gender_map.get(request.form['gender'], 0)

        # Encode department
        dept_map = {
            'Computer Science': 0,
            'Information Technology': 1,
            'Electronics': 2,
            'Mechanical': 3,
            'Electrical': 4,
            'Civil': 5,
            'Chemical': 6,
            'Biotechnology': 7,
            'Aerospace': 8,
            'Data Science': 9,
            'AI & ML': 10,
            'IoT': 11
        }
        department = dept_map.get(request.form['department'], 0)

        # Numeric fields
        cgpa = float(request.form['cgpa'])
        projects = int(request.form['projects'])
        internships = int(request.form['internships'])
        certifications = int(request.form['certifications'])
        communication = int(request.form['communication'])
        problem_solving = int(request.form['problem_solving'])
        extracurriculars = int(request.form['extracurriculars'])

        # Technical skills (checkboxes)
        python_skill = 1 if 'python' in request.form else 0
        java_skill = 1 if 'java' in request.form else 0
        cpp_skill = 1 if 'cpp' in request.form else 0
        dsa_skill = 1 if 'dsa' in request.form else 0
        webdev_skill = 1 if 'webdev' in request.form else 0
        ml_skill = 1 if 'ml' in request.form else 0
        cloud_skill = 1 if 'cloud' in request.form else 0
        devops_skill = 1 if 'devops' in request.form else 0
        cybersecurity_skill = 1 if 'cybersecurity' in request.form else 0
        database_skill = 1 if 'database' in request.form else 0
        mobile_skill = 1 if 'mobile' in request.form else 0
        blockchain_skill = 1 if 'blockchain' in request.form else 0

        # Calculate total skills for prediction (maintaining original 4 skill slots)
        programming_skills = python_skill + java_skill + cpp_skill
        advanced_skills = cloud_skill + devops_skill + cybersecurity_skill
        specialized_skills = database_skill + mobile_skill + blockchain_skill
        
        # Use the most prominent skills for the model's 4 skill slots
        input_data = np.array([[age, gender, department, cgpa, projects, internships,
                              programming_skills > 0, dsa_skill, webdev_skill, ml_skill,
                              certifications, communication, problem_solving, extracurriculars]])

        # Make prediction
        prediction = model.predict(input_data)[0]
        probability = round(model.predict_proba(input_data)[0][1] * 100, 2)

        # Update result based on both prediction and probability
        if probability >= 60:
            result = "Likely to be Placed"
            prediction = 1
        else:
            result = "Unlikely to be Placed"
            prediction = 0

        # Update feature importance plot
        plt.figure(figsize=(7, 5))
        features = ['Age', 'Gender', 'Dept', 'CGPA', 'Projects', 'Internships', 'Prog', 'DSA', 'WebDev',
                   'ML', 'Certs', 'Comm', 'ProbSolv', 'Extra']
        plt.barh(features, input_data[0])
        plt.xlabel('Value')
        plt.title('Feature Input Overview')
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plot_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()

        # Update suggestions logic
        suggestions = []
        if probability < 60:  # Only show suggestions if probability is below 60%
            suggestions.append(f"⚠️ Your placement probability is {probability}%. Here's how to improve:")
            if cgpa < 7.0:
                suggestions.append("📘 Improve your CGPA to meet most companies' cut-off criteria.")
            if communication < 6:
                suggestions.append("Improve communication skills to stand out in interviews.")
            if problem_solving < 6:
                suggestions.append("Practice more problem-solving questions and mock tests.")
            if internships < 1:
                suggestions.append("Gain practical experience through internships.")
            if certifications < 3:
                suggestions.append("Consider completing industry-relevant certifications.")
            if projects < 2:
                suggestions.append("Build more hands-on projects to strengthen your portfolio.")
            if extracurriculars < 4:
                suggestions.append("Participate in clubs, competitions, or volunteering to boost your profile.")
            
            # New skill-based suggestions
            total_skills = sum([python_skill, java_skill, cpp_skill, dsa_skill, webdev_skill, ml_skill,
                              cloud_skill, devops_skill, cybersecurity_skill, database_skill, mobile_skill, blockchain_skill])
            if total_skills < 3:
                suggestions.append("🔧 Develop more technical skills to increase your versatility.")
            if not any([python_skill, java_skill, cpp_skill]):
                suggestions.append("Learn at least one major programming language (Python, Java, or C++).")
            if not any([cloud_skill, devops_skill]):
                suggestions.append("Consider learning cloud computing or DevOps - highly demanded skills.")
            if not any([database_skill, cybersecurity_skill]):
                suggestions.append("Add fundamental skills like database management or cybersecurity.")
            
            if len(suggestions) == 1:  # Only header, no weak areas found
                suggestions.append("Consider exploring more specialized skills to stand out in your field.")
        if not (python_skill or dsa_skill or webdev_skill or ml_skill):
                suggestions.append("🔧 Add some technical skills (e.g., Python, DSA, WebDev, ML).")
        elif len(suggestions) == 1:  # Only header, no weak areas found
                suggestions.append("Consider exploring more internships or certifications to boost your resume.")
        else:
            suggestions.append("You're on track! Continue refining your technical and soft skills.")
            if certifications < 4:
                suggestions.append("Consider pursuing advanced certifications or online specializations.")
            if extracurriculars < 5:
                suggestions.append("Get more involved in extracurriculars or leadership roles.")

        # ✅ Properly return the response after suggestion logic
        return jsonify({
            'name': name,
            'prediction': result,
            'probability': probability,
            'plot': plot_base64,
            'suggestions': suggestions
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/sample-data')
def sample_data():
    samples = {
        "1": {
            'name': 'Sanya Gautam',
            'age': 21,
            'gender': 'F',
            'department': 'Computer Science',
            'cgpa': 8.2,
            'projects': 2,
            'internships': 1,
            'certifications': 2,
            'communication': 7,
            'problem_solving': 6,
            'extracurriculars': 5,
            'skills': ['python', 'dsa']
        },
        "2": {
            'name': 'Rahul Sharma',
            'age': 22,
            'gender': 'M',
            'department': 'Mechanical',
            'cgpa': 6.5,
            'projects': 1,
            'internships': 0,
            'certifications': 1,
            'communication': 5,
            'problem_solving': 4,
            'extracurriculars': 3,
            'skills': ['ml']
        },
        "3": {
            'name': 'Ananya Verma',
            'age': 20,
            'gender': 'F',
            'department': 'Electronics',
            'cgpa': 9.1,
            'projects': 3,
            'internships': 2,
            'certifications': 4,
            'communication': 9,
            'problem_solving': 8,
            'extracurriculars': 7,
            'skills': ['java', 'ml', 'cloud', 'database']
        }
    }
    return jsonify(samples)


if __name__ == '__main__':
    app.run(debug=True)