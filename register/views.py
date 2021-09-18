from django.http.response import HttpResponseRedirect
from django.shortcuts import render , HttpResponse ,get_object_or_404  ,  redirect
from django.urls import reverse 
from django.contrib.auth import authenticate, login, logout
from django.db.models import Value, Count, CharField
from .forms import *
from .models import *

def info(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("register:login"))
    
    img = Student.objects.get(user = request.user)

    return render(request, "registers/userinfo.html",{
        "image" : img
    })

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("register:login"))

    registered_subject_seat = []
    unregister_subject_seat = []

    current_subject = Student.objects.get(user = request.user).subject.all()
    #ใช้__inถ้าเราส่งมาเป็นquery set
    other_subject = Subject.objects.exclude(pk__in = current_subject)

    for seat in current_subject:
        registered_subject_seat.append(seat.max_seat - seat.subject.all().count())
        
    for seat in other_subject:
        unregister_subject_seat.append(seat.max_seat - seat.subject.all().count())

    return render(request , "registers/index.html", {
        "subjects" : current_subject,
        "other_subject" : other_subject,
        "user_seat" : registered_subject_seat,
        "other_seat" : unregister_subject_seat,

        
    })
    
def login_view(request):
    if request.method == "POST":
        user = request.POST["username"]
        passw = request.POST["password"]
        user = authenticate(request , username=user, password = passw)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("register:info"))
        else:
            return render(request, "registers/login.html", {
                "message": "Invalid credentials"
            })
    return render(request, "registers/login.html")

def logout_view(request):
    logout(request)
    return render(request, "registers/login.html",{
        "message" : "Logged out."
    })

def subject_info(request , subject_id):
    this_subject = get_object_or_404(Subject, pk= subject_id)
    current_subject = Student.objects.get(user = request.user).subject.all()
    current_seat = this_subject.subject.count()
    maxseat = this_subject.max_seat
    check_seat = maxseat - current_seat > 0
    if this_subject in current_subject :
        check = True
    else:
        check = False
    return render(request , "registers/subjectinfo.html", {
        "subject" : this_subject,
        "user_registered" : check,
        "check_seat" : check_seat,
        "current_seat" : current_seat,
    })

def enroll(request , subject_id):
    if request.method == "POST":
        select_subject = Subject.objects.get(pk = subject_id)
        student = Student.objects.get(user = request.user)
        student.subject.add(select_subject)
    return HttpResponseRedirect(reverse("register:index"))

def unenroll(request , subject_id):
    if request.method == "POST":
        select_subject = Subject.objects.get(pk = subject_id)
        student = Student.objects.get(user = request.user)
        student.subject.remove(select_subject)
    return HttpResponseRedirect(reverse("register:index"))

# Create your views here.

def upload(request):
  
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES ) 
  
        if form.is_valid():
            image = form.cleaned_data['image']
            a = Student.objects.get(user = request.user)
            a.img = image
            a.save()
            return HttpResponseRedirect(reverse("register:info"))
    else:
        form = ImageForm()

    return render(request, 'registers/upload.html', {'form' : form})
  

