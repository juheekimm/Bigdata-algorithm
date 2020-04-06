from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponseRedirect

def signup(request):
    if request.method == "POST":
        if request.POST["password1"] == request.POST["password2"]:
            user = User.objects.create_user(
                username=request.POST["username"],password=request.POST["password1"])
            auth.login(request,user)
            return HttpResponseRedirect("../joinsuccess")
        return render(request, "signup.html")
    return render(request, "signup.html")

def login(request):
    if request.method == "POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user = auth.authenticate(
            request,
            username=username,
            password=password)
        
        if user is not None:
            auth.login(request, user)
            save_session(request, username, password)
            return HttpResponseRedirect("../success")
        else:
            return render(request, "login.html", {"error":"username or password is incorrect"})
    else:
        return render(request, "login.html")

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("../../")

def home(request):
    return render(request, "home.html")

def success(request):
    return render(request, "success.html")

def joinsuccess(request):
    return render(request, "joinsuccess.html")

def save_session(request, username, password):
    request.session['username'] = username
    request.session['password'] = password

def profile(request):
    if not request.user.is_authenticated:
        data = {'username': request.user, 'is_authenticated': request.user.is_authenticated}
    else:
        data = {'last_login': request.user.last_login, 'username': request.user.username,
                'password': request.user.password, 'is_authenticated': request.user.is_authenticated}
    return render(request, 'profile.html', context={'data': data})
# Create your views here.
