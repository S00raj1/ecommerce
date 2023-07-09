from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,authenticate,login
from .models import Profile
# Create your views here.


def user_login(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        password = request.POST.get('pass1')
        user = authenticate(request,username=uname,password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login')
            messages.error(request,"Id or password doesnot match")
    return render(request,'accounts/login.html')


def user_signup(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        uname = request.POST['uname']
        email = request.POST['email']
        password = make_password(request.POST['password'])
        password1 = make_password(request.POST['password1'])
        if password == password1:
            user = User.objects.create(first_name=fname,last_name=lname,username=uname,email=email,password=password)
            user.save()
            return redirect('login')
        messages.error(request,"Passwords Doesnot match")
    return render(request,'accounts/signup.html')


def user_logout(request):
    logout(request)
    return redirect('home')


def PasswordResetComplete(request):
    return redirect('login')


login_required(login_url = 'login')
def profile(request):
    return render(request,'accounts/profile.html',{'profile' : Profile.objects.filter(user=request.user),})