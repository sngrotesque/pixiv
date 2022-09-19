from .utils import *

class pixiv:
    def __init__(self, HTTP_Cookie :str, ArtistID :int = None, Proxy :dict = None):
        self.DEFINED_Cookie   = HTTP_Cookie # 你在Pixiv网站上的Cookie
        self.DEFINED_ArtistID = ArtistID    # 某位画师的用户ID
        self.DEFINED_Proxy    = Proxy       # 代理服务器
        self.DEFINED_Headers  = {"User-Agent": UserAgent, "Cookie": self.DEFINED_Cookie}
        self.RESULTS_ArtistInfo   = {} # Json数据，用来存放关注列表中所有用户的ID和名字
        self.RESULTS_ArtworkLinks = [] # List数据，用来存放某位画师所有的插画作品链接
        self.RESULTS_PictureLinks = [] # List数据，用来存放某个作品链接中的所有图片链接

    def GetAllArtistInfo(self, YourOwnID :int):
        serialNumber = 1
        for page in range(0, 196609, 24):
            url = f'https://www.pixiv.net/ajax/user/{YourOwnID}/following?offset={page}&limit=24&rest=show'
            TotalArtistID = rget(url, headers = self.DEFINED_Headers, proxies = self.DEFINED_Proxy).json()
            if not TotalArtistID['body']['users']: print('\n>>>> Done.'); break
            
            for index in TotalArtistID['body']['users']:
                print(f"\r>>>> 已获取{CYAN}{serialNumber:>4}{RESET}个ID", end='')
                self.RESULTS_ArtistInfo[f'{serialNumber:0>4}'] = {
                    "ArtistUrl": f'https://www.pixiv.net/users/{index["userId"]}',
                    "userName" : index['userName']}
                serialNumber += 1

    @property
    def GetTotalArtworksLink(self):
        url = f'https://www.pixiv.net/ajax/user/{self.DEFINED_ArtistID}/profile/all?lang=zh'
        TotalArtworks = rget(url, headers = self.DEFINED_Headers, proxies = self.DEFINED_Proxy).json()
        TotalArtworks= list(TotalArtworks['body']['illusts'].keys())
        serialNumber = 1
        for artworkID in TotalArtworks:
            self.RESULTS_ArtworkLinks.append(f'https://www.pixiv.net/artworks/{artworkID}')
            print(f'\r>>>> {CYAN}{serialNumber:>4}{RESET} Get artwork ID: {artworkID:>8}', end='')
            serialNumber += 1
        print('\n>>>> Done.')

    def GetPictureLink(self, ArtworkUrl :str):
        artworkID = re.findall(r'https://www.pixiv.net/artworks/(\d+)', ArtworkUrl, re.S)[0]
        ArtkworkJson = rget(f'https://www.pixiv.net/ajax/illust/{artworkID}/pages?lang=zh',
            headers = self.DEFINED_Headers, proxies = self.DEFINED_Proxy).json()
        for index in ArtkworkJson['body']:
            self.RESULTS_PictureLinks.append(index['urls']['original'])

    def DownloadPictures(self, PictureLink :str, DirectoryName :str):
        if not exists(DirectoryName): mkdir(DirectoryName)
        PictureFileName = re.findall(
        r'\w+://[a-zA-Z0-9.\-\_]+/[a-zA-Z\-\_]+/img/'
        r'([0-9a-zA-Z./\_]+)', PictureLink, re.S | re.I)[0]
        PictureFileName = PictureFileName.replace('/', '_')
        PictureFileName = f'{DirectoryName}/{PictureFileName}'
        if exists(PictureFileName):
            print(f'>>>> 已存在{PictureFileName}, 跳过...')
            return
        
        self.DEFINED_Headers['Referer'] = 'https://www.pixiv.net/'
        pictureData = rget(PictureLink, headers = self.DEFINED_Headers,
            proxies = self.DEFINED_Proxy).content
        
        print(f'>>>> ')
        fwrite(PictureFileName, pictureData)





