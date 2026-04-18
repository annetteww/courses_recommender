from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    url = models.URLField()
    direction = models.CharField(max_length=200, blank=True)
    duration = models.CharField(max_length=100, blank=True)
    embedding = models.JSONField(null=True, blank=True)  # Для векторного представления
    
    def __str__(self):
        return self.title

class StudentProfile(models.Model):
    course_level = models.CharField(max_length=50, choices=[
        ('бакалавр', 'Бакалавр'),
        ('магистр', 'Магистр'),
        ('специалист', 'Специалист'),
    ])
    direction = models.CharField(max_length=200)
    interests = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def student_vector(self):
        # Простое векторное представление профиля студента
        return f"{self.course_level} {self.direction} {self.interests}"
