# coding: utf8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from books.forms import RegisterForm, LoginForm, ProfileForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
# Create your views here.


def test(request):
    return render(request, 'test.html')


def index(request):
    return render(request, 'index.html')


def login_validate(request, username, password):
    rtvalue = False
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            return True
    return rtvalue    


def login(request):
    error = []
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            password = data['password']
            if login_validate(request, username, password):
                return HttpResponseRedirect("/home/")  # 登录成功则跳转
            else:
                error.append('密码不正确')
        else:
            error.append('请输入用户名和密码')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'error': error, 'form': form})


def home(request):
    return render(request, 'home.html')


def register(request):
    error = []
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            email = data['email']
            password = data['password']
            password2 = data['password2']
            if not User.objects.all().filter(username=username):
                if form.pwd_validate(password, password2):
                    user = User.objects.create_user(username, email, password)
                    user.save()
                    login_validate(request, username, password)
                    return HttpResponseRedirect("/home/")  # 注册成功则跳转
                else:
                    error.append('请输入相同密码')
            else:
                error.append('该用户已存在，更换用户名')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form, 'error': error})


@login_required()
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')


@login_required
def profile(request):
    form = ProfileForm(instance=request.user.get_profile())
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = request.user.get_profile()
            profile.nick = form.cleaned_data['nick']
            profile.use_gravatar = form.cleaned_data['use_gravatar']
            profile.save()
    return render(request, 'profile.html', {
        'form': form,
    })