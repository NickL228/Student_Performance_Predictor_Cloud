from django.shortcuts import render
import pickle
import os
from .models import Prediction

def predict_student(request):
    result = None

    if request.method == "POST":
        study_hours = int(request.POST["study_hours"])
        attendance = int(request.POST["attendance"])
        assignment_score = int(request.POST["assignment_score"])
        previous_grade = int(request.POST["previous_grade"])

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(BASE_DIR, "student_model.pkl")

        with open(model_path, "rb") as f:
            model = pickle.load(f)

        prediction = model.predict([[study_hours, attendance, assignment_score, previous_grade]])
        result = prediction[0]

        Prediction.objects.create(
            study_hours=study_hours,
            attendance=attendance,
            assignment_score=assignment_score,
            previous_grade=previous_grade,
            result=result
        )

    return render(request, "predictor/predict_student.html", {"result": result})

def history(request):
    data = Prediction.objects.all().order_by('-created_at')
    return render(request, "predictor/history.html", {"data": data})

def home(request):
    return render(request, "predictor/home.html")