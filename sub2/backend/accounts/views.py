from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import View
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# from django.contrib import auth
from django.http import HttpResponseRedirect
from backend import settings
# from django.contrib.auth.mixins import LoginRequiredMixin

class IndexView(View):
    def get(self, request, *args, **kwargs):
        context = {'parm1': 'hello', 'parm2': 'django', 'auth': request.user.is_authenticated}
        print(request.user)
        return render(request, 'index.html', context=context)

@login_required
def profile(request):
    data = {'last_login': request.user.last_login, 'username': request.user.username,
            'password': request.user.password, 'is_authenticated': request.user.is_authenticated}
    return render(request, 'profile.html', context={'data': data})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(settings.LOGIN_URL)
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup_form.html', { 'form' : form })

# def login(request):
#     if request.method == "POST":
#         username=request.POST["username"]
#         password=request.POST["password"]
#         user = auth.authenticate(
#             request,
#             username=username,
#             password=password)
        
#         if user is not None:
#             auth.login(request, user)
#             save_session(request, username, password)
#             return HttpResponseRedirect("../success")
#         else:
#             return render(request, "login.html", {"error":"username or password is incorrect"})
#     else:
#         return render(request, "login.html")

# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect("../../")

# def home(request):
#     return render(request, "home.html")

# def success(request):
#     return render(request, "success.html")

# def joinsuccess(request):
#     return render(request, "joinsuccess.html")

# def save_session(request, username, password):
#     request.session['username'] = username
#     request.session['password'] = password

# def profile(request):
#     if not request.user.is_authenticated:
#         data = {'username': request.user, 'is_authenticated': request.user.is_authenticated}
#     else:
#         data = {'last_login': request.user.last_login, 'username': request.user.username,
#                 'password': request.user.password, 'is_authenticated': request.user.is_authenticated}
#     return render(request, 'profile.html', context={'data': data})
# Create your views here.