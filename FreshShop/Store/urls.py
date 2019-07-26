from django.urls import path,re_path
from Store.views import *

urlpatterns = [
    path('register/',register),
    path('login/',login),
    path('index/', index),
    path('ajax_test/', ajax_test),
    path('store_register/',store_register),
    path('add_goods/', add_goods),
    re_path(r'list_goods/(?P<state>\w+)/', good_list),
    path('add/', add),
    path('goods_verbose/',goods_verbose),
    path('goods_update/', goods_update),
    path('quit/', quit),
    re_path(r'set_good/(?P<state>\w+)/', set_good),
    path('goods_style/', goods_style),
    path('delete_goodtype/', delete_goodtype),
    path('modify_goodtype/', modify_goodtype),
    path('goodtype_verbose/', goodtype_verbose),
]

urlpatterns += [
    path('base/',base)
]