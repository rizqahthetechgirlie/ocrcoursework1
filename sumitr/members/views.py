

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import CustomLoginForm
from django.contrib.auth.decorators import login_required

def login_view(request):
    form = CustomLoginForm(data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.role == 'teacher':
                    return redirect('teacher_dashboard')
                elif user.role == 'senior_admin':
                    return redirect('admin_dashboard')
                else:
                    return redirect('student_dashboard')
            else:
                messages.error(request, "Invalid username or password")
    return render(request, 'members/login.html', {'form': form})
@login_required
def student_dashboard(request):
    return render(request, 'members/student_dashboard.html')

@login_required
def teacher_dashboard(request):
    return render(request, 'members/teacher_dashboard.html')

@login_required
def admin_dashboard(request):
    return render(request, 'members/admin_dashboard.html')
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Homework, Quiz, Progress, Badge

@login_required
def student_dashboard(request):
    """Displays the student dashboard with key sections."""
    return render(request, "members/student_dashboard.html")

@login_required
def my_work(request):
    """Shows assigned homework and due dates."""
    homework = Homework.objects.filter(student=request.user)
    return render(request, "members/my_work.html", {"homework": homework})

@login_required
def practice_quiz(request):
    """Allows students to attempt quizzes with feedback."""
    quizzes = Quiz.objects.all()  # This will be developed later, filter would be based on adaptive learning and algorithms.
    return render(request, "members/practice_quiz.html", {"quizzes": quizzes})

@login_required
def my_progress(request):
    """This displays topics practiced, acquired skills, and mastered skills."""
    progress = Progress.objects.get(user=request.user)
    return render(request, "members/my_progress.html", {"progress": progress})

@login_required
def badges(request):
    """This shows the badges earned by the student."""
    badges = Badge.objects.filter(user=request.user)
    return render(request, "members/badges.html", {"badges": badges})
