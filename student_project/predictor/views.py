from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import json
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


@csrf_exempt
def predict_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            study_hours = int(data["study_hours"])
            attendance = int(data["attendance"])
            assignment_score = int(data["assignment_score"])
            previous_grade = int(data["previous_grade"])

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

            return JsonResponse({"result": result})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Only POST requests allowed"}, status=405)


def history_api(request):
    predictions = Prediction.objects.all().order_by('-created_at')

    data = []
    for prediction in predictions:
        data.append({
            "id": prediction.id,
            "study_hours": prediction.study_hours,
            "attendance": prediction.attendance,
            "assignment_score": prediction.assignment_score,
            "previous_grade": prediction.previous_grade,
            "result": prediction.result,
            "created_at": prediction.created_at.strftime("%d/%m/%Y %H:%M")
        })

    return JsonResponse(data, safe=False)


@csrf_exempt
def register_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            username = data["username"]
            password = data["password"]

            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already exists"}, status=400)

            user = User.objects.create_user(username=username, password=password)
            user.save()

            return JsonResponse({"message": "User registered successfully"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Only POST requests allowed"}, status=405)


@csrf_exempt
def login_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            username = data["username"]
            password = data["password"]

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse({
                    "message": "Login successful",
                    "username": username,
                    "is_staff": user.is_staff
                })
            else:
                return JsonResponse({"error": "Invalid username or password"}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Only POST requests allowed"}, status=405)


@csrf_exempt
def logout_api(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse({"message": "Logout successful"})

    return JsonResponse({"error": "Only POST requests allowed"}, status=405)


def users_api(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Not logged in"}, status=403)

    if not request.user.is_staff:
        return JsonResponse({"error": "Admin only"}, status=403)

    users = User.objects.all().order_by("id")

    data = []
    for user in users:
        data.append({
            "id": user.id,
            "username": user.username,
            "is_staff": user.is_staff
        })

    return JsonResponse(data, safe=False)


@csrf_exempt
@require_POST
def delete_user_api(request, id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Not logged in"}, status=403)

    if not request.user.is_staff:
        return JsonResponse({"error": "Admin only"}, status=403)

    try:
        user = User.objects.get(id=id)

        if user.is_staff:
            return JsonResponse({"error": "Admin user cannot be deleted"}, status=400)

        user.delete()
        return JsonResponse({"status": "deleted"})

    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
    
@csrf_exempt
@require_POST
def delete_prediction(request, id):
    try:
        prediction = Prediction.objects.get(id=id)
        prediction.delete()
        return JsonResponse({"status": "deleted"})
    except Prediction.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)