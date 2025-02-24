

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
class CustomUser(AbstractUser):
    STUDENT = "student"
    TEACHER = "teacher"
    SENIOR_ADMIN = "senior_admin"
    ROLE_CHOICES = [
        (STUDENT, "Student"),
        (TEACHER, "Teacher"),
        (SENIOR_ADMIN, "Senior Admin"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    year_group = models.CharField(max_length=20, blank=True, null=True)  # For students only
    guardian_email = models.EmailField(blank=True, null=True)  # For students only
    user_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    first_name =  models.CharField(max_length=20, blank=True, null=True)
    last_name =  models.CharField(max_length=20, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.user_id:
            # This generates a unique user id for every user automatically.
            last_user = CustomUser.objects.filter(role=self.role).order_by("-id").first()
            if last_user and last_user.user_id:
                numeric_part = int(last_user.user_id[2:])
                next_id = numeric_part + 1
            else:
                next_id = 1
            prefix = {"student": "ST", "teacher": "TE", "senior_admin": "SA"}.get(self.role, "US")
            self.user_id = f"{prefix}{next_id:03}"

        if not self.username:
            # Generate username using first letter of surname and first letter of first name
            base_username = f"{self.last_name[:4].lower()}{self.first_name[:1].lower()}{self.user_id[-3:]}"
            username = base_username
            counter = 1
            while CustomUser.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            self.username = username

        super().save(*args, **kwargs)
User = get_user_model()  # Using the custom user model
class Homework(models.Model):
    title = models.CharField(max_length=255)
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assigned_homework")  # Teacher/Admin
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="student_homework")  # Student
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.title} (Due: {self.due_date})"
class Quiz(models.Model):
     LEVEL_CHOICES = [("KS2", "KS2"), ("KS3", "KS3")]
     title = models.CharField(max_length=255)
     difficulty = models.CharField(max_length=50, choices=[("easy", "Easy"), ("medium", "Medium"), ("hard", "Hard")])
     level = models.CharField(max_length=3, choices=LEVEL_CHOICES, default="KS2")  # KS2 or KS3
     topic = models.CharField(max_length=255)  # E.g., "Fractions", "Algebra"

     def __str__(self):
         return f"{self.title} ({self.difficulty})"
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1, choices=[("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")
        ])
    def __str__(self):
        return f"Question: {self.text[:50]}..."


class Progress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    topics_practiced = models.TextField(blank=True)  # This stores a list of topics that has been practiced by students.
    acquired_skills = models.TextField(blank=True)
    mastered_skills = models.TextField(blank=True)
    def __str__(self):
        return f"Progress for {self.user.username}"
class Badge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date_awarded = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name} - {self.user.username}"




