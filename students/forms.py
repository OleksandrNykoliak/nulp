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
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contract_number'].disabled = True
        # date_fields вручну кажемо які формати приймати
        date_fields = [
            'date_of_birth', 'enrollment_year', 'graduation_year',
            'passport_issue_date', 'contract_date', 'contract_termination_date',
            'registration_date', 'deregistration_date'
        ]
        for f in date_fields:
            self.fields[f].input_formats = ['%Y-%m-%d']
        
        # всі поля необов’язкові крім ПІБ
        for field_name, field in self.fields.items():
            if field_name != 'full_name':
                field.required = False


# forms.py
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