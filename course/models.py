from django.db import models
from student.models import Semester, Student
from teacher.models import Teacher
from django.utils import timezone

# Part can be A or B
PartName = (
    ('A', 'A'),
    ('B', 'B'),
)

class Course(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    code = models.CharField(max_length=8)
    credit = models.IntegerField()
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Part(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(choices=PartName, max_length=2)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.course.code} - Part {self.name}"

class Class(models.Model):
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    class_number = models.IntegerField()
    date = models.DateField(default=timezone.now)
    topic = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    class Meta:
        ordering = ['-date', '-class_number']
        unique_together = ['part', 'class_number']
    
    def __str__(self):
        return f"{self.part} - Class {self.class_number}"

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('P', 'Present'),
        ('A', 'Absent'),
    ]
    
    class_session = models.ForeignKey(Class, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    
    class Meta:
        unique_together = ['class_session', 'student']
    
    def __str__(self):
        return f"{self.student} - {self.class_session} - {self.status}"

class CT(models.Model):
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    ct_number = models.IntegerField()
    date = models.DateField(default=timezone.now)
    topic = models.CharField(max_length=200, null=True)
    total_marks = models.IntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    
    class Meta:
        ordering = ['-date', '-ct_number']
        unique_together = ['part', 'ct_number']
    
    def __str__(self):
        return f"{self.part} - CT {self.ct_number}"

class CTResult(models.Model):
    ct = models.ForeignKey(CT, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    marks = models.FloatField()
    
    class Meta:
        unique_together = ['ct', 'student']
    
    def __str__(self):
        return f"{self.student} - {self.ct} - {self.marks}"

class Exam(models.Model):
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    topic = models.CharField(max_length=200, null=True)
    total_marks = models.IntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.part} - Semester Exam"

class ExamResult(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    marks = models.FloatField()
    
    class Meta:
        unique_together = ['exam', 'student']
    
    def __str__(self):
        return f"{self.student} - {self.exam} - {self.marks}"