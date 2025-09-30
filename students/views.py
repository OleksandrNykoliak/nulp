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


@login_required
def student_list(request):
    form = StudentSearchForm(request.GET or None)
    students = Student.objects.all().order_by('full_name') 
    
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
