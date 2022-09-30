from snpix.utils import *
import snpix

YouOwnID = 000000000 # 你自己的Pixiv ID
ArtistID = 000000000 # 指定的画师Pixiv ID
Cookie = fread('Cookie.txt').decode()
Proxy = {
    'http': 'http://127.0.0.1:1080',
    'https': 'http://127.0.0.1:1080'
}

# 实例化类
pixiv = snpix.pixiv(HTTP_Cookie=Cookie,  Proxy = Proxy)

pixiv.GetAllArtistInfo(YouOwnID) # 通过你自己的ID来获取关注列表中的所有用户ID和名字
pixiv.RESULTS_ArtistInfo         # 结果保存在此处

pixiv.GetArtworks(ArtistID) # 获取指定用户的所有作品页与作品中所有图片的下载链接
pixiv.RESULTS_ArtworkLinks  # 所有作品页保存在此处
pixiv.RESULTS_PictureLinks  # 所有图片的下载链接保存在此处

url = ['https://www.pixiv.net/artworks/00000000',
'https://www.pixiv.net/artworks/00000000', 'https://www.pixiv.net/artworks/00000000']
folder = 'd:/123123'

pixiv.DownloadArtwork(url, folder) # 将作品列表分别下载保存至指定文件夹
