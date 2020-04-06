from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

# from rest_framework.authtoken.models import Token

# for user in User.objects.all():
#     Token.objects.get_or_create(user=user)

# 토큰추가
# from django.core import serializers
# from django.http import HttpResponse
# from rest_framework.decorators import api_view, permission_classes, authentication_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# from .models import Post

# @api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
# @authentication_classes((JSONWebTokenAuthentication,))
# def posts(request):
#     posts = Post.objects.filter(
#         published_at__isnull=False).order_by('-published_at')
#     post_list = serializers.serialize('json', posts)
#     return HttpResponse(post_list, content_type="text/json-comment-filtered")

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

# def profile(request):
#     if not request.user.is_authenticated:
#         data = {'username': request.user, 'is_authenticated': request.user.is_authenticated}
#     else:
#         data = {'last_login': request.user.last_login, 'username': request.user.username,
#                 'password': request.user.password, 'is_authenticated': request.user.is_authenticated}
#     return render(request, 'profile.html', context={'data': data})
# Create your views here.

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