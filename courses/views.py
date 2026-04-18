from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Course, StudentProfile
from .parsers import parse_dorea_courses
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import re

model = None

def load_model():
    global model
    if model is None:
        model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def index(request):
    return render(request, 'courses/index.html')

def parse_courses(request):
    """Парсит курсы при первом запуске"""
    count = parse_dorea_courses()
    return JsonResponse({'status': 'success', 'parsed': count})

def recommend_courses(request):
    if request.method == 'POST':
        course_level = request.POST.get('course_level')
        direction = request.POST.get('direction')
        interests = request.POST.get('interests')
        
        # Сохраняем профиль студента
        profile = StudentProfile.objects.create(
            course_level=course_level,
            direction=direction,
            interests=interests
        )
        
        # Получаем рекомендации
        recommendations = get_recommendations(course_level, direction, interests)
        
        return render(request, 'courses/results.html', {
            'recommendations': recommendations,
            'profile': profile
        })
    
    return redirect('index')

def get_recommendations(course_level, direction, interests):
    load_model()
    
    # Создаем вектор профиля студента
    student_text = f"{course_level} {direction} {interests}"
    student_embedding = model.encode(student_text)
    
    # Получаем все курсы с описаниями
    courses = Course.objects.exclude(embedding__isnull=True)
    
    if not courses.exists():
        # Если нет эмбеддингов, возвращаем первые 5 курсов
        return list(Course.objects.all()[:5])
    
    # Вычисляем схожесть
    course_texts = []
    course_embeddings = []
    
    for course in courses:
        text = f"{course.title} {course.description}"
        embedding = np.array(course.embedding)
        course_texts.append(text)
        course_embeddings.append(embedding)
    
    similarities = cosine_similarity([student_embedding], course_embeddings)[0]
    
    # Сортируем по схожести
    scored_courses = sorted(
        zip(courses, similarities), 
        key=lambda x: x[1], 
        reverse=True
    )
    
    return scored_courses[:10]
