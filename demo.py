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
pixiv = snpix.pixiv(HTTP_Cookie=Cookie, ArtistID = ArtistID,  Proxy = Proxy)

pixiv.GetAllArtistInfo(YouOwnID) # 通过你自己的ID来获取关注列表中的所有用户ID和名字
pixiv.RESULTS_ArtistInfo         # 结果保存在此处

pixiv.GetTotalArtworksLink # 通过PixivAPI获取指定画师的所有插画作品链接
pixiv.RESULTS_ArtworkLinks # 结果保存在此处

artworkUrl = 'https://www.pixiv.net/artworks/99901109'
pixiv.GetPictureLink(artworkUrl) # 通过PixivAPI获取单个作品中所有的图片链接
pixiv.RESULTS_PictureLinks # 结果保存在此处

PictureUrl = 'https://i.pximg.net/img-original/img/2022/07/22/06/21/36/99901109_p0.jpg'
DirectoryName = 'pixiv_picture'
pixiv.DownloadPictures(PictureUrl, DirectoryName)
# 通过图片的源链接下载原图
