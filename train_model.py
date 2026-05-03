import pandas as pd
import random
from faker import Faker
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import pickle

fake = Faker()

data = []

for _ in range(50):
    study_hours = random.randint(1, 10)
    attendance = random.randint(40, 100)
    assignment_score = random.randint(30, 100)
    previous_grade = random.randint(30, 100)

    if study_hours > 5 and attendance > 60:
        result = "Pass"
    else:
        result = "Fail"

    data.append([
        study_hours,
        attendance,
        assignment_score,
        previous_grade,
        result
    ])

df = pd.DataFrame(data, columns=[
    "study_hours",
    "attendance",
    "assignment_score",
    "previous_grade",
    "result"
])

# Split data
X = df[["study_hours", "attendance", "assignment_score", "previous_grade"]]
y = df["result"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

model = DecisionTreeClassifier()
model.fit(X_train, y_train)

predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print("Model Accuracy:", accuracy)

example = [[6, 75, 70, 65]]
print("Prediction:", model.predict(example)[0])

with open("student_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model saved!")