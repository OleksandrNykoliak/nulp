# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Student
from .forms import StudentForm, StudentSearchForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import os
import tempfile
import subprocess
from django.http import FileResponse
from docxtpl import DocxTemplate
import re
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import openpyxl
from openpyxl.styles import Font, Alignment
from django.http import HttpResponse
from django.utils import timezone


@login_required
def student_list(request):
    form = StudentSearchForm(request.GET or None)
    students = Student.objects.all().order_by('full_name') 
    
    if form.is_valid():
        search = form.cleaned_data.get('search')
        institute = form.cleaned_data.get('institute')
        course = form.cleaned_data.get('course')
        dormitory = form.cleaned_data.get('dormitory')
        from_date_of_birth = form.cleaned_data.get('from_date_of_birth')
        to_date_of_birth = form.cleaned_data.get('to_date_of_birth')
        from_enrollment_year = form.cleaned_data.get('from_enrollment_year')
        to_enrollment_year = form.cleaned_data.get('to_enrollment_year')
        from_registration_date = form.cleaned_data.get('from_registration_date')
        to_registration_date = form.cleaned_data.get('to_registration_date')
        
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

        # Фільтрація за датою народження
        if from_date_of_birth:
            students = students.filter(date_of_birth__gte=from_date_of_birth)
        if to_date_of_birth:
            students = students.filter(date_of_birth__lte=to_date_of_birth)

        # Фільтрація за датою вступу
        if from_enrollment_year:
            students = students.filter(enrollment_year__gte=from_enrollment_year)
        if to_enrollment_year:
            students = students.filter(enrollment_year__lte=to_enrollment_year)

        # Фільтрація за датою реєстрації
        if from_registration_date:
            students = students.filter(registration_date__gte=from_registration_date)
        if to_registration_date:
            students = students.filter(registration_date__lte=to_registration_date)
            
    paginator = Paginator(students, 50)
    page = request.GET.get('page')
    
    try:
        students_page = paginator.page(page)
    except PageNotAnInteger:
        students_page = paginator.page(1)
    except EmptyPage:
        students_page = paginator.page(paginator.num_pages)
    
    # Створюємо рядок параметрів для пагінації
    filter_params = request.GET.copy()
    if 'page' in filter_params:
        del filter_params['page']
    filter_query_string = filter_params.urlencode()
    
    context = {
        'students': students_page,
        'form': form,
        'filter_params': filter_query_string
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
    messages.error(request, "❌ Видалення заборонено. Будь ласка, створіть нового користувача.")
    return redirect('student_list')





@login_required
def student_contract_pdf(request, pk):
    student = get_object_or_404(Student, pk=pk)

    # Шлях до шаблону
    template_path = os.path.join(os.path.dirname(__file__), "contracts/contract.docx")

    # Завантажуємо шаблон Word
    doc = DocxTemplate(template_path)

    context = {
        "full_name": student.full_name or "____________________",
        "passport_data": student.passport_data or "____________________",
        "passport_record_number": getattr(student, "passport_record_number", "__________") or "__________",
        "institute": student.institute or "___",
        "course": student.course or "___",
        "dormitory_number": student.dormitory_number or "___",
        "dormitory_address": student.dormitory_address or "___",
        "room_number": student.room_number or "___",
        "contract_number": student.contract_number or "___",
        "contract_date": student.contract_date.strftime("%d.%m.%Y") if student.contract_date else "___",
        "termination_date": student.contract_termination_date.strftime("%d.%m.%Y") if student.contract_termination_date else "___",

        # фактична адреса
        "address": student.address or "____________________",
        "city": student.city or "____________________",
        "category": student.get_category_display() if student.category else "___",

        # телефон
        "phone": student.phone or "____________________",

        # паспорт
        "passport_issued_by": student.passport_issued_by or "____________________",
        "passport_issued_date": student.passport_issue_date.strftime("%d.%m.%Y") if student.passport_issue_date else "___",

        # домашня адреса
        "home_add_category": student.get_home_add_category_display() if student.home_add_category else "___",
        "home_add_city": student.home_add_city or "___",
        "home_add_street": student.home_add_street or "___",
        "home_add_building": student.home_add_building or "___",
        "home_add_apartment": student.home_add_apartment or "___",
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




# Додайте цю функцію після функції student_contract_pdf
@login_required
def student_export(request):
    # Використовуємо ту саму логіку фільтрації, що і в student_list
    form = StudentSearchForm(request.GET or None)
    students = Student.objects.all().order_by('full_name')
    
    if form.is_valid():
        search = form.cleaned_data.get('search')
        institute = form.cleaned_data.get('institute')
        course = form.cleaned_data.get('course')
        dormitory = form.cleaned_data.get('dormitory')
        from_date_of_birth = form.cleaned_data.get('from_date_of_birth')
        to_date_of_birth = form.cleaned_data.get('to_date_of_birth')
        from_enrollment_year = form.cleaned_data.get('from_enrollment_year')
        to_enrollment_year = form.cleaned_data.get('to_enrollment_year')
        from_registration_date = form.cleaned_data.get('from_registration_date')
        to_registration_date = form.cleaned_data.get('to_registration_date')
        
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

        # Фільтрація за датою народження
        if from_date_of_birth:
            students = students.filter(date_of_birth__gte=from_date_of_birth)
        if to_date_of_birth:
            students = students.filter(date_of_birth__lte=to_date_of_birth)

        # Фільтрація за датою вступу
        if from_enrollment_year:
            students = students.filter(enrollment_year__gte=from_enrollment_year)
        if to_enrollment_year:
            students = students.filter(enrollment_year__lte=to_enrollment_year)

        # Фільтрація за датою реєстрації
        if from_registration_date:
            students = students.filter(registration_date__gte=from_registration_date)
        if to_registration_date:
            students = students.filter(registration_date__lte=to_registration_date)

    # Створюємо нову книгу Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Студенти"

    # Додаємо заголовки
    headers = [
        'ПІБ', 'Дата народження', 'Телефон', 'ННІ', 'Курс',
        'Гуртожиток', 'Кімната', 'Дата реєстрації', 'Дата вступу', 'Дата закінчення',
        'Примітки', 'Паспортні дані', 'Дата видачі паспорта', 'Ким виданий паспорт',
        'Країна', 'Область', 'Район', 'Категорія', 'Місто', 'Адреса',
        'Домашня адреса: Країна', 'Область', 'Район', 'Категорія', 'Місто', 'Вулиця', 'Будинок', 'Квартира',
        'Дата договору', 'Номер договору', 'Дата розірвання договору',
        'Згода на реєстрацію', 'Дата реєстрації прописки', 'Гуртожиток реєстрації', 'Дата зняття з реєстрації'
    ]

    # Форматуємо заголовки
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal='center')

    # Додаємо дані
    for row, student in enumerate(students, 2):
        ws.cell(row=row, column=1, value=student.full_name)
        ws.cell(row=row, column=2, value=student.date_of_birth.strftime("%d.%m.%Y") if student.date_of_birth else '')
        ws.cell(row=row, column=3, value=student.phone or '')
        ws.cell(row=row, column=4, value=student.institute or '')
        ws.cell(row=row, column=5, value=student.course or '')
        ws.cell(row=row, column=6, value=student.dormitory_number or '')
        ws.cell(row=row, column=7, value=student.room_number or '')
        ws.cell(row=row, column=8, value=student.registration_date.strftime("%d.%m.%Y") if student.registration_date else '')
        ws.cell(row=row, column=9, value=student.enrollment_year.strftime("%d.%m.%Y") if student.enrollment_year else '')
        ws.cell(row=row, column=10, value=student.graduation_year.strftime("%d.%m.%Y") if student.graduation_year else '')
        ws.cell(row=row, column=11, value=student.notes or '')
        ws.cell(row=row, column=12, value=student.passport_data or '')
        ws.cell(row=row, column=13, value=student.passport_issue_date.strftime("%d.%m.%Y") if student.passport_issue_date else '')
        ws.cell(row=row, column=14, value=student.passport_issued_by or '')
        ws.cell(row=row, column=15, value=student.country or '')
        ws.cell(row=row, column=16, value=student.region or '')
        ws.cell(row=row, column=17, value=student.region_rajon or '')
        ws.cell(row=row, column=18, value=student.get_category_display() if student.category else '')
        ws.cell(row=row, column=19, value=student.city or '')
        ws.cell(row=row, column=20, value=student.address or '')
        ws.cell(row=row, column=21, value=student.home_add_country or '')
        ws.cell(row=row, column=22, value=student.home_add_region or '')
        ws.cell(row=row, column=23, value=student.home_add_rajon or '')
        ws.cell(row=row, column=24, value=student.get_home_add_category_display() if student.home_add_category else '')
        ws.cell(row=row, column=25, value=student.home_add_city or '')
        ws.cell(row=row, column=26, value=student.home_add_street or '')
        ws.cell(row=row, column=27, value=student.home_add_building or '')
        ws.cell(row=row, column=28, value=student.home_add_apartment or '')
        ws.cell(row=row, column=29, value=student.contract_date.strftime("%d.%m.%Y") if student.contract_date else '')
        ws.cell(row=row, column=30, value=student.contract_number or '')
        ws.cell(row=row, column=31, value=student.contract_termination_date.strftime("%d.%m.%Y") if student.contract_termination_date else '')
        ws.cell(row=row, column=32, value='Так' if student.registration_consent else 'Ні')
        ws.cell(row=row, column=33, value=student.registration_date.strftime("%d.%m.%Y") if student.registration_date else '')
        ws.cell(row=row, column=34, value=student.registration_dormitory or '')
        ws.cell(row=row, column=35, value=student.deregistration_date.strftime("%d.%m.%Y") if student.deregistration_date else '')

    # Автоматичне налаштування ширини стовпців
    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column_letter].width = adjusted_width

    # Створюємо відповідь
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    filename = f"students_export_{timezone.now().strftime('%Y-%m-%d_%H-%M')}.xlsx"
    response['Content-Disposition'] = f'attachment; filename={filename}'
    
    wb.save(response)
    return response

