import hashlib

from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import HttpResponseRedirect

from Store.models import *

# Create your views here.
# 装饰器校验
def loginValid(fun):
    def inner(request,*args,**kwargs):
        cookie = request.COOKIES.get('username')
        session = request.session.get('username')
        if cookie and session and cookie==session:
            return fun(request,*args,**kwargs)
        else:
            return HttpResponseRedirect('/store/login')
    return inner

# hash加密
def set_password(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    return md5.hexdigest()

# 注册用户
def register(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = Seller()
            user.username = username
            user.password = set_password(password)
            user.nickname = username
            user.save()
            return HttpResponseRedirect('/store/login')

    return render(request,'store/register.html')

# 注册的ajax校验
def ajax_test(request):
    result = {'status':'error','data':''}
    username = request.GET.get('username')
    if username:
        user = Seller.objects.filter(username=username).first()
        if user:
            result['data'] = '用户名重复'
        else:
            result = {'status':'success','data':'用户名可以使用'}
    else:
        result['data'] = '用户名不能为空'
    return JsonResponse(result)

#登陆
def login(request):
    response = render(request,'store/login.html')
    response.set_cookie('login','login')
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = Seller.objects.filter(username=username).first()
            if user and user.password==set_password(password) and request.COOKIES.get('login')=='login':
                response = HttpResponseRedirect('/store/index')
                response.set_cookie('username',username)
                response.set_cookie('user_id',user.id)
                request.session['username'] = username
                store = Store.objects.filter(user_id=user.id).first()
                if store:
                    response.set_cookie('has_store',store.id)
                else:
                    response.set_cookie('has_store','')
                return response
    return response

# 退出
def quit(request):
    response = HttpResponseRedirect('/store/index')
    print(request.path)
    for cookie in request.COOKIES:
        response.delete_cookie(cookie)
    return response


#主页
@loginValid
def index(request):

    return render(request,'store/index.html',locals())


def base(request):
    return render(request,'store/base.html')

# 店铺注册
@loginValid
def store_register(request):
    type_list = StoreType.objects.all()
    if request.method=="POST":
        post_data = request.POST
        store_name = post_data.get('store_name')
        store_address = post_data.get('store_address')
        store_description = post_data.get('store_description')
        store_logo = request.FILES.get('store_logo')
        store_phone = post_data.get('store_phone')
        store_money = post_data.get('store_money')
        user_id = request.COOKIES.get('user_id')
        type = request.POST.getlist('type')
        store = Store()
        store.store_name = store_name
        store.store_address = store_address
        store.store_description = store_description
        store.store_logo = store_logo
        store.store_phone = store_phone
        store.store_money = store_money
        store.user_id = user_id
        store.save()
        for type in type:
            store_type = StoreType.objects.get(id=type)
            store.type.add(store_type)
        store.save()
        response = HttpResponseRedirect('/store/index')
        response.set_cookie('has_store', store.id)
        return response

    return render(request,'store/store_register.html',locals())

#添加商品
@loginValid
def add_goods(request):
    goodtype = GoodsType.objects.all()
    if request.method=="POST":
        goods = request.POST
        goods_name = goods.get("goods_name")
        goods_price = goods.get("goods_price")
        goods_number = goods.get("goods_number")
        goods_description = goods.get("goods_description")
        goods_date = goods.get("goods_date")
        goods_safeDate = goods.get("goods_safeDate")
        store_id = request.COOKIES.get('has_store')
        goods_image = request.FILES.get('goods_image')
        goodstype_id = goods.get('goodtype')
        good_type = GoodsType.objects.get(id=goodstype_id)

        goods_add = Goods()
        goods_add.goods_name = goods_name
        goods_add.goods_price = goods_price
        goods_add.goods_number = goods_number
        goods_add.goods_description = goods_description
        goods_add.goods_date = goods_date
        goods_add.goods_safeDate = goods_safeDate
        goods_add.goods_image = goods_image
        goods_add.goods_type = good_type
        goods_add.save()
        store_id = Store.objects.get(id=store_id)
        goods_add.store_id.add(store_id)
        goods_add.save()
        return HttpResponseRedirect('/store/list_goods/up')
    return render(request,'store/add_goods.html',locals())

# TODO 下面是添加商品的
def add(request):
    fish = '甜橙、山楂'
    fish_list = fish.split('、')
    for i in fish_list:
        goods_add = Goods()
        goods_add.goods_name = i
        goods_add.goods_price = 1000
        goods_add.goods_number = 123123123
        goods_add.goods_description = '我是%s'%i
        goods_add.goods_date = '2019-7-6'
        goods_add.goods_safeDate = 156
        goods_add.goods_image = 'asdasd'
        goods_add.save()
        store_id = Store.objects.get(id=5)
        goods_add.store_id.add(store_id)
        goods_add.save()
    return HttpResponseRedirect('/store/index')

# 展示商品列表
@loginValid
def good_list(request,state):
    if state == 'up':
        goods_status = 1
    else:
        goods_status = 0
    keyword = request.GET.get('keywords','')
    page_num = request.GET.get('page',1)
    store_id = request.COOKIES.get('has_store')
    store = Store.objects.get(id=store_id)
    if keyword:
        goods = store.goods_set.filter(goods_name__contains=keyword,goods_status=goods_status)
    else:
        goods = store.goods_set.filter(goods_status=goods_status)
    paginator = Paginator(goods,6)
    page = paginator.page(int(page_num))
    page_range = paginator.page_range
    return render(request,'store/good_list.html',locals())


# 商品详情
@loginValid
def goods_verbose(request):
    good_id = request.GET.get('id')
    good_data = Goods.objects.filter(id=good_id).first()
    return render(request,'store/goods_verbose.html',locals())

# 商品修改
@loginValid
def goods_update(request):
    good_id = request.GET.get('id')
    good_data = Goods.objects.filter(id=int(good_id)).first()
    if request.method=="POST":
        goods = request.POST
        goods_name = goods.get("goods_name")
        print(goods_name)
        goods_price = goods.get("goods_price")
        goods_number = goods.get("goods_number")
        goods_description = goods.get("goods_description")
        goods_date = goods.get("goods_date")
        goods_safeDate = goods.get("goods_safeDate")
        goods_image = request.FILES.get('goods_image')
        print(goods_image)

        goods_update = Goods.objects.get(id=good_id)
        if goods_image:
            goods_update.goods_image = goods_image
        goods_update.goods_name = goods_name
        goods_update.goods_price = goods_price
        goods_update.goods_number = goods_number
        goods_update.goods_description = goods_description
        goods_update.goods_date = goods_date
        goods_update.goods_safeDate = goods_safeDate
        goods_update.save()
        return HttpResponseRedirect('/store/goods_verbose/?id='+good_id)
    return render(request,'store/goods_update.html',locals())

# 上架、下架、删除
def set_good(request,state):
    if state == 'up':
        goods_status = 1
    else:
        goods_status = 0
    good_id = request.GET.get('id')
    referer = request.META.get('HTTP_REFERER')
    if good_id:
        good = Goods.objects.filter(id=good_id).first()
        if state=='delete':
            good.delete()
        else:
            good.goods_status = goods_status
            good.save()
    return HttpResponseRedirect(referer)

# 商品类型
def goods_style(request):
    goodType = GoodsType.objects.all()
    if request.method=="POST":
        type_name = request.POST.get('type_name')
        description = request.POST.get('description')
        type_image = request.FILES.get('type_image')

        goodtype = GoodsType()
        goodtype.type_name = type_name
        goodtype.description = description
        goodtype.type_image = type_image
        goodtype.save()
    return render(request,'store/goods_style.html',{'goodType':goodType})

def delete_goodtype(request):
    goodtype_id = request.GET.get('id')
    goodtype = GoodsType.objects.get(id=goodtype_id)
    goodtype.delete()
    return HttpResponseRedirect('/store/goods_style')

def goodtype_verbose(request):
    goodtype_id = request.GET.get('id')
    goodtype = GoodsType.objects.get(id=goodtype_id)
    return render(request,'store/goodtype_verbose.html',locals())


def modify_goodtype(request):
    goodtype_id = request.GET.get('id')
    good_type = GoodsType.objects.get(id=goodtype_id)
    if request.method=="POST":
        type_name = request.POST.get('type_name')
        description = request.POST.get('description')
        type_image = request.FILES.get('type_image')

        good_type.type_name = type_name
        good_type.description = description
        good_type.type_image = type_image
        good_type.save()
        return HttpResponseRedirect('/store/goods_style')
    return render(request,'store/modify_goodtype.html',locals())