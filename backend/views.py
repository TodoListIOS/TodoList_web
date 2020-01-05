from django.core import serializers
from django.shortcuts import render
import json
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from backend import models


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
