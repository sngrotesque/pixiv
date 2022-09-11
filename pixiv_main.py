from snpix.utils import *
import snpix

SNGrotesqueID = '38279179'
Cookie = fread('000_cookie.txt').decode()
Proxy = {'http': 'http://127.0.0.1:1080','https': 'http://127.0.0.1:1080'}

res = snpix.pixiv(SNGrotesqueID, HTTP_Cookie=Cookie, Proxy = Proxy)
res.GetAllUsersNameID

with open('000_ALL_Pixiv_Follow_list_new.json', 'w', encoding='utf-8') as f:
    f.write(jdump(res.RESULTS_AuthorNameID, ensure_ascii=False))


