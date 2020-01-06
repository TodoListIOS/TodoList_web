from django.core import serializers
from django.shortcuts import render, redirect
import json
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from backend import models,forms


# 网页登录页面
def web_login(request):
    if request.session.get('is_login', None):
        return redirect('homepage')

    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        message = "请检查填写的内容！(验证码)"
        print(123)
        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']
            users = models.Account.objects.filter(email=email)
            if users.count() != 0:
                user = users.first()
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_email'] = user.email
                    request.session['user_name'] = user.name

                    return redirect('homepage')
                else:
                    message = "用户名或密码错误"
            else:
                message = "用户不存在，请先注册"
                return render(request, 'login.html', locals())
        return render(request, 'login.html', locals())

    login_form = forms.UserForm()
    return render(request, 'login.html', locals())


# 登陆认证API接口
def login_api(request):
    if request.method == 'POST':
        input_email = request.POST.get("email", None)
        input_password = request.POST.get("password", None)

        print(input_email)
        print(input_password)
        try:
            user = models.Account.objects.get(Email=input_email, Password=input_password)
            # back_list = []
            # user_data = {'name': user.Name, 'email': user.Email, 'password': user.Password}
            # back_list.append(user_data)
            # response = json.dumps(back_list, ensure_ascii=False)
            return HttpResponse("Pass")
        except ObjectDoesNotExist:
            return HttpResponse("Error")


# 注册API接口
def register_api(request):
    if request.method == 'POST':
        input_email = request.POST.get('email')
        input_name = request.POST.get('name')
        input_password = request.POST.get('password')
        try:
            models.Account.objects.create(Email=input_email, Name=input_name, Password=input_password)
            return HttpResponse("Pass")
        except ObjectDoesNotExist:
            return HttpResponse("Error")


# 密码找回API接口
def password_find_back_api(request):
    pass


# 同步记录API接口
def records_sync_api(request):
    pass


# 连接测试API接口
def json_transfer(request):
    if request.method == "GET":
        try:
            users = models.Account.objects.all()
            user_list = serializers.serialize("json", users)
            response = json.dumps(user_list, ensure_ascii=False)
            print(user_list)
            return HttpResponse(user_list)
            # back_list = []
            # user_data = {'name': user.Name, 'email': user.Email, 'password': user.Password}
            # back_list.append(user_data)
            # response = json.dumps(back_list, ensure_ascii=False)
        except ObjectDoesNotExist:
            return HttpResponse("None")
