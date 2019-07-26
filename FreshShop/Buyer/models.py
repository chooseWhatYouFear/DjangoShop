from django.db import models

# Create your models here.
class Buyer(models.Model):
    username = models.CharField(max_length=32,verbose_name='用户名')
    password = models.CharField(max_length=32,verbose_name='密码')
    email = models.EmailField(verbose_name='邮箱')
    phone = models.IntegerField(verbose_name='联系电话',null=True,blank=True)
    connect_address = models.TextField(verbose_name='联系地址',null=True,blank=True)


class Adress(models.Model):
    address = models.TextField(verbose_name='收货地址')
    receiver = models.CharField(max_length=32,verbose_name='接收人')
    recv_phone = models.CharField(max_length=32,verbose_name='接收人电话')
    buyer_id = models.ForeignKey(to=Buyer,on_delete=models.CASCADE,verbose_name='用户id')
