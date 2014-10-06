# coding: utf8
from django.shortcuts import render
from books.forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
# Create your views here.

def test(request):
    return render(request, 'test.html')

def index(request):
    return render(request, 'index.html')

def login(request):
    error = []
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            password = data['password']
            if login_validate(request, username, password):
                return HttpResponseRedirect("/home/") #登录成功则跳转
            else:
                error.append('密码不正确')
        else:
             error.append('请输入用户名和密码')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'error': error, 'form': form})


def login_validate(request, username, password):
    rtvalue = False
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            return True
    return rtvalue

def home(request):
    return render(request, 'home.html')

def register(request):
  error=[]
  if request.method == 'POST':
    form = RegisterForm(request.POST)
    if form.is_valid():
      data = form.cleaned_data
      username = data['username']
      email = data['email']
      password = data['password']
      password2= data['password2']
      if not User.objects.all().filter(username=username):
        if form.pwd_validate(password, password2):
          user = User.objects.create_user(username, email, password)
          user.save()
          login_validate(request,username,password)
          return HttpResponseRedirect("/home/") #注册成功则跳转
        else:
          error.append('请输入相同密码')
      else:
        error.append('该用户已存在，更换用户名')
  else:
    form = RegisterForm()
  return render(request, 'register.html',{'form':form,'error':error})


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')