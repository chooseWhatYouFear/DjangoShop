from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect

from Buyer.models import *
from Store.models import *
from Store.views import set_password

from alipay import AliPay

def loginValid(fun):
    def inner(request,*args,**kwargs):
        cookie = request.COOKIES.get('username')
        session = request.session.get('username')
        if cookie and session and cookie==session:
            return fun(request,*args,**kwargs)
        else:
            return HttpResponseRedirect('/buyer/login')
    return inner
# Create your views here.
@loginValid
def index(request):
    result = []
    goodtype_list = GoodsType.objects.all()
    for goodstype in goodtype_list:
        goods_list = goodstype.goods_set.values()[:4]
        if goods_list:
            goods_type = {
                "type_id":goodstype.id,
                'type_name':goodstype.type_name,
                'description':goodstype.description,
                'type_image':goodstype.type_image,
                'goods_list':goods_list
            }
            result.append(goods_type)
    return render(request,'buyer/index.html',locals())


def register(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        buyer = Buyer()
        buyer.username = username
        buyer.password = set_password(password)
        buyer.email = email
        buyer.save()
        return HttpResponseRedirect('/buyer/login')
    return render(request,'buyer/register.html')

def login(request):
    if request.method=="POST":
        print(123)
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            print(123)
            user = Buyer.objects.filter(username=username).first()
            if user and set_password(password)==user.password:
                response = HttpResponseRedirect('/buyer/index')
                response.set_cookie('username',username)
                response.set_cookie('user_id',user.id)
                request.session['username'] = username
                return response
    return render(request,'buyer/login.html')

def logout(request):
    response = HttpResponseRedirect('/buyer/login')
    for cookie in request.COOKIES:
        response.delete_cookie(cookie)
    return response

# 商品列表
def goods_list(request):
    type_id = request.GET.get('type_id')
    goodstype = GoodsType.objects.filter(id=type_id).first()
    if goodstype:
        goods = goodstype.goods_set.filter(goods_status=1)

    return render(request,'buyer/goods_list.html',locals())


# 支付宝支付
def aliPay(request):
    money = request.GET.get('money')
    order = request.GET.get('order')

    alipay_public_key_string = """-----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEApFw2Wx6Ps96xw8cT4NuFK4xqsWZpUmdBNmhF2OEneOz7bY0fzLnJUJ/XjHzuf/VpzwAC9tOikwcytJBYQAYid3qADb2HaLg4k5jHriIojxk8Ld9gbkPYFzz9hQEnLKIBIeYDrRcQlG4laC4g8dA4TDig0oLF3MMvbBOrTZZG/BAKt+pXvynhSBbm9HKFx4l/4zvDRxIkg9BEeXLGie+P4QRW/J0nDXtK3zi3dY1i6+5xP7x01dnxHv6/Q22kWO4kqG6NJ6xcAGl2NMkKWgcbqNLwNHCaRmocQAV2m+mXF8HT5ha4NxTg4PZAzj9HLRk2I/9/YYS5pDXKx/Gs2ERTQwIDAQAB
    -----END PUBLIC KEY-----"""

    app_private_key_string = """-----BEGIN RSA PRIVATE KEY-----
    MIIEowIBAAKCAQEApFw2Wx6Ps96xw8cT4NuFK4xqsWZpUmdBNmhF2OEneOz7bY0fzLnJUJ/XjHzuf/VpzwAC9tOikwcytJBYQAYid3qADb2HaLg4k5jHriIojxk8Ld9gbkPYFzz9hQEnLKIBIeYDrRcQlG4laC4g8dA4TDig0oLF3MMvbBOrTZZG/BAKt+pXvynhSBbm9HKFx4l/4zvDRxIkg9BEeXLGie+P4QRW/J0nDXtK3zi3dY1i6+5xP7x01dnxHv6/Q22kWO4kqG6NJ6xcAGl2NMkKWgcbqNLwNHCaRmocQAV2m+mXF8HT5ha4NxTg4PZAzj9HLRk2I/9/YYS5pDXKx/Gs2ERTQwIDAQABAoIBADhx/qzeWwWvxibxOI9xdFOXXpDcFfGZyliQCOTJtk+eO17NJ42chFmu+0yhHxtMwfC4FUyFNAEAaNZ/9/7M3Ithw5Z0b4t0MOHnhzPzQTCbvwIWA7z6iby5UmuaEMUQQglNQBfyotwG08vqg5/oHV132StSg/ckBSY9vwffQzOPFbwXR6uPE/6E/wAL+ozhlvqftimCObfwrrGgfHpnH0StmDIxNKF8ZGFbpiMKUt43p2PPo6Oq7m9YEDqJhE4aRCEtNOQwA8Kv+nGQAHWmySd+L3Zj0xeuv8c/Y2WZuB/soxace8uc2ecppYGWl6ZqpBcDw7ZKqKpelt3z2nhcIIkCgYEA19lKhoI0fmiW+Pkry6WdoeizAa+yhMWtg6e7O/qp/v9P4z2n1hAG60H4+P/65u0JwoVIlTQ3mRIwyJKzddOQ8XQwsxmBgnYJRglTTBlG3qwIZ/YFmya6kwMfMUDUcYn7tH3mv4iM4nXfmHRbl2X1TBiWSX8PhakyL1IxIxVcpIUCgYEAwu8Jgm2Hhww2Q54iA/+XoY5nIAGglGaVa8sShcii9qwICvgHld1VXmw8sKeLnYg7Nflf5TCc/Ep4UgqZGInz5/Jy/c+8OXloiQ2kmtN8uRPGTS6mZhPeoa5g3dPdRKev6J1Mb78HI/y9op2n718EZt6QYu/0b473oKP1GuTrJycCgYBQ+nFOM00UW5LAR2LZ3QFde9qkeFEGJM9rBCNnZiwewZQsEbaExbCC1FZevFJaDnXJ540KhPOS1tM8fGUdgEjxfQDEQH5o/nWOM/NvKlB/O5VPw2npAkee3d328XaCPh0TYuSN2OHaGBTRsl2mWBcF/HdtjWC6aXatcC2FFv+RrQKBgBeDP7FkxsEqXu0/CLlUvhR1mcjJiXX8/a732q8aaVW5oGq6Sifwf5iZE6T3QKbqxMGY59E8UOM5lFPJBXhpQ2tJ2kb1JK4GD+7gH2exdMzaLsQmiVmsseDsqLB5GqpqU5SKTKr57sGPfcw8mgIMgvpphB769I/0Pbg5rpnk3NxnAoGBAMD4eSoN9u3ATldCzIBHsPQzoJYUmpCdEVMmU4fL3ggwlloNFd9dzC1z6QsNKKbd/HBwGZkbvf2LMVGfpUvQJPrOZHT9aJMJzcdM6BymI5B/zfn1RHZA+6dGVGQDry1yME6+U8mixyRHIeRWSCu2QcLNRihJVOY9iDHsWAHSGB5o
    -----END RSA PRIVATE KEY-----"""

    # 实例化
    alipay = AliPay(
        appid='2016101000652495',
        app_notify_url=None,
        app_private_key_string=app_private_key_string,
        alipay_public_key_string=alipay_public_key_string,
        sign_type='RSA2'
    )

    # 发起支付请求
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no = order,
        total_amount = money,
        subject = "生鲜交易",
        return_url = '/',
        notify_url = None
    )

    return HttpResponseRedirect('https://openapi.alipaydev.com/gateway.do?' + order_string)
