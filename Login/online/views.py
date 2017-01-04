#coding=utf-8
import smtplib

import re
from audioop import reverse

from django.core.mail import send_mail
from django.core.mail import BadHeaderError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django import forms
from .models import User, Article
import random

#表单
class UserForm(forms.Form):
    reg_email = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'ipt','id':'emailname','placeholder':'Please input email address'}))
    password = forms.CharField(label='',widget=forms.PasswordInput(attrs={'class':'ipt','id':'password','placeholder':'Please input password'}))

class ForgetPwd(forms.Form):
    email = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'ipt', 'id': 'for_pwd_email', 'placeholder': 'Please input email address'}))

class Indenti_code(forms.Form):
    code = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'ipt', 'id': 'for_pwd_email', 'placeholder': 'Please input code'}))

class registForm(forms.Form):
    reg_email = forms.CharField(label='', widget=forms.TextInput(
        attrs={'class': 'ipt', 'id': 'regist_email', 'placeholder': 'Please input email address'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'class': 'ipt', 'id': 'password', 'placeholder': 'Please input password'}))
    password_repeat = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'class': 'ipt', 'id': 'password_repeat', 'placeholder': 'Please input password again'}))

class Set_pass(forms.Form):
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'class': 'ipt', 'id': 'password', 'placeholder': 'Please input password'}))
    password_repeat = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'class': 'ipt', 'id': 'password_repeat', 'placeholder': 'Please input password again'}))

def set_pass(req):
    email = req.session['email']
    error = ''
    if req.method == 'POST':
        uf = Set_pass(req.POST)
        if uf.is_valid():
            password = uf.cleaned_data['password']
            pass_re = uf.cleaned_data['password_repeat']
            user = User.objects(email=email)[0]
            if password == pass_re:
                user.password = password
                user.save()

                return HttpResponseRedirect('/online/login')
            else:
                error = 'two input is wrong'
                return render_to_response('set_password.html', {'uf': uf, 'error': error},
                                      context_instance=RequestContext(req))
    else:
        uf = Set_pass(req.POST)
    return render_to_response('set_password.html', {'uf': uf, 'error': error}, context_instance=RequestContext(req))


# global identi_code    #不能够实现多个向多个用户同时发送验证码，先这样吧
# identi_code=0
#注册
def regist(req):
    error=''
    if req.method == 'POST':
        register = registForm(req.POST)
        if register.is_valid():
      #获得表单数据
            reg_email = register.cleaned_data['reg_email']
            password = register.cleaned_data['password']
            password_repeat = register.cleaned_data['password_repeat']

            if validateEmail(reg_email)==0:
                error="email address is wrong"
                return render_to_response('register.html', {'uf': register, 'error': error},
                                          context_instance=RequestContext(req))

            exist = User.objects.filter(email=reg_email)
            if exist:
                error='email address is registed'
                return render_to_response('register.html', {'uf': register, 'error': error},
                                          context_instance=RequestContext(req))
            elif password_repeat!=password:
                error='Two passwords are not consistent'
                return render_to_response('register.html', {'uf': register, 'error': error},
                                          context_instance=RequestContext(req))
            else:
                user=User(reg_email)
                user.password=password
                user.save()

                uf=UserForm()
                response = HttpResponseRedirect('/online/login/')
                return response
                #return render_to_response('login.html',{'uf':uf},context_instance=RequestContext(req))
    else:
        register=registForm()
    return render_to_response('register.html',{'uf':register,'error':error}, context_instance=RequestContext(req))
    #return render_to_response('register.html')
#登陆
def login(req):
    error=''
    if req.method == 'POST':
        uf = UserForm(req.POST)
        if uf.is_valid():
            #获取表单用户密码
            reg_email = uf.cleaned_data['reg_email']
            password = uf.cleaned_data['password']

            #获取的表单数据与数据库进行比较
            user = User.objects.filter(email=reg_email)
            if user:
                pass
            else:
                error='Email address is not registed'
                return render_to_response('login.html', {'uf': uf, 'error': error}, context_instance=RequestContext(req))
            user = User.objects.filter(email =reg_email,password = password)
            if user:
                #比较成功，跳转index
                response = HttpResponseRedirect('/online/index/')
                #将username写入浏览器cookie,失效时间为3600
                response.set_cookie('username',reg_email,3600)
                return response
            else:
                #比较失败,用户不存在或密码错误，提示用户注册
                error='Password is wrong'
                return render_to_response('login.html', {'uf': uf, 'error': error}, context_instance=RequestContext(req))
    else:
        uf = UserForm()
    return render_to_response('login.html',{'uf':uf,'error':error},context_instance=RequestContext(req))

#登陆成功
def index(request):

    # username = req.COOKIES.get('username','')
    # return render_to_response('Login/base.html')
    username=request.COOKIES.get('username','')
    if username:
        user = User.objects(email=username)[0]
        content = {
            'active_menu': 'homepage',
            'user': user,
        }
        return render(request, 'index.html', content)
    else:
        response = HttpResponseRedirect('/online/login/')
        return response

#退出
def logout(request):
    # # #清理cookie里保存username

    uf = UserForm()
    response = HttpResponseRedirect('/online/login/')
    response.delete_cookie('username')
    return response


def identi_code(req):
    i_code=req.session['code']
    error = ''
    if req.method == 'POST':
        uf = Indenti_code(req.POST)
        if uf.is_valid():
            code = uf.cleaned_data['code']
            if code == i_code:
                return HttpResponseRedirect('/online/set_pass')
            else:
                error = 'code is wrong'
                return render_to_response('identi_code.html', {'uf': uf, 'error': error},
                                      context_instance=RequestContext(req))
    else:
        uf = Indenti_code(req.POST)
    return render_to_response('identi_code.html', {'uf':uf,'error': error}, context_instance=RequestContext(req))

