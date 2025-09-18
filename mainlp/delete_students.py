# delete_students.py
import os
import django

# Налаштування Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_registry.settings')
django.setup()

from students.models import Student

def delete_all_students():
    count, _ = Student.objects.all().delete()
    print(f"❌ Видалено {count} студентів з бази даних")

if __name__ == "__main__":
    delete_all_students()
    print("✅ Очищення завершено!")
