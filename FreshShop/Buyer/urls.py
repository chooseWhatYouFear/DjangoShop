from django.urls import path

from Buyer.views import *

urlpatterns = [
    path('index/',index),
    path('register/', register),
    path('login/', login),
    path('logout/', logout),
    path('goods_list/', goods_list),
    path('aliPay/', aliPay),
]
