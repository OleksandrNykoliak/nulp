import os
import django
import random
from datetime import date, timedelta

# Налаштування Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_registry.settings')
django.setup()

from students.models import Student
from django.contrib.auth import get_user_model
User = get_user_model()


def create_sample_students():
    first_names = ["Іван", "Олена", "Петро", "Марія", "Олексій", "Анна", "Андрій", "Наталія", "Сергій", "Юлія", "Дмитро", "Тетяна", "Михайло", "Катерина"]
    last_names = ["Шевченко", "Коваленко", "Бондаренко", "Ткаченко", "Кравченко", "Олійник", "Шевчук", "Сергієнко", "Савченко", "Бондар", "Лисенко", "Мельник"]
    middle_names = ["Олександрович", "Іванович", "Петрович", "Михайлович", "Васильович", "Олегівна", "Ігорівна", "Андріївна", "Сергіївна", "Володимирівна"]

    streets = ["Шевченка", "Франка", "Грушевського", "Лісова", "Центральна", "Соборна", "Незалежності"]
    cities = ["Київ", "Львів", "Одеса", "Харків", "Дніпро", "Запоріжжя", "Вінниця", "Житомир", "Чернігів", "Полтава"]

    institutes = [choice[0] for choice in Student.INSTITUTE_CHOICES]
    regions = [choice[0] for choice in Student.UKRAINIAN_REGIONS]
    person_types = [choice[0] for choice in Student.PERSON_TYPE_CHOICES]
    genders = [choice[0] for choice in Student.GENDER_CHOICES]
    categories = [choice[0] for choice in Student.CITY_TYPE_CHOICES]

    for i in range(20):  # 🔹 створюємо 20 студентів
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        middle_name = random.choice(middle_names)
        full_name = f"{last_name} {first_name} {middle_name}"

        # Вік від 18 до 25
        birth_year = random.randint(1998, 2005)
        birth_month = random.randint(1, 12)
        birth_day = random.randint(1, 28)
        date_of_birth = date(birth_year, birth_month, birth_day)

        phone = f"+380{random.randint(50, 99)}{random.randint(100, 999)}{random.randint(1000, 9999)}"
        institute = random.choice(institutes)
        course = random.randint(1, 6)

        enrollment_year = date(birth_year + 18, 9, 1)
        graduation_year = date(enrollment_year.year + course, 6, 30)

        region = random.choice(regions)
        city = random.choice(cities)
        address = f"вул. {random.choice(streets)} {random.randint(1, 200)}"

        dormitory = random.randint(1, 23)
        room_number = str(random.randint(100, 500))

        passport_data = f"AB{random.randint(100000, 999999)}"
        passport_issue_date = date(random.randint(2016, 2023), random.randint(1, 12), random.randint(1, 28))
        passport_issued_by = "Державна міграційна служба України"

        contract_date = date(2022, random.randint(1, 12), random.randint(1, 28))
        contract_number = f"Д-{random.randint(100, 999)}"
        contract_termination_date = date(2024, random.randint(1, 12), random.randint(1, 28))

        registration_consent = random.choice([True, False])
        registration_date = date(2022, random.randint(1, 12), random.randint(1, 28))
        registration_dormitory = random.randint(1, 23)
        deregistration_date = date(2023, random.randint(1, 12), random.randint(1, 28))

        notes = random.choice(["Зразковий студент", "Потребує консультацій", "Активний у громадському житті", None])

        # 🔹 Домашня адреса
        home_region = random.choice(regions)
        home_city = random.choice(cities)
        home_street = random.choice(streets)
        home_building = str(random.randint(1, 200))
        home_apartment = str(random.randint(1, 120))

        student = Student(
            type=random.choice(person_types),
            gender=random.choice(genders),
            category=random.choice(categories),
            full_name=full_name,
            date_of_birth=date_of_birth,
            phone=phone,
            institute=institute,
            course=course,
            enrollment_year=enrollment_year,
            graduation_year=graduation_year,
            passport_data=passport_data,
            passport_issue_date=passport_issue_date,
            passport_issued_by=passport_issued_by,
            country="Україна",
            region=region,
            city=city,
            address=address,
            dormitory_number=dormitory,
            room_number=room_number,
            contract_date=contract_date,
            contract_number=contract_number,
            contract_termination_date=contract_termination_date,
            registration_consent=registration_consent,
            registration_date=registration_date,
            registration_dormitory=registration_dormitory,
            deregistration_date=deregistration_date,
            notes=notes,

            # 👇 нові поля для домашньої адреси
            home_add_country="Україна",
            home_add_region=home_region,
            home_add_rajon=f"Район {random.randint(1, 20)}",
            home_add_category=random.choice(categories),
            home_add_city=home_city,
            home_add_street=f"вул. {home_street}",
            home_add_building=home_building,
            home_add_apartment=home_apartment,
        )

        student.save()
        print(f"✅ Створено {student.get_type_display()} ({student.get_gender_display()}): {full_name}")


def create_custom_superusers():
    users_with_passwords = {
        "Polishchuk": "PolishchukW5",
        "Andriiovskyj": "AndriiovskyjR2",
        "Dovha": "DovhaX9",
        "Stefinko": "StefinkoQ7",
        "Nedbaliuk": "NedbaliukT3",
        "Ivaneiko": "IvaneikoL4",
        "Kos": "KosZ8",
        "Verbyana": "VerbyanaM7",
        "Nykoliak": "NykoliakJ6",
    }

    for username, password in users_with_passwords.items():
        email = f"{username.lower()}@example.com"
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            print(f"👑 Створено суперюзера: {username} / {password}")
        else:
            print(f"⚠️ Суперюзер {username} вже існує")


if __name__ == "__main__":
    create_sample_students()
    create_custom_superusers()
    print("🎉 Наповнення бази даних завершено!")
