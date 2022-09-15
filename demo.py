from snpix.utils import *
import snpix

YouOwnID = '' # 你自己的Pixiv ID
Cookie = fread('000_cookie.txt').decode()
Proxy = {'http': 'http://127.0.0.1:1080','https': 'http://127.0.0.1:1080'}

res = snpix.pixiv(HTTP_Cookie=Cookie, Proxy = Proxy)
res.GetAllUsersNameID(YouOwnID)

with open('000_AllPixivFollowList.json', 'w', encoding='utf-8') as f:
    f.write(jdump(res.RESULTS_ArtistNameID, ensure_ascii=False))


