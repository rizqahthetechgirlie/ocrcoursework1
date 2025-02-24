from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import student_dashboard, my_work, practice_quiz, my_progress, badges
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='newpassword/password_reset_form.html'),
         name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='newpassword/password_reset_done.html'),
         name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='newpassword/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='newpassword/password_reset_complete.html'),
         name='password_reset_complete'),
    path("my_work/", my_work, name="my_work"),
    path("practice_quiz/", practice_quiz, name="practice_quiz"),
    path("my_progress/", my_progress, name="my_progress"),
    path("badges/", badges, name="badges"),
]



