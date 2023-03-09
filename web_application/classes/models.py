from django.db import models
from django.contrib.auth.models import User

from portals.models import Portal

class Class(models.Model):
    name = models.TextField(blank=False, null=False, max_length=100)
    portal = models.ForeignKey(Portal, on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(blank=False, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False, related_name='created_by')
    assigned_teacher = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='assigned_teacher')
    

    class Meta:
            verbose_name_plural = "Classes"
            db_table = "classes"

class Student(models.Model):
    email = models.EmailField(blank=False, null=False)
    belongs_to_class = models.BooleanField(blank=False, null=False)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE, blank=False, null=False)
    absences = models.IntegerField(blank=False, null=False)

    class Meta:
            verbose_name_plural = "Students"
            db_table = "students"


class StudentGrade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=False, null=False)
    grades = models.TextField(blank=False, null=False) # {'Maths': 1-20, '..' : .. ,}
    average_grade = models.DecimalField(decimal_places=3, max_digits=5, blank=False, null=False)

    class Meta:
            verbose_name_plural = "StudentsGrades"
            db_table = "students_grades"





