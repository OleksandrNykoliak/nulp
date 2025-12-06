from django import forms
from .models import Student

from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'enrollment_year': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'graduation_year': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'passport_issue_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'contract_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'contract_termination_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'registration_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'deregistration_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'settlement_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'eviction_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'notes': forms.Textarea(attrs={'rows': 3, 'cols': 40, 'class': 'form-control'}),

        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contract_number'].disabled = True
        # date_fields вручну кажемо які формати приймати
        date_fields = [
            'date_of_birth', 'enrollment_year', 'graduation_year',
            'passport_issue_date', 'contract_date', 'contract_termination_date',
            'registration_date', 'deregistration_date',
            'settlement_date', 'eviction_date',
        ]
        for f in date_fields:
            self.fields[f].input_formats = ['%Y-%m-%d']
        
        # всі поля необов’язкові крім ПІБ
        for field_name, field in self.fields.items():
            if field_name != 'full_name':
                field.required = False


# # forms.py
# class StudentSearchForm(forms.Form):
#     search = forms.CharField(required=False, label="Пошук")
#     institute = forms.ChoiceField(
#         choices=[('', '---------')] + Student.INSTITUTE_CHOICES, 
#         required=False, 
#         label="ННІ"
#     )
#     course = forms.ChoiceField(
#         choices=[('', '---------')] + Student.COURSE_CHOICES, 
#         required=False, 
#         label="Курс"
#     )
#     dormitory = forms.ChoiceField(
#         choices=[('', '---------')] + Student.DORMITORY_NUMBERS, 
#         required=False, 
#         label="Гуртожиток"
#     )
    
    
class StudentSearchForm(forms.Form):
    search = forms.CharField(required=False, label="Пошук")
    institute = forms.ChoiceField(
        choices=[('', '---------')] + Student.INSTITUTE_CHOICES, 
        required=False, 
        label="ННІ"
    )
    course = forms.ChoiceField(
        choices=[('', '---------')] + Student.COURSE_CHOICES, 
        required=False, 
        label="Курс"
    )
    dormitory = forms.ChoiceField(
        choices=[('', '---------')] + Student.DORMITORY_NUMBERS, 
        required=False, 
        label="Гуртожиток"
    )
    # Додаємо фільтри за датами
    from_date_of_birth = forms.DateField(
        required=False, 
        label="Дата народження (від)",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    to_date_of_birth = forms.DateField(
        required=False, 
        label="Дата народження (до)",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    from_enrollment_year = forms.DateField(
        required=False, 
        label="Дата вступу (від)",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    to_enrollment_year = forms.DateField(
        required=False, 
        label="Дата вступу (до)",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    from_registration_date = forms.DateField(
        required=False, 
        label="Дата реєстрації (від)",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    to_registration_date = forms.DateField(
        required=False, 
        label="Дата реєстрації (до)",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    
from django import forms
from .models import Penalty

class PenaltyForm(forms.ModelForm):
    class Meta:
        model = Penalty
        fields = ['student', 'points', 'reason', 'comment', 'severity', 'penalty_date']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 3}),
            'comment': forms.Textarea(attrs={'rows': 2}),
            'penalty_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'points': 'Кількість штрафних балів',
            'reason': 'Причина штрафу',
            'comment': 'Додатковий коментар',
            'severity': 'Рівень порушення',
            'penalty_date': 'Дата порушення',
        }



class PenaltySearchForm(forms.Form):
    student_search = forms.CharField(
        required=False, 
        label='Пошук студента',
        widget=forms.TextInput(attrs={'placeholder': 'ПІБ студента'})
    )
    dormitory = forms.ChoiceField(
        choices=[('', '---------')] + Student.DORMITORY_NUMBERS,
        required=False,
        label='Гуртожиток'
    )
    status = forms.ChoiceField(
        choices=[('', '---------')] + [('active', 'Активні'), ('all', 'Всі')],
        required=False,
        label='Статус штрафів'
    )
    severity = forms.ChoiceField(
        choices=[('', '---------')] + Penalty.SEVERITY_CHOICES,
        required=False,
        label='Рівень порушення'
    )
    date_from = forms.DateField(
        required=False,
        label='Дата від',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    date_to = forms.DateField(
        required=False,
        label='Дата до',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    # НОВІ ПОЛЯ
    institute = forms.ChoiceField(
        choices=[('', '---------')] + Student.INSTITUTE_CHOICES,
        required=False,
        label='ННІ'
    )
    min_points = forms.ChoiceField(
        choices=[
    ('', '---------'),
    ('5', '5'),
    ('10', '10'),
    ('15', '15'),
    ('20', '20'),
    ('25', '25'),
        ],
        required=False,
        label='Мінімальна сума балів'
    )

class PenaltyCancellationForm(forms.ModelForm):
    class Meta:
        model = Penalty
        fields = ['cancellation_reason']
        widgets = {
            'cancellation_reason': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Вкажіть причину скасування штрафного балу...'}),
        }
        labels = {
            'cancellation_reason': 'Причина скасування',
        }
        
from .models import PenaltyReduction 
# Додайте після PenaltyCancellationForm
class PenaltyReductionForm(forms.ModelForm):
    class Meta:
        model = PenaltyReduction
        fields = ['student', 'penalty', 'points_reduced', 'reason', 'work_details', 'reduction_date', 'notes']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Причина списання балів...'}),
            'work_details': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Опишіть, як студент відпрацював порушення...'}),
            'notes': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Додаткові примітки...'}),
            'reduction_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'points_reduced': 'Кількість списаних балів',
            'reason': 'Причина списання',
            'work_details': 'Опис відпрацювання',
            'reduction_date': 'Дата відпрацювання',
            'notes': 'Додаткові примітки',
        }
    
    def __init__(self, *args, **kwargs):
        student_id = kwargs.pop('student_id', None)
        super().__init__(*args, **kwargs)
        
        if student_id:
            # Фільтруємо студента
            self.fields['student'].queryset = Student.objects.filter(id=student_id)
            self.fields['student'].initial = student_id
            self.fields['student'].disabled = True
            
            # Фільтруємо тільки активні штрафи цього студента
            self.fields['penalty'].queryset = Penalty.objects.filter(
                student_id=student_id, 
                status='active'
            )