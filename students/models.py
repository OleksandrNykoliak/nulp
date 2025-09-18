from django.db import models
from django.utils import timezone
class Student(models.Model):
    INSTITUTE_CHOICES = [
        ('ІАДУ', 'ІАДУ'),
        ('ІАРД', 'ІАРД'),
        ('ІБІД', 'ІБІД'),
        ('ІГДГ', 'ІГДГ'),
        ('ІГСН', 'ІГСН'),
        ('ІНЕМ', 'ІНЕМ'),
        ('ІЕСК', 'ІЕСК'),
        ('ІМІТ', 'ІМІТ'),
        ('ІПМТ', 'ІПМТ'),
        ('ІКНІ', 'ІКНІ'),
        ('ІКТА', 'ІКТА'),
        ('ІКТЕ', 'ІКТЕ'),
        ('ІППО', 'ІППО'),
        ('ІППТ', 'ІППТ'),
        ('ІМФН', 'ІМФН'),
        ('ІСТР', 'ІСТР'),
        ('ІХХТ', 'ІХХТ'),
    ]
    
    COURSE_CHOICES = [(i, str(i)) for i in range(1, 7)]
    
    UKRAINIAN_REGIONS = [
        ('Вінницька', 'Вінницька'),
        ('Волинська', 'Волинська'),
        ('Дніпропетровська', 'Дніпропетровська'),
        ('Донецька', 'Донецька'),
        ('Житомирська', 'Житомирська'),
        ('Закарпатська', 'Закарпатська'),
        ('Запорізька', 'Запорізька'),
        ('Івано-Франківська', 'Івано-Франківська'),
        ('Київська', 'Київська'),
        ('Кіровоградська', 'Кіровоградська'),
        ('Луганська', 'Луганська'),
        ('Львівська', 'Львівська'),
        ('Миколаївська', 'Миколаївська'),
        ('Одеська', 'Одеська'),
        ('Полтавська', 'Полтавська'),
        ('Рівненська', 'Рівненська'),
        ('Сумська', 'Сумська'),
        ('Тернопільська', 'Тернопільська'),
        ('Харківська', 'Харківська'),
        ('Херсонська', 'Херсонська'),
        ('Хмельницька', 'Хмельницька'),
        ('Черкаська', 'Черкаська'),
        ('Чернівецька', 'Чернівецька'),
        ('Чернігівська', 'Чернігівська'),
        ('АР Крим', 'АР Крим'),
    ]
    
    
    DORMITORY_NUMBERS = [(i, str(i)) for i in range(1, 24)]
    
    DORMITORY_ADDRESSES = {
        1: "м. Львів, вул. Бой-Желенського Т., 14",
        3: "м. Львів, вул. Карпинця І., 27",
        4: "м. Львів, вул. Сахарова А., акад., 25",
        5: "м. Львів, вул. Лукаша М., 4",
        7: "м. Львів, вул. Лукаша М., 1",
        8: "м. Львів, вул. Сахарова А., акад., 23",
        9: "м. Львів, вул. Лукаша М., 2",
        10: "м. Львів, вул. Відкрита, 1",
        11: "м. Львів, вул. Лукаша М., 5",
        12: "м. Львів, вул. Лазаренка Є., акад., 38",
        14: "м. Львів, вул. Лазаренка Є., акад., 40",
        15: "м. Львів, вул. Лазаренка Є., акад., 42",
        17: "м. Львів, вул. Пулюя І., 33",
        18: "м. Львів, вул. Плужника Є., 5",
        19: "смт. Брюховичі, вул. Сухомлинського В., 18",
        20: "м. Львів, вул. Під Голоском, 20",
        21: "м. Львів, вул. Пулюя І., 33",
        22: "м. Львів, вул. Володимира Великого, 57",
        23: "м. Львів, вул. Під Голоском, 23",
    }
        
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    full_name = models.CharField(max_length=200, verbose_name="ПІБ студента")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Дата народження")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    institute = models.CharField(max_length=10, choices=INSTITUTE_CHOICES, blank=True, null=True, verbose_name="ННІ")
    course = models.IntegerField(choices=COURSE_CHOICES, blank=True, null=True, verbose_name="Курс")
    enrollment_year = models.DateField(blank=True, null=True, verbose_name="Рік вступу")
    graduation_year = models.DateField(blank=True, null=True, verbose_name="Рік закінчення навчання")
    passport_data = models.CharField(max_length=50, blank=True, null=True, verbose_name="Серія та номер паспорта/ID")
    passport_issue_date = models.DateField(blank=True, null=True, verbose_name="Дата видачі паспорта/ID")
    passport_issued_by = models.CharField(max_length=200, blank=True, null=True, verbose_name="Ким виданий паспорт/ID")
    country = models.CharField(max_length=50, default="Україна", blank=True, null=True, verbose_name="Країна")
    region = models.CharField(max_length=50, choices=UKRAINIAN_REGIONS, blank=True, null=True, verbose_name="Область")
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name="Місто")
    address = models.CharField(max_length=200, blank=True, null=True, verbose_name="Адреса проживання")
    dormitory_number = models.IntegerField(choices=DORMITORY_NUMBERS, blank=True, null=True, verbose_name="Номер гуртожитку")
    # dormitory_address = models.CharField(max_length=200, blank=True, null=True, verbose_name="Адреса гуртожитку")  # 🔹 нове поле
    room_number = models.CharField(max_length=10, blank=True, null=True, verbose_name="Номер кімнати")
    contract_date = models.DateField(blank=True, null=True, verbose_name="Дата договору")
    contract_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Номер договору")
    contract_termination_date = models.DateField(blank=True, null=True, verbose_name="Дата розірвання договору")
    registration_consent = models.BooleanField(default=False, verbose_name="Згода на реєстрацію")
    registration_date = models.DateField(blank=True, null=True, verbose_name="Дата реєстрації прописки")
    registration_dormitory = models.IntegerField(choices=DORMITORY_NUMBERS, blank=True, null=True, verbose_name="Номер гуртожитку реєстрації")
    deregistration_date = models.DateField(blank=True, null=True, verbose_name="Дата зняття з реєстрації")
    notes = models.TextField(blank=True, null=True, verbose_name="Примітки")
    contract_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Номер договору")

    @property
    def dormitory_address(self):
        return self.DORMITORY_ADDRESSES.get(self.dormitory_number, "___")
        def __str__(self):
            return self.full_name
    
    def save(self, *args, **kwargs):
        if not self.contract_number and self.dormitory_number:
            # беремо поточний рік
            current_year = timezone.now().year

            # шукаємо останній договір у цьому гуртожитку за цей рік
            last_contract = Student.objects.filter(
                dormitory_number=self.dormitory_number,
                contract_number__startswith=f"{self.dormitory_number}-{current_year}"
            ).exclude(contract_number__isnull=True).exclude(contract_number="") \
            .order_by("-created_at").first()

            if last_contract:
                try:
                    last_seq = int(last_contract.contract_number.split("-")[-1])
                except (ValueError, IndexError):
                    last_seq = 0
            else:
                last_seq = 0

            new_seq = last_seq + 1

            # Генеруємо номер: <гуртожиток>-<рік>-<порядковий>
            self.contract_number = f"{self.dormitory_number}-{current_year}-{new_seq}"

        super().save(*args, **kwargs)


    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенти"
        
        
        
    