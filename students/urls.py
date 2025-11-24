from django.urls import path
from . import views

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('new/', views.student_create, name='student_create'),
    path('<int:pk>/edit/', views.student_update, name='student_update'),
    path('<int:pk>/delete/', views.student_delete, name='student_delete'),
    path('<int:pk>/contract/', views.student_contract_pdf, name='student_contract_pdf'), 
    path('login/', auth_views.LoginView.as_view(template_name='students/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('export/', views.student_export, name='student_export'),  # Додайте цей рядок
    path('<int:pk>/archive/', views.archive_student, name='archive_student'),
    path('archive/<int:pk>/unarchive/', views.unarchive_student, name='unarchive_student'),
    path('archive/', views.student_archive_list, name='student_archive_list'),
    path('archive/<int:pk>/', views.student_archive_detail, name='student_archive_detail'),
    path('all/', views.combined_student_list, name='combined_student_list'),
    path('penalties/', views.penalty_list, name='penalty_list'),
    path('penalties/new/', views.penalty_create, name='penalty_create'),
    path('penalties/student/<int:student_id>/new/', views.penalty_create_for_student, name='penalty_create_for_student'),
    path('penalties/<int:pk>/cancel/', views.penalty_cancel, name='penalty_cancel'),
    path('students-with-penalties/', views.students_with_penalties, name='students_with_penalties'),
    path('penalties/<int:pk>/delete/', views.penalty_delete, name='penalty_delete'),
]