def forgetPwd(req):
    error=''
    if req.method == 'POST':
        uf=ForgetPwd(req.POST)
        if uf.is_valid():
            email = uf.cleaned_data['email']

            if validateEmail(email):
                user = User.objects.filter(email=email)
                if user:
                    pass
                else:
                    error = 'Email address is not registed'
                    return render_to_response('forgetPwd.html', {'uf': uf, 'error': error},
                                              context_instance=RequestContext(req))
                try:
                    identi_code = random.randint(100000,999999)

                    send_mail('Note identifying code','Identifying code is '+str(identi_code),'Lxiaoyouling@163.com',[email,],fail_silently=False)
                    req.session['email']=email
                    req.session['code']=str(identi_code)
                    return HttpResponseRedirect('/online/identical_code')
                except BadHeaderError:
                    pass
                    error = 'Send email failed'
                    return render_to_response('forgetPwd.html', {'uf': uf, 'error': error},
                                              context_instance=RequestContext(req))
            else:
                error = 'Email address is novalid'
            return render_to_response('forgetPwd.html',{'uf':uf,'error':error},context_instance=RequestContext(req))
    else:
        uf = ForgetPwd()
    return render_to_response('forgetPwd.html',{'uf':uf}, context_instance=RequestContext(req))

#判断邮箱的合法性
def validateEmail(email):
    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return 1
    return 0

def article_list(request):
    username = request.COOKIES.get('username', '')
    user = User.objects(email=username)[0]
    article = Article.objects(author=username)
    category_list = article.values_list('category').distinct('category')
    query_category = request.GET.get('category', '')
    if (not query_category) or Article.objects.filter(category=query_category).count() is 0:
        query_category = 'all'
        articleList = Article.objects.filter(author=username)
    else:
        articleList = Article.objects.filter(category=query_category,author=username)

    if request.method == 'POST':
        keyword = request.POST.get('keyword', '')
        articleList = article.filter(title__contains=keyword)
        query_category = 'all'

    paginator = Paginator(articleList, 5)
    page = request.GET.get('page')
    try:
        articleList = paginator.page(page)
    except PageNotAnInteger:
        articleList = paginator.page(1)
    except EmptyPage:
        articleList = paginator.page(paginator.num_pages)
    content = {
        'user': user,
        'active_menu': 'view_book',
        'category_list': category_list,
        'query_category': query_category,
        'article_list': articleList,
    }
    return render(request, 'article_list.html', content)

def detail(request):
    username = request.COOKIES.get('username', '')
    user = User.objects(email=username)[0]
    book_id = request.GET.get('id', '')
    if book_id == '':
        return HttpResponseRedirect(reverse('view_book_list'))
    try:
        book = Article.objects.get(pk=book_id)
    except Article.DoesNotExist:
        return HttpResponseRedirect(reverse('view_book_list'))
    content = {
        'user': user,
        'active_menu': 'view_book',
        'book': book,
    }
    return render(request, 'detail.html', content)

def add_article(request):
    user = request.COOKIES.get('username', '')
    state = None
    if request.method == 'POST':
        new_book = Article(
                title=request.POST.get('name', ''),
                author=user,
                category=request.POST.get('category', ''),
                weather=request.POST.get('weather', ''),
                content=request.POST.get('content', ''),
        )
        new_book.save()
        state = 'success'
    content = {
        'user': user,
        'active_menu': 'add_article',
        'state': state,
    }
    return render(request, 'add_article.html', content)

def add_img(request):
    username = request.COOKIES.get('username', '')
    user = User.objects(email=username)[0]
    state = None
    if request.method=='POST':

        user.image=request.FILES.get('img','')
        user.save()
        state='success'
    content = {
        'user': user,
        'state':state,
        'book_list':Article.objects.all(),
        'active_menu':'add_img',
    }
    return render(request, 'add_img.html', content)

def modify_name(request):
    username = request.COOKIES.get('username', '')
    state = None

    if username:
        user = User.objects(email=username)[0]
        if request.method == 'POST':
            user.name = request.POST.get('name','')
            user.save()
            state = 'success'
            content = {

                'state': state,

            }
            return render(request, 'modify_name.html', content)
        else:
            state='error'
    else:
        state = 'error'
    return render(request, 'modify_name.html')

def modify_passwd(request):
    error = ''
    if request.method == 'POST':
        modify_pass = registForm(request.POST)
        if modify_pass.is_valid():
            # 获得表单数据
            old_passwd = modify_pass.cleaned_data['reg_email']
            password = modify_pass.cleaned_data['password']
            password_repeat = modify_pass.cleaned_data['password_repeat']

            username = request.COOKIES.get('username', '')
            user = User.objects(email=username)[0]

            if old_passwd!=user.password:
                error = "old password is wrong"
                return render_to_response('modify_passwd.html', {'uf': modify_pass, 'error': error},
                                          context_instance=RequestContext(request))
            elif password!=password_repeat:
                error = "two password is wrong"
                return render_to_response('modify_passwd.html', {'uf': modify_pass, 'error': error},
                                          context_instance=RequestContext(request))
            else:
                user.password = password
                user.save()

                uf = UserForm()
                response = HttpResponseRedirect('/online/index/')
                return response
                # return render_to_response('login.html',{'uf':uf},context_instance=RequestContext(req))
    else:
        modify_pass = registForm()
    return render_to_response('modify_passwd.html', {'uf': modify_pass, 'error': error}, context_instance=RequestContext(request))