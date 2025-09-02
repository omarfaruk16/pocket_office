# models.py
from django.db import models

class Semester(models.Model):
    name = models.CharField(max_length=50)
    year = models.CharField(max_length=5, null=True)

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20)
    semester = models.ForeignKey(Semester, null=True, blank=True, on_delete=models.SET_NULL)
    previous_semester = models.ForeignKey(Semester, null=True, blank=True, on_delete=models.SET_NULL, related_name="previous_semester")
    
   
    def __str__(self):
        return f"{self.name} ({self.student_id})"
