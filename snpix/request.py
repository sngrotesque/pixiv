from .utils import *

class pixiv:
    def __init__(self,
        YourOwnID :str,
        HTTP_Cookie :str = None,
        Proxy :dict = None
        ):
        self.DEFINED_YourID = YourOwnID
        self.DEFINED_Cookie = HTTP_Cookie
        self.DEFINED_Proxy = Proxy
        
        self.DEFINED_UserAgent = 'Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0'
        self.DEFINED_BQ = 24 # 基本量(Basic quantity)
        
        self.RESULTS_AuthorNameID = {}

    @property
    def GetAllUsersID(self):
        '''获取关注列表所有的用户ID与用户名称'''
        ForLoopMaxValue = self.DEFINED_BQ * 8192 + 1
        serialNumber = 1
        
        for page in range(0, ForLoopMaxValue, self.DEFINED_BQ):
            HTTP_Headers = {"User-Agent": self.DEFINED_UserAgent, "Cookie": self.DEFINED_Cookie}
            url = f'https://www.pixiv.net/ajax/user/{self.DEFINED_YourID}/following?offset={page}&limit={self.DEFINED_BQ}&rest=show'
            TotalAuthorID = rget(url, headers = HTTP_Headers, proxies = self.DEFINED_Proxy, timeout = 3).json()
            
            if not TotalAuthorID['body']['users']: break
            
            for ID_Index in TotalAuthorID['body']['users']:
                print(f"\r>>>> 已获取[{serialNumber:>4}]个ID | {len(TotalAuthorID['body']['users'])}", end='')
                self.RESULTS_AuthorNameID[f'{serialNumber:0>4}'] = {
                    "userId": ID_Index['userId'], "userName": ID_Index['userName']}
                
                serialNumber += 1

