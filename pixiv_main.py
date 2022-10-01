from snpix.utils import *
import snpix

# 524346 进度已完成

cookie = fread('000_cookie.txt').decode()
ProxyInfo = {"http": "http://127.0.0.1:1080", "https": "http://127.0.0.1:1080"}

def single():
    artistID = '524346'
    path = f'p:/Pixiv/{artistID}'

    pixiv = snpix.pixiv(HTTP_Cookie=cookie, Proxy=ProxyInfo)

    pixiv.MultiThreadGetArtworks(artistID)
    pixiv.MultiThreadDownloadArtwork(pixiv.RESULTS_PictureLinks, path)

def Multiple():
    artistIDList = [
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        ''
    ]

    pixiv = snpix.pixiv(HTTP_Cookie=cookie, Proxy=ProxyInfo)
    
    for artistID in artistIDList:
        path = f'p:/Pixiv/{artistID}'
        pixiv.MultiThreadGetArtworks(artistID)
        pixiv.MultiThreadDownloadArtwork(pixiv.RESULTS_PictureLinks, path)

# Multiple()
single()
