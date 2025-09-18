# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Student
from .forms import StudentForm, StudentSearchForm
from django.contrib.auth.decorators import login_required


# views.py
@login_required
def student_list(request):
    form = StudentSearchForm(request.GET or None)
    students = Student.objects.all()
    
    if form.is_valid():
        search = form.cleaned_data.get('search')
        institute = form.cleaned_data.get('institute')
        course = form.cleaned_data.get('course')
        dormitory = form.cleaned_data.get('dormitory')
        
        if search:
            students = students.filter(
                Q(full_name__icontains=search) |
                Q(phone__icontains=search)
            )
        
        if institute and institute != '---------':
            students = students.filter(institute=institute)
        
        if course and course != '---------':
            try:
                course_int = int(course)
                students = students.filter(course=course_int)
            except (ValueError, TypeError):
                pass
        
        if dormitory and dormitory != '---------':
            try:
                dormitory_int = int(dormitory)
                students = students.filter(dormitory_number=dormitory_int)
            except (ValueError, TypeError):
                pass
    
    context = {
        'students': students,
        'form': form,
        'filter_params': request.GET.urlencode()
    }
    return render(request, 'students/student_list.html', context)
@login_required
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    
    return render(request, 'students/student_form.html', {'form': form})
@login_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            # редірект назад на форму цього ж студента
            return redirect('student_update', pk=student.pk)
    else:
        form = StudentForm(instance=student)
    
    return render(request, 'students/student_form.html', {'form': form})
@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    
    return render(request, 'students/student_confirm_delete.html', {'student': student})




from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from .models import Student
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.http import HttpResponse
import os
from datetime import datetime
from reportlab.platypus import Table, TableStyle, PageBreak
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
import os

from .models import Student

import os
import tempfile
import subprocess
from django.http import HttpResponse, FileResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from docxtpl import DocxTemplate

from .models import Student


@login_required
def student_contract_pdf(request, pk):
    student = get_object_or_404(Student, pk=pk)

    # Шлях до шаблону
    template_path = os.path.join(os.path.dirname(__file__), "contracts/contract_template.docx")

    # Завантажуємо шаблон Word
    doc = DocxTemplate(template_path)

    # Контекст для підстановки
    context = {
        "full_name": student.full_name or "____________________",
        "passport_data": student.passport_data or "____________________",
        "institute": student.institute or "___",
        "course": student.course or "___",
        "dormitory_number": student.dormitory_number or "___",
        "dormitory_address": student.dormitory_address or "___",
        "room_number": student.room_number or "___",
        "contract_number": student.contract_number or "___",
        "contract_date": student.contract_date.strftime("%d.%m.%Y") if student.contract_date else "___",
        "termination_date": student.contract_termination_date.strftime("%d.%m.%Y") if student.contract_termination_date else "___",
        "address": student.address or "____________________",
        "city": student.city or "____________________",
        "phone": student.phone or "____________________",
        "passport_issued_by": student.passport_issued_by or "____________________",
        "passport_issue_date": student.passport_issue_date.strftime("%d.%m.%Y") if student.passport_issue_date else "___",
    }

    # Рендеримо DOCX з даними
    doc.render(context)

    # Тимчасові файли
    tmp_dir = tempfile.mkdtemp()
    docx_path = os.path.join(tmp_dir, "contract.docx")
    pdf_path = os.path.join(tmp_dir, "contract.pdf")

    # Зберігаємо DOCX
    doc.save(docx_path)

    # Конвертація в PDF через libreoffice
    subprocess.run([
        "libreoffice", "--headless", "--convert-to", "pdf", "--outdir", tmp_dir, docx_path
    ], check=True)

    # Повертаємо PDF у браузер
    surname = student.full_name.split()[0] if student.full_name else "contract"
    response = FileResponse(open(pdf_path, "rb"), content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="{surname}_contract.pdf"'
    return response




# ПІБ: Олійник Андрій Іванович
# Паспорт: AB505072
# Інститут: ІКТЕ, курс 4
# Гуртожиток № 19, кімната 122
# Дата договору: 09.09.2022
# Номер договору: Д-303
# Термін дії до: 07.08.2024
# Адреса: вул. Шевченка 76
# Телефон: +380557259938



# ПІБ: {{ full_name }}
# Паспорт: {{ passport_data }}
# Інститут: {{ institute }}, курс {{ course }}
# Гуртожиток № {{ dormitory_number }}, кімната {{ room_number }}

# Дата договору: {{ contract_date }}
# Номер договору: {{ contract_number }}
# Термін дії до: {{ termination_date }}
# Адреса: {{ address }}
# Телефон: {{ phone }}
