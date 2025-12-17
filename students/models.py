from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User
from django.urls import reverse

class Student(models.Model):
    INSTITUTE_CHOICES = [
        ('ІАДУ', 'ІАДУ'),
        ('ІАРД', 'ІАРД'),
        ('ІБІБ', 'ІБІБ'),
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
    CITY_TYPE_CHOICES = [
        ('city', 'м.'),
        ('settlement', 'с-ще'),
        ('village', 'с.'),
        ('villagesmt', 'смт.'),
    ]
    
    PERSON_TYPE_CHOICES = [
        ('student', 'Студент'),
        ('postgraduate', 'Аспірант'),
        ('doctoral', 'Докторант'),
        ('external', 'Сторонній'),
        ('staff', 'Співробітник'),
        ('child', 'Дитина'),
    ]
    
    GENDER_CHOICES = [
        ('m', 'ч'),
        ('f', 'ж'),
    ]
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    type = models.CharField(max_length=50, choices=PERSON_TYPE_CHOICES, blank=True, null=True, verbose_name="Тип")
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, blank=True, null=True, verbose_name="Стать")
    full_name = models.CharField(max_length=200, verbose_name="ПІБ студента")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Дата народження")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    institute = models.CharField(max_length=10, choices=INSTITUTE_CHOICES, blank=True, null=True, verbose_name="ННІ")
    course = models.IntegerField(choices=COURSE_CHOICES, blank=True, null=True, verbose_name="Курс")
    enrollment_year = models.DateField(blank=True, null=True, verbose_name="Рік вступу")
    graduation_year = models.DateField(blank=True, null=True, verbose_name="Рік закінчення навчання")
    passport_data = models.CharField(max_length=50, blank=True, null=True, verbose_name="Серія та номер паспорта/ID")
    passport_record_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="запис №")
    passport_issue_date = models.DateField(blank=True, null=True, verbose_name="Дата видачі паспорта/ID")
    passport_issued_by = models.CharField(max_length=200, blank=True, null=True, verbose_name="Ким виданий паспорт/ID")
    country = models.CharField(max_length=50, default="Україна", blank=True, null=True, verbose_name="Країна")
    region = models.CharField(max_length=50, choices=UKRAINIAN_REGIONS, blank=True, null=True, verbose_name="Область")
    region_rajon = models.CharField(max_length=200, blank=True, null=True, verbose_name="Район")
    category = models.CharField(max_length=50, choices=CITY_TYPE_CHOICES, blank=True, null=True, verbose_name="Категорія")
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name="Місто")
    address = models.CharField(max_length=200, blank=True, null=True, verbose_name="Вулиця")
    dormitory_number = models.IntegerField(choices=DORMITORY_NUMBERS, blank=True, null=True, verbose_name="Номер гуртожитку")
    room_number = models.CharField(max_length=10, blank=True, null=True, verbose_name="Номер кімнати")
    settlement_date = models.DateField(blank=True, null=True, verbose_name="Дата поселення")
    eviction_date = models.DateField(blank=True, null=True, verbose_name="Дата виселення")
    home_add_country = models.CharField(max_length=50, default="Україна", blank=True, null=True, verbose_name="Країна")
    home_add_region = models.CharField(max_length=50, choices=UKRAINIAN_REGIONS, blank=True, null=True, verbose_name="Область")
    home_add_rajon = models.CharField(max_length=200, blank=True, null=True, verbose_name="Район")
    home_add_category = models.CharField(max_length=50, choices=CITY_TYPE_CHOICES, blank=True, null=True, verbose_name="Категорія")
    home_add_city = models.CharField(max_length=50, blank=True, null=True, verbose_name="Місто")
    home_add_street = models.CharField(max_length=100, blank=True, null=True, verbose_name="Вулиця")
    home_add_building = models.CharField(max_length=20, blank=True, null=True, verbose_name="Будинок")
    home_add_apartment = models.CharField(max_length=20, blank=True, null=True, verbose_name="Квартира")
    contract_date = models.DateField(blank=True, null=True, verbose_name="Дата договору")
    contract_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Номер договору(не заповнюємо)")
    contract_termination_date = models.DateField(blank=True, null=True, verbose_name="Дата розірвання договору")
    registration_consent = models.BooleanField(default=False, verbose_name="Згода на реєстрацію")
    registration_date = models.DateField(blank=True, null=True, verbose_name="Дата реєстрації прописки")
    registration_dormitory = models.IntegerField(choices=DORMITORY_NUMBERS, blank=True, null=True, verbose_name="Номер гуртожитку реєстрації")
    deregistration_date = models.DateField(blank=True, null=True, verbose_name="Дата зняття з реєстрації")
    notes = models.TextField(blank=True, null=True, verbose_name="Примітки")
    history = HistoricalRecords()
    
    @property
    def total_penalty_points_with_reductions(self):
        """Загальна сума штрафних балів з урахуванням відпрацювань"""
        total_penalties = self.penalties.filter(status='active').aggregate(
            total=Sum('points')
        )['total'] or 0
        
        total_reductions = self.penalty_reductions.aggregate(
            total=Sum('points_reduced')
        )['total'] or 0
        
        return max(0, total_penalties - total_reductions)
    
    @property
    def dormitory_address(self):
        return self.DORMITORY_ADDRESSES.get(self.dormitory_number, "___")

    def __str__(self):
        return self.full_name
    
    def get_absolute_url(self):
        return reverse('student_update', args=[str(self.id)])
    
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

