from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.
def signup(request):
    if request.method=='POST':
        #user entered info,needs to signup in
        if request.POST.get('password1')==request.POST.get('password2'):
            #if password matches
            try:
                user=User.objects.get(username=request.POST.get('username'))
                #username already taken
                return render(request,'accounts/signup.html',{'error':'User name has been already taken'})
            except User.DoesNotExist:
                user=User.objects.create_user(username=request.POST.get('username'),password=request.POST.get('password1'))
                #authentication grunted
                return redirect('home')
        else:
            #wrong typed password
            return render(request,'accounts/signup.html',{'error':'Wrong password retype!'})
    else:
        #user not entered info till now
           return render(request,'accounts/signup.html')
    
def login(request):
    if request.method=='POST':
        #user entered info,needs to log in
        user=auth.authenticate(username=request.POST.get('username'),password=request.POST.get('password1'))
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            return render(request,'accounts/login.html',{'error':'Username or Password is incorrect!'})
    else:
        #user not entered info till now
        return render(request,'accounts/login.html')
def logout(request):
    if request.method=='POST':
        auth.logout(request)
        #TODO redirect to login
        return redirect('home')
