from django.db import models


# Create your models here.

# 用户信息表，用于登录查找，注册写入，找回修改
class Account(models.Model):
    Email = models.EmailField(unique=True, default='user@empty.com', null=False, max_length=128)
    Name = models.CharField(default='Tom_the_cat', null=False, max_length=128)
    Password = models.CharField(default='I_am_a_idiot', null=False, max_length=128)
    # Auth_code = models.CharField(default='Bust_is_small', null=False, max_length=128)

    class Meta:
        db_table = 'Account'


# 用户记录表，用于记录用户备忘信息
class UserRecords(models.Model):
    pass