class StudentArchive(models.Model):
    # Всі поля з моделі Student
    original_student = models.OneToOneField(
        Student, 
        on_delete=models.CASCADE, 
        related_name='archive_record',
        verbose_name="Оригінальний студент"
    )
    archived_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата архівації")
    archived_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name="Ким архівовано"
    )
    
    # Дублюємо всі поля для незалежності даних
    created_at = models.DateTimeField(verbose_name="Дата створення")
    type = models.CharField(max_length=50, choices=Student.PERSON_TYPE_CHOICES, blank=True, null=True, verbose_name="Тип")
    gender = models.CharField(max_length=50, choices=Student.GENDER_CHOICES, blank=True, null=True, verbose_name="Стать")
    full_name = models.CharField(max_length=200, verbose_name="ПІБ студента")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Дата народження")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    institute = models.CharField(max_length=10, choices=Student.INSTITUTE_CHOICES, blank=True, null=True, verbose_name="ННІ")
    course = models.IntegerField(choices=Student.COURSE_CHOICES, blank=True, null=True, verbose_name="Курс")
    enrollment_year = models.DateField(blank=True, null=True, verbose_name="Рік вступу")
    graduation_year = models.DateField(blank=True, null=True, verbose_name="Рік закінчення навчання")
    passport_data = models.CharField(max_length=50, blank=True, null=True, verbose_name="Серія та номер паспорта/ID")
    passport_record_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="запис №")
    passport_issue_date = models.DateField(blank=True, null=True, verbose_name="Дата видачі паспорта/ID")
    passport_issued_by = models.CharField(max_length=200, blank=True, null=True, verbose_name="Ким виданий паспорт/ID")
    country = models.CharField(max_length=50, default="Україна", blank=True, null=True, verbose_name="Країна")
    region = models.CharField(max_length=50, choices=Student.UKRAINIAN_REGIONS, blank=True, null=True, verbose_name="Область")
    region_rajon = models.CharField(max_length=200, blank=True, null=True, verbose_name="Район")
    category = models.CharField(max_length=50, choices=Student.CITY_TYPE_CHOICES, blank=True, null=True, verbose_name="Категорія")
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name="Місто")
    address = models.CharField(max_length=200, blank=True, null=True, verbose_name="Вулиця")
    dormitory_number = models.IntegerField(choices=Student.DORMITORY_NUMBERS, blank=True, null=True, verbose_name="Номер гуртожитку")
    room_number = models.CharField(max_length=10, blank=True, null=True, verbose_name="Номер кімнати")
    settlement_date = models.DateField(blank=True, null=True, verbose_name="Дата поселення")
    eviction_date = models.DateField(blank=True, null=True, verbose_name="Дата виселення")
    home_add_country = models.CharField(max_length=50, default="Україна", blank=True, null=True, verbose_name="Країна")
    home_add_region = models.CharField(max_length=50, choices=Student.UKRAINIAN_REGIONS, blank=True, null=True, verbose_name="Область")
    home_add_rajon = models.CharField(max_length=200, blank=True, null=True, verbose_name="Район")
    home_add_category = models.CharField(max_length=50, choices=Student.CITY_TYPE_CHOICES, blank=True, null=True, verbose_name="Категорія")
    home_add_city = models.CharField(max_length=50, blank=True, null=True, verbose_name="Місто")
    home_add_street = models.CharField(max_length=100, blank=True, null=True, verbose_name="Вулиця")
    home_add_building = models.CharField(max_length=20, blank=True, null=True, verbose_name="Будинок")
    home_add_apartment = models.CharField(max_length=20, blank=True, null=True, verbose_name="Квартира")
    contract_date = models.DateField(blank=True, null=True, verbose_name="Дата договору")
    contract_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Номер договору")
    contract_termination_date = models.DateField(blank=True, null=True, verbose_name="Дата розірвання договору")
    registration_consent = models.BooleanField(default=False, verbose_name="Згода на реєстрацію")
    registration_date = models.DateField(blank=True, null=True, verbose_name="Дата реєстрації прописки")
    registration_dormitory = models.IntegerField(choices=Student.DORMITORY_NUMBERS, blank=True, null=True, verbose_name="Номер гуртожитку реєстрації")
    deregistration_date = models.DateField(blank=True, null=True, verbose_name="Дата зняття з реєстрації")
    notes = models.TextField(blank=True, null=True, verbose_name="Примітки")

    @property
    def dormitory_address(self):
        return Student.DORMITORY_ADDRESSES.get(self.dormitory_number, "___")

    def __str__(self):
        return f"Архів: {self.full_name}"

    class Meta:
        verbose_name = "Архівний студент"
        verbose_name_plural = "Архівні студенти"
        
        
    @property
    def total_penalty_points(self):
        return self.penalties.filter(status='active').aggregate(total=models.Sum('points'))['total'] or 0

    @property
    def active_penalties(self):
        return self.penalties.filter(status='active')

    @property
    def has_penalties(self):
        return self.penalties.filter(status='active').exists()
