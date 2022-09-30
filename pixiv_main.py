from snpix.utils import *
import snpix

import os, time

artistID = '74188348'
path = f'p:/Pixiv/{artistID}'

cookie = fread('000_cookie.txt').decode()
ProxyInfo = {"http": "http://127.0.0.1:1080", "https": "http://127.0.0.1:1080"}

pixiv = snpix.pixiv(HTTP_Cookie=cookie, Proxy=ProxyInfo)

pixiv.MultiThreadGetArtworks(artistID)
pixiv.MultiThreadDownloadArtwork(pixiv.RESULTS_PictureLinks, path)
