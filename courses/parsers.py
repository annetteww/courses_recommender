import requests
from bs4 import BeautifulSoup
from django.utils.html import strip_tags
import re
from .models import Course

def parse_dorea_courses():
    """Парсит курсы с do.rea.ru"""
    url = "https://do.rea.ru/"
    try:
        response = requests.get(url, timeout=30)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        courses = []
        # Ищем карточки курсов (адаптируйте селекторы под реальную структуру)
        course_elements = soup.find_all('div', class_=re.compile(r'course|program|card'))
        
        for elem in course_elements[:50]:  # Берем первые 50 курсов
            title_elem = elem.find(['h1', 'h2', 'h3', 'a', '.title'])
            url_elem = elem.find('a', href=True)
            desc_elem = elem.find(['p', '.description'])
            
            if title_elem and url_elem:
                title = title_elem.get_text(strip=True)
                course_url = url_elem['href']
                if not course_url.startswith('http'):
                    course_url = 'https://do.rea.ru' + course_url
                
                description = desc_elem.get_text(strip=True) if desc_elem else ''
                
                # Сохраняем или обновляем курс
                course, created = Course.objects.update_or_create(
                    url=course_url,
                    defaults={
                        'title': title,
                        'description': description[:1000],
                    }
                )
                courses.append(course)
        
        return len(courses)
    except Exception as e:
        print(f"Ошибка парсинга: {e}")
        return 0
