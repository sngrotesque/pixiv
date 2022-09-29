from snpix.utils import *
import snpix
import time

myuid    = 38279179
artistID = 13916279

cookie = fread('000_cookie.txt').decode()
ProxyInfo = {"http": "http://127.0.0.1:1080", "https": "http://127.0.0.1:1080"}

pixiv = snpix.pixiv(HTTP_Cookie=cookie, Proxy=ProxyInfo)



