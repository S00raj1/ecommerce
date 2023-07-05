from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout,authenticate,login
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
        
    return render(request,'accounts/login.html')


def user_signup(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        uname = request.POST['uname']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        if password == password1:
            user = User.objects.create(first_name=fname,last_name=lname,username=uname,email=email,password=password)
            user.save()
            return redirect('login')
    return render(request,'accounts/signup.html')


def user_logout(request):
    logout(request)
    return redirect('home')


def forgotPassword(request):
    pass
