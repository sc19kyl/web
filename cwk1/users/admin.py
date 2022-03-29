from django.contrib import admin

# Register your models here.
from .models import Student, Department, Module, Dep_Mod, Dep_Stud, Rating, Prof_Rating, Professor, Prof_Mod

admin.site.register(Student)
admin.site.register(Department)
admin.site.register(Module)
admin.site.register(Dep_Mod)
admin.site.register(Dep_Stud)
admin.site.register(Rating)
admin.site.register(Professor)
admin.site.register(Prof_Rating)
admin.site.register(Prof_Mod)
