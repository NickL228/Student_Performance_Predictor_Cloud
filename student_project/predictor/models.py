from django.db import models

class Prediction(models.Model):
    study_hours = models.IntegerField()
    attendance = models.IntegerField()
    assignment_score = models.IntegerField()
    previous_grade = models.IntegerField()
    result = models.CharField(max_length=10)

    created_at = models.DateTimeField(auto_now_add=True)