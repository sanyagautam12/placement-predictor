import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os

data = {
    "cgpa": np.random.uniform(5.0, 9.5, 200),
    "projects": np.random.randint(0, 5, 200),
    "internships": np.random.randint(0, 3, 200),
    "python": np.random.randint(0, 2, 200),
    "dsa": np.random.randint(0, 2, 200),
    "webdev": np.random.randint(0, 2, 200),
    "ml": np.random.randint(0, 2, 200),
    "certifications": np.random.randint(0, 6, 200),
    "communication": np.random.randint(1, 11, 200),
    "problem_solving": np.random.randint(1, 11, 200),
    "extracurriculars": np.random.randint(1, 11, 200),
    "age": np.random.randint(18, 26, 200),
    "gender": np.random.randint(0, 3, 200),  # 0 = M, 1 = F, 2 = O
    "department": np.random.randint(0, 4, 200),  # 0 = CSE, 1 = IT, 2 = ECE, 3 = Mech
    "placed": np.random.randint(0, 2, 200)
}

df = pd.DataFrame(data)

os.makedirs("data", exist_ok=True)
df.to_csv("data/student_data.csv", index=False)
print("✅ Dataset saved as data/student_data.csv")

X = df.drop("placed", axis=1)
y = df["placed"]

print("Training on features:", X.columns.tolist())
print("Shape:", X.shape)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Model Accuracy:", accuracy)

os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/placement_model.pkl")
print(" Model saved as model/placement_model.pkl")