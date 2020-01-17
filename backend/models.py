from django.db import models

# Create your models here.

# 用户信息表，用于登录查找，注册写入，找回修改
from django.utils import timezone


class Account(models.Model):
    Email = models.EmailField(unique=True, default='user@empty.com', null=False, max_length=128)
    Name = models.CharField(default='Tom_the_cat', null=False, max_length=128)
    Password = models.CharField(default='I_am_a_idiot', null=False, max_length=128)
    Auth_code = models.CharField(default='Bust_is_small', null=False, max_length=128)

    class Meta:
        db_table = 'Account'


# 用户记录表，用于记录用户备忘信息
class UserRecords(models.Model):
    Email = models.EmailField(default='user@empty.com', null=False, max_length=128)
    timestamp = models.CharField(default='Tom_the_cat', null=False, max_length=128)
    detail = models.TextField(default='Tom_the_cat', max_length=150)
    checked = models.BooleanField(default=False)
    sync = models.BooleanField(default=False)
    due = models.CharField(default='Tom_the_cat', null=False, max_length=128)

    class Meta:
        db_table = 'UserRecords'


class BoCExchangeRate(models.Model):
    timestamp = models.CharField(default='Tom_the_cat', null=False, max_length=128)
    rate = models.FloatField(default='530.00', null=False, max_length=64)
    spider_time = models.CharField(default='Tom_the_cat', null=False, max_length=128)

    class Meta:
        db_table = 'BOC_Exchange'


class CEBExchangeRate(models.Model):
    timestamp = models.CharField(default='Tom_the_cat', null=False, max_length=128)
    rate = models.FloatField(default='530.00', null=False, max_length=64)
    spider_time = models.CharField(default='Tom_the_cat', null=False, max_length=128)

    class Meta:
        db_table = 'CEB_Exchange'
