from .utils import *

class pixiv:
    """
    YourOwnID是必须的，这个值代表你自己的PixivID，是网址栏的ID
    ArtistID是可选，这个值代表想爬取的那个画师的ID。
    HTTP_Cookie是可选的，这个值为你自己的Pixiv Cookie数据。
    Proxy是可选的，使用代理加VPN对Pixiv官网进行访问。
    """
    def __init__(self,
        YourOwnID :str,
        ArtistID :str = None,
        HTTP_Cookie :str = None,
        Proxy :dict = None
        ):
        self.DEFINED_YourID = YourOwnID
        self.DEFINED_ArtistID = ArtistID
        self.DEFINED_Cookie = HTTP_Cookie
        self.DEFINED_Proxy = Proxy
        
        self.DEFINED_UserAgent = 'Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0'
        self.DEFINED_BQ = 24 # 基本量(Basic quantity)
        
        self.RESULTS_ArtistNameID = {}
        self.RESULTS_ArtistPictures = {}

    @property
    def GetAllUsersID(self):
        '''获取关注列表所有的用户ID与用户名称'''
        ForLoopMaxValue = self.DEFINED_BQ * 8192 + 1
        HTTP_Headers = {"User-Agent": self.DEFINED_UserAgent, "Cookie": self.DEFINED_Cookie}
        serialNumber = 1
        
        for page in range(0, ForLoopMaxValue, self.DEFINED_BQ):
            url = f'https://www.pixiv.net/ajax/user/{self.DEFINED_YourID}/following?offset={page}&limit={self.DEFINED_BQ}&rest=show'
            TotalArtistID = rget(url, headers = HTTP_Headers, proxies = self.DEFINED_Proxy, timeout = 3).json()
            
            if not TotalArtistID['body']['users']: break
            
            for ID_Index in TotalArtistID['body']['users']:
                print(f"\r>>>> 已获取{serialNumber:>4}个ID | 本轮用户数: {len(TotalArtistID['body']['users'])}", end='')
                self.RESULTS_ArtistNameID[f'{serialNumber:0>4}'] = {
                    "userId": ID_Index['userId'], "userName": ID_Index['userName']}
                
                serialNumber += 1

    @property
    def GetArtworksOfSingleArtist(self):
        pass

    @property
    def GetAllArtistArtworks(self):
        self.GetAllUsersID
        HTTP_Headers = {"User-Agent": self.DEFINED_UserAgent, "Cookie": self.DEFINED_Cookie}
        serialNumber = 1
        
        for index in self.RESULTS_ArtistNameID:
            uid = self.RESULTS_ArtistNameID[index]['userId']
            url = f'https://www.pixiv.net/ajax/user/{uid}/profile/all?lang=en'
            ArtworkLinks = rget(url, headers = HTTP_Headers, proxies = self.DEFINED_Proxy, timeout = 3).json()
            for ArtworkID in ArtworkLinks[]








