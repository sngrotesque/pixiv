from snpix.utils import *
import snpix

myuid = 38279179
as109 = 1226647

cookie = fread('000_cookie.txt').decode()
ProxyInfo = {"http": "http://127.0.0.1:1080", "https": "http://127.0.0.1:1080"}

pixiv = snpix.pixiv(HTTP_Cookie=cookie, Proxy=ProxyInfo)










