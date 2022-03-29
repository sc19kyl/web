from curses.ascii import HT
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Student, Module, Professor, Dep_Mod, Dep_Stud, Department, Rating, Prof_Rating, Prof_Mod
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound
import json
from django.core import serializers

# Create your views here.

cur_user = 0

def index(request):

    
    print("asdasd")
    return render(request, 'main_page.html')

def main_page(request,username):

    user = Student.objects.get(student=request.user)
    print(request.session)
    dep_stud = Dep_Stud.objects.get(student = user)

    modules = Dep_Mod.objects.filter(department = dep_stud.department)
    #user2 = User.objects.get(pk=4)
    #professor = Professor.objects.get(professor=user2)
    #prof_rating = Prof_Rating.objects.filter(professor=professor)
    

    context = {
        'modules' : modules,
    }

    print(modules)
    return render(request, 'main_page.html',context)


def Login(request):

    if request.method == 'POST':
        data = request.POST
        print(data.get('username'))
        print(data.get('password'))
        user = authenticate(username=data.get('username'),password=data.get('password'))
        
        if user != None:
            print(user.id)
            request.session['id'] = user.id
            request.session['username'] = user.username
            login(request,user)
            return redirect(main_page, user.username)
        else:
            return HttpResponseNotFound("user not found")   
            
    if request == 'GET':
        print("we are in get")
    
    print(request.GET)
    return render(request,'login.html')

def register(request):

    if request.method == 'POST':
        data = request.POST
        print(data.get('email'))
        print(data.get('username'))
        print(data.get('password'))
        emailIn = data.get('email')
        usernameIn = data.get('username')
        passwordIn = data.get('password')
        print(emailIn)
        print(usernameIn)
        if (User.objects.filter(email=emailIn).exists() == True):
            print("user exists")
            return HttpResponseNotFound("user already exists")
        else:
            user = User.objects.create_user(email=emailIn,username=usernameIn, password=passwordIn)
            stud = Student(student = user)
            stud.save()
            print("user created")
        return HttpResponse("user created")
    
    if request.method == 'GET':
         return render(request,'login.html')
    
def rating(request):
    
    if request.method == 'POST':
        data = request.POST
        name = data.get('name')
        user2 = User.objects.get(username = name)
        professors = Professor.objects.all()
        rating = []
        if professors.count() > 0:
            
            for p in professors:
                print(p)
                prof_rating = Prof_Rating.objects.filter(professor=p).all()
                rating.append(prof_rating)
            
            print(rating[0][0].module.year)
            context = {
                'rating' : rating,
            }
            return render(request,'rating.html',context)

        else:
            return HttpResponseNotFound("user not found")
        
    if request.method == 'GET':
        return render(request,'ratingform.html')

def average(request):

    if request.method == 'GET':
        return render(request,'average.html')

    if request.method == 'POST':
        
        data = request.POST
        name = data.get('name')
        module = data.get('module_code')
        user = User.objects.get(username = name)
        professor = Professor.objects.get(professor=user)
        module = Module.objects.filter(module_code = module).all()
        total_rating_points = 0
        total_rating = 0
        for m in module:
            ratings = Prof_Mod.objects.filter(professor = professor, module = m).all()
            for rating in ratings:
                print(rating.rating.rating)
                total_rating_points = total_rating_points + int(rating.rating.rating)
                total_rating += 1

        average_rating =  int(total_rating_points/total_rating)
        print(average_rating)
        if average_rating:
            context = {
                "rating" : average_rating
            }
            return HttpResponse(json.dumps(context), content_type="application/json")
        else:
            return HttpResponseNotFound("not found")

def rate(request):
    if request.method == 'GET':
        return render(request, "rateform.html")

    if request.method == 'POST':
        data = request.POST
        year = data.get('year')
        module_code = data.get('module_code')
        semester = data.get('semester')
        module = Module.objects.get(module_code = module_code,year = year,semester=semester)
        if not module:
            return HttpResponseNotFound("module not found")
        name = data.get('name')
        user = User.objects.get(username = name)
        professor = Professor.objects.get(professor = user)
        if not professor:
            return HttpResponseNotFound("professor not found")
        rating = int(data.get('rating'))
        rating = Rating.objects.get(pk = rating)
        prof_rating = Prof_Mod(professor = professor, module = module, rating = rating)
        prof_rating.save()
        print(prof_rating)
        print(request.POST)
        return HttpResponse('found')

def list(request):
    if request.method == 'GET':
        modules = Module.objects.all()
        prof_mod2 = Prof_Mod.objects.all()
        prof_mod = {}
        professors = []
        i = 1     
        for m in modules.iterator():   
            string = "module_" + str(i)
            prof_mod[string] = m.module_name
            string = "year_" + str(i)
            prof_mod[string] = m.year
            string = "semester_" + str(i)
            prof_mod[string] = m.semester
            
            for prof in prof_mod2.iterator():
                if m == prof.module:
                    professors.append(prof.professor.professor.username)
                    pass
            string = "professor_" + str(i)
            prof_mod[string] = professors
            i += 1
            professors = []

        print(prof_mod)
        print(professors)

    return HttpResponse(json.dumps(prof_mod), content_type="application/json")

def view(request):
    
    context = {}

    professors = Professor.objects.all()

    for professor in professors:
        professor_name = professor.professor.username
        total_rating = 0
        prof_ratings = Prof_Mod.objects.filter(professor = professor).all()
        print(len(prof_ratings))
        if len(prof_ratings) == 0:
            average_rating = 0
        else: 
            for prof_rating in prof_ratings:
                print(prof_rating)
                total_rating += prof_rating.rating.rating
            average_rating = int(total_rating/len(prof_ratings))
        context[professor_name] = average_rating
    
    return HttpResponse(json.dumps(context), content_type="application/json")

