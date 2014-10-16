# coding: utf8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from books_app.forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django import forms
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from models import *
from forms import *
from models import Book


def index(request):  # 用户未登录时的页面
    list_items = Book.objects.all()
    paginator = Paginator(list_items, 6)
    #return render(request, 'index.html')
    # 采用重定向方法
    t = get_template('index.html')
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))


def login_validate(request, username, password):  # 判断用户是否登陆
    rtvalue = False
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            return True
    return rtvalue


def login(request):  # 用户登陆
    error = []
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            password = data['password']
            if login_validate(request, username, password):
                # return HttpResponseRedirect("/home/")  # 登录成功则跳转
                return HttpResponseRedirect("/books/")  # 登录成功则跳转
            else:
                error.append('密码不正确')
        else:
            error.append('请输入用户名和密码')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'error': error, 'form': form})


def list_book(request):  # 用户登录后显示书
    list_items = Book.objects.all()
    paginator = Paginator(list_items, 10)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        list_items = paginator.page(page)
    except:
        list_items = paginator.page(paginator.num_pages)

    t = get_template('books_app/list_book.html')
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))


def create_book(request):  # 用户可以创建书
    form = BookForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = BookForm()

    t = get_template('books_app/create_book.html')
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))


def view_book(request, id):  # 用户可以产看书的详细信息
    book_instance = Book.objects.get(id=id)

    t = get_template('books_app/view_book.html')
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))


def edit_book(request, id):  # 用户可以对书进行编辑
    book_instance = Book.objects.get(id=id)

    form = BookForm(request.POST or None, instance=book_instance)

    if form.is_valid():
        form.save()

    t = get_template('books_app/edit_book.html')
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))


def wereview(request):  # 显示书评
    t = get_template('wereview.html')
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))


def booklist(request):  # 显示书评
    t = get_template('mybooklist.html')
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))


def home(request):
    return render(request, 'home.html')


def register(request):  # 用户注册
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
                    return HttpResponseRedirect("/books/")  # 注册成功则跳转
                else:
                    error.append('请输入相同密码')
            else:
                error.append('该用户已存在，更换用户名')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form, 'error': error})


@login_required()
def logout(request):  # 用户注销
    auth_logout(request)
    return HttpResponseRedirect('/')