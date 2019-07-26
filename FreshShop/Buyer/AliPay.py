from alipay import AliPay

alipay_public_key_string = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEApFw2Wx6Ps96xw8cT4NuFK4xqsWZpUmdBNmhF2OEneOz7bY0fzLnJUJ/XjHzuf/VpzwAC9tOikwcytJBYQAYid3qADb2HaLg4k5jHriIojxk8Ld9gbkPYFzz9hQEnLKIBIeYDrRcQlG4laC4g8dA4TDig0oLF3MMvbBOrTZZG/BAKt+pXvynhSBbm9HKFx4l/4zvDRxIkg9BEeXLGie+P4QRW/J0nDXtK3zi3dY1i6+5xP7x01dnxHv6/Q22kWO4kqG6NJ6xcAGl2NMkKWgcbqNLwNHCaRmocQAV2m+mXF8HT5ha4NxTg4PZAzj9HLRk2I/9/YYS5pDXKx/Gs2ERTQwIDAQAB
-----END PUBLIC KEY-----"""


app_private_key_string = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEApFw2Wx6Ps96xw8cT4NuFK4xqsWZpUmdBNmhF2OEneOz7bY0fzLnJUJ/XjHzuf/VpzwAC9tOikwcytJBYQAYid3qADb2HaLg4k5jHriIojxk8Ld9gbkPYFzz9hQEnLKIBIeYDrRcQlG4laC4g8dA4TDig0oLF3MMvbBOrTZZG/BAKt+pXvynhSBbm9HKFx4l/4zvDRxIkg9BEeXLGie+P4QRW/J0nDXtK3zi3dY1i6+5xP7x01dnxHv6/Q22kWO4kqG6NJ6xcAGl2NMkKWgcbqNLwNHCaRmocQAV2m+mXF8HT5ha4NxTg4PZAzj9HLRk2I/9/YYS5pDXKx/Gs2ERTQwIDAQABAoIBADhx/qzeWwWvxibxOI9xdFOXXpDcFfGZyliQCOTJtk+eO17NJ42chFmu+0yhHxtMwfC4FUyFNAEAaNZ/9/7M3Ithw5Z0b4t0MOHnhzPzQTCbvwIWA7z6iby5UmuaEMUQQglNQBfyotwG08vqg5/oHV132StSg/ckBSY9vwffQzOPFbwXR6uPE/6E/wAL+ozhlvqftimCObfwrrGgfHpnH0StmDIxNKF8ZGFbpiMKUt43p2PPo6Oq7m9YEDqJhE4aRCEtNOQwA8Kv+nGQAHWmySd+L3Zj0xeuv8c/Y2WZuB/soxace8uc2ecppYGWl6ZqpBcDw7ZKqKpelt3z2nhcIIkCgYEA19lKhoI0fmiW+Pkry6WdoeizAa+yhMWtg6e7O/qp/v9P4z2n1hAG60H4+P/65u0JwoVIlTQ3mRIwyJKzddOQ8XQwsxmBgnYJRglTTBlG3qwIZ/YFmya6kwMfMUDUcYn7tH3mv4iM4nXfmHRbl2X1TBiWSX8PhakyL1IxIxVcpIUCgYEAwu8Jgm2Hhww2Q54iA/+XoY5nIAGglGaVa8sShcii9qwICvgHld1VXmw8sKeLnYg7Nflf5TCc/Ep4UgqZGInz5/Jy/c+8OXloiQ2kmtN8uRPGTS6mZhPeoa5g3dPdRKev6J1Mb78HI/y9op2n718EZt6QYu/0b473oKP1GuTrJycCgYBQ+nFOM00UW5LAR2LZ3QFde9qkeFEGJM9rBCNnZiwewZQsEbaExbCC1FZevFJaDnXJ540KhPOS1tM8fGUdgEjxfQDEQH5o/nWOM/NvKlB/O5VPw2npAkee3d328XaCPh0TYuSN2OHaGBTRsl2mWBcF/HdtjWC6aXatcC2FFv+RrQKBgBeDP7FkxsEqXu0/CLlUvhR1mcjJiXX8/a732q8aaVW5oGq6Sifwf5iZE6T3QKbqxMGY59E8UOM5lFPJBXhpQ2tJ2kb1JK4GD+7gH2exdMzaLsQmiVmsseDsqLB5GqpqU5SKTKr57sGPfcw8mgIMgvpphB769I/0Pbg5rpnk3NxnAoGBAMD4eSoN9u3ATldCzIBHsPQzoJYUmpCdEVMmU4fL3ggwlloNFd9dzC1z6QsNKKbd/HBwGZkbvf2LMVGfpUvQJPrOZHT9aJMJzcdM6BymI5B/zfn1RHZA+6dGVGQDry1yME6+U8mixyRHIeRWSCu2QcLNRihJVOY9iDHsWAHSGB5o
-----END RSA PRIVATE KEY-----"""

# 实例化
alipay = AliPay(
    appid = '2016101000652495',
    app_notify_url = None,
    app_private_key_string = app_private_key_string,
    alipay_public_key_string = alipay_public_key_string,
    sign_type = 'RSA2'
)

# 发起支付请求
order_string = alipay.api_alipay_trade_page_pay(
    out_trade_no = '1002',
    total_amount = '10000.00',
    subject = "生鲜交易",
    return_url = None,
    notify_url = None
)

print('	https://openapi.alipaydev.com/gateway.do?'+order_string)