from django.db.models import Case, When, Sum, F, ExpressionWrapper
   
        
class Penalty(models.Model):
    SEVERITY_CHOICES = [
        (1, 'Незначне порушення'),
        (2, 'Середнє порушення'), 
        (3, 'Серйозне порушення'),
        (4, 'Критичне порушення'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Активний'),
        ('cancelled', 'Скасований'),
        ('expired', 'Неактивний'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Студент", related_name='penalties')
    points = models.PositiveIntegerField(default=1, verbose_name="Штрафні бали")
    reason = models.TextField(verbose_name="Причина штрафу")
    comment = models.TextField(blank=True, null=True, verbose_name="Коментар")
    severity = models.IntegerField(choices=SEVERITY_CHOICES, default=1, verbose_name="Важкість порушення")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name="Статус")
    penalty_date = models.DateField(default=timezone.now, verbose_name="Дата порушення")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Ким видано")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    cancelled_at = models.DateTimeField(blank=True, null=True, verbose_name="Дата скасування")
    cancelled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                   related_name='cancelled_penalties', verbose_name="Ким скасовано")
    cancellation_reason = models.TextField(blank=True, null=True, verbose_name="Причина скасування")
    
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.student.full_name} - {self.points} бал(ів) - {self.get_severity_display()}"
    
        # Додайте ці властивості до моделі Penalty
    @property
    def reduced_points(self):
        """Загальна кількість відпрацьованих балів для цього штрафу"""
        return self.reductions.aggregate(total=Sum('points_reduced'))['total'] or 0
    
    # @property
    # def remaining_points(self):
    #     """Залишок балів після відпрацювання"""
    #     return max(0, self.points - self.reduced_points)
    
    @property
    def total_reductions(self):
        """Загальна кількість списаних балів для цього штрафу"""
        return self.reductions.aggregate(total=Sum('points_reduced'))['total'] or 0
    
    @property
    def remaining_points(self):
        """Залишок балів після відпрацювання"""
        return max(0, self.points - self.total_reductions)
    
    @property
    def is_fully_reduced(self):
        """Чи повністю відпрацьований штраф"""
        return self.remaining_points == 0
    
    @property
    def is_active(self):
        return self.status == 'active'
    
    class Meta:
        verbose_name = "Штрафний бал"
        verbose_name_plural = "Штрафні бали"
        ordering = ['-penalty_date', '-created_at']

# Додайте властивість до моделі Student для підрахунку загальних штрафних балів


# Додайте після моделі Penalty
class PenaltyReduction(models.Model):
    """Модель для відпрацювання штрафних балів"""
    student = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE, 
        verbose_name="Студент", 
        related_name='penalty_reductions'
    )
    penalty = models.ForeignKey(
        Penalty, 
        on_delete=models.CASCADE, 
        verbose_name="Штраф",
        related_name='reductions',
        null=True, 
        blank=True
    )
    points_reduced = models.PositiveIntegerField(
        verbose_name="Кількість списаних балів",
        default=1
    )
    reason = models.TextField(
        verbose_name="Причина відпрацювання/списання"
    )
    work_details = models.TextField(
        verbose_name="Опис відпрацювання",
        help_text="Як саме студент відпрацював порушення"
    )
    reduction_date = models.DateField(
        default=timezone.now,
        verbose_name="Дата відпрацювання"
    )
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name="Ким зараховано"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата створення"
    )
    notes = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Додаткові примітки"
    )
    
    def __str__(self):
        return f"Відпрацювання {self.points_reduced} балів для {self.student.full_name}"
    
    class Meta:
        verbose_name = "Відпрацювання штрафу"
        verbose_name_plural = "Відпрацювання штрафів"
        ordering = ['-reduction_date', '-created_at']