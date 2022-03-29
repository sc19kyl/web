from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Student(models.Model):
    student = models.OneToOneField(User,on_delete=models.CASCADE)
    is_student = 1
    is_professor = 0
    
    def __str__(self):
        return self.student.username
    
class Professor(models.Model):
    professor = models.OneToOneField(User,on_delete=models.CASCADE)
    is_student = 0
    is_professor = 1

    def __str__(self):
        return self.professor.username

def create_module_code(strIn):
    code = ""
    for i in strIn:
        if i.isupper():
            code += i
    return code

class Module(models.Model):
    module_id = models.AutoField(primary_key=True)
    module_name = models.CharField(max_length=100,default='')
    module_code = models.CharField(max_length = 10)
    semester_choices = {
        ("1", "1"),
        ("2", "2"),
    }
    semester = models.CharField(
        max_length = 1,
        choices = semester_choices,
        default = '1'
        )
    year = models.IntegerField(default=0)

    def __str__(self):
        return self.module_name + '_' + str(self.year)

class Department(models.Model):
    dep_id = models.AutoField(primary_key=True)
    dep_name = models.CharField(max_length=100,default='')

    def __str__(self):
        return self.dep_name

class Dep_Mod(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE,default="")
    department = models.ForeignKey(Department, on_delete=models.CASCADE,default="")

    def __str__(self):
        return self.module.module_name + "_" + self.department.dep_name

class Dep_Stud(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE,default="")
    department = models.ForeignKey(Department, on_delete=models.CASCADE,default="")

    def __str__(self):
        return self.student.student.username + "_" + self.department.dep_name

class Rating(models.Model):
    rating = models.IntegerField(default=0)
    def __str__(self):
        return str(self.rating)

class Prof_Rating(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE,default="")
    module = models.ForeignKey(Module,on_delete=models.CASCADE, default="" )
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE,default="")
    rating_choices = {
        ("1","1"),
        ("2","2"),
        ("3","3"),
        ("4","4"),
        ("5","5"),
    }
    rating2 = models.CharField(
        max_length=1,
        choices=rating_choices,
        default='1',
    )
    def __str__(self):
        return self.professor.professor.username + "_" + self.module.module_name + "_" + str(self.module.year) + "_" + str(self.rating.rating)

class Prof_Mod(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE,default="")
    module = models.ForeignKey(Module,on_delete=models.CASCADE, default="" )
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE,default="")
    def __str__(self):
        return self.professor.professor.username + "_" + self.module.module_name  + '_' + str(self.module.year)

