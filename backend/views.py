from django.core import serializers
from django.shortcuts import render, redirect
import json
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt

from backend import models, forms

from django.utils.http import urlquote
from django.core.mail import send_mail, send_mass_mail, EmailMultiAlternatives
import random


# 网页登录页面
def web_login(request):
    if request.session.get('is_login', None):
        return redirect('homepage')

    if request.method == "POST":
        login_form = forms.LoginForm(request.POST)

        message = "请检查填写的内容！(验证码)"
        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']
            users = models.Account.objects.filter(Email=email)
            if users.count() != 0:
                user = users.first()
                if user.Password == password:
                    request.session['is_login'] = True
                    request.session['user_email'] = user.Email
                    request.session['user_name'] = user.Name

                    return redirect('homepage')
                else:
                    message = "用户名或密码错误"
            else:
                message = "用户不存在，请先注册"
                return render(request, 'login.html', locals())
        return render(request, 'login.html', locals())

    if request.session.get('message', None):
        message = request.session.get('message', None)
        del request.session['message']
    login_form = forms.LoginForm()
    return render(request, 'login.html', locals())


# 网页注册页面
def web_register(request):
    if request.session.get('is_login', None):
        return redirect("homepage")
    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！(验证码)"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'register.html', locals())
            else:
                same_email_user = models.Account.objects.filter(Email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱已被注册！'
                    return render(request, 'register.html', locals())
                # 当一切都OK的情况下，创建新用户

                new_user = models.Account(Name=username, Password=password1, Email=email)
                new_user.save()
                return redirect('web_login')  # 自动跳转到登录页面

    if request.session.get('message', None):
        message = request.session.get('message', None)
        del request.session['message']
    register_form = forms.RegisterForm()
    return render(request, 'register.html', locals())


# 网页主页
def homepage(request):
    if not request.session.get('is_login', None):
        return redirect('web_login')

    if request.method == "GET":
        # announcement = models.Announcement.objects.filter(visible=True)
        return render(request, 'homepage.html', locals())


# 网页登出
def web_logout(request):
    if not request.session.get('is_login', None):  # 原本未登录则无登出
        return redirect("web_login")
    request.session.flush()

    return redirect("web_login")


# 密码找回
def web_password_find_back(request):
    if request.session.get('is_login', None):
        return redirect('homepage')

    if request.method == "POST":
        if "send_code" in request.POST:
            PwdBack = forms.PwdBack(request.POST)
            if PwdBack.is_valid():
                email = PwdBack.cleaned_data['email']
                users = models.Account.objects.filter(Email=email)
                if users.count() != 0:
                    user = users.first()
                    code = random.randint(1000, 9999)
                    try:
                        user = models.Account.objects.get(Email=email)
                        user.Auth_code = code
                        user.save()
                    except ObjectDoesNotExist:
                        message = "Ops,Something wrong! try again pls!"
                        PwdBack = forms.PwdBack()
                        return render(request, 'pwdback_email_input.html', locals())
                    text = "您的密码找回验证码为：" + str(code)
                    res = send_mail('验证码',
                                    text,
                                    'buct_dongwu@163.com',
                                    [email])
                    if res == 1:
                        message = "密码找回验证码已发送至您的邮箱"
                        AuthCode = forms.AuthCode()
                        return render(request, 'pwdback_email_authcode.html', locals())
                    else:
                        message = "Ops,Something wrong! try again pls!"
                        PwdBack = forms.PwdBack()
                        return render(request, 'pwdback_email_input.html', locals())
                else:
                    message = "用户不存在，请先注册!"
                    request.session['message'] = message
                    return redirect('web_register')
            message = "input error"
            PwdBack = forms.PwdBack()
            return render(request, 'pwdback_email_input.html', locals())
        elif "input_code" in request.POST:
            AuthCode = forms.AuthCode(request.POST)
            if AuthCode.is_valid():
                email = request.POST["input_code"]
                input_AuthCode = AuthCode.cleaned_data['AuthCode']
                newpwd1 = AuthCode.cleaned_data['password1']
                newpwd2 = AuthCode.cleaned_data['password2']
                if newpwd1 != newpwd2:  # 判断两次密码是否相同
                    message = "两次输入的密码不同！"
                    AuthCode = forms.AuthCode()
                    return render(request, 'pwdback_email_authcode.html', locals())
                else:
                    user = models.Account.objects.get(Email=email)
                    if user.Auth_code != input_AuthCode:
                        message = "验证码错误！"
                        AuthCode = forms.AuthCode()
                        return render(request, 'pwdback_email_authcode.html', locals())
                    else:
                        user.Password = newpwd1
                        user.save()
                        message = "密码找回成功！"
                        request.session['message'] = message
                        return redirect('web_login')

    PwdBack = forms.PwdBack()
    return render(request, 'pwdback_email_input.html', locals())


# 登陆认证API接口
@csrf_exempt
def login_api(request):
    if request.method == 'POST':
        input_email = request.POST.get("email", None)
        input_password = request.POST.get("password", None)

        print(input_email)
        print(input_password)
        try:
            user = models.Account.objects.get(Email=input_email, Password=input_password)
            back_list = []
            user_data = {'name': user.Name, 'email': user.Email, 'password': user.Password}
            back_list.append(user_data)
            response = json.dumps(back_list, ensure_ascii=False)
            return HttpResponse(response)
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
            back_list = [{'state': "pass"}]
            response = json.dumps(back_list, ensure_ascii=False)
            return HttpResponse(response)
        except ObjectDoesNotExist:
            back_list = [{'state': "error"}]
            response = json.dumps(back_list, ensure_ascii=False)
            return HttpResponse(response)


# 密码找回API接口
def password_find_back_api(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # 值1：  邮件标题   值2： 邮件主体
        # 值3： 发件人      值4： 收件人
        emaillist = [email]
        code = random.randint(1000, 9999)
        text = "您的密码找回验证码为：" + str(code)
        res = send_mail('验证码',
                        text,
                        'buct_dongwu@163.com',
                        emaillist)
        if res == 1:
            return HttpResponse('processed')
        else:
            return HttpResponse('Error')


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


def web_feed_back(request):
    if request.method == "GET":
        if not request.session.get('is_login', None):
            return redirect('login')
        user = models.Account.objects.get(Email=request.session.get('user_email', None))
        fb = forms.FeedBack()
        return render(request, 'feedback.html', locals())
    else:
        fb = forms.FeedBack(request.POST)
        if fb.is_valid():
            text = fb.cleaned_data['text']
            # 值1:邮件标题 值2：邮件主体 值3:发件人 值4：收件人
            user_name = request.session.get('user_name', None)
            user_email = request.session.get('user_email', None)
            foot = user_name + "\t" + user_email + "\t"
            text = text + "\n" + foot
            res = send_mail('反馈信息',
                            text,
                            'buct_dongwu@163.com',
                            ['18811610600@163.com'])

            if res == 1:
                message = "提交成功！谢谢"
                fb = forms.FeedBack()
                return render(request, 'feedback.html', locals())
            else:
                message = "提交失败！反馈邮件程序错误"
                fb = forms.FeedBack()
                return render(request, 'feedback.html', locals())
