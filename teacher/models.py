from django.db import models
from django.contrib.auth.models import User

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="teacher")
    teacher_id = models.IntegerField()
    phone = models.CharField(max_length=13, null= True, blank= True)
    permanent_address = models.CharField(max_length=100, null = True, blank=True)
    picture = models.ImageField(upload_to="profile/")

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Degree(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='degrees', null= True)  # ✅ KEY FIX
    degree_name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=30)
    university = models.CharField(max_length=40)
    passing_year = models.DateField()
    result = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.degree_name} - {self.university}"