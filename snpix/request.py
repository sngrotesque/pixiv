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
        '''
        目前遇到的问题如下
            1. 由于每页加载self.DEFINED_BQ个用户，导致如果用户总数无法整除for循环中page中的数时会无法获取到所有用户的ID
        解决方案猜测
            1. 将self.DEFINED_BQ设为1，每次只获取1个用户的ID，最后判断users中的列表以确认是否结束循环（但效率会很慢）
            2. 保持现状，但通过users列表中的数据来决定如何处理总数据（可行性比较低）
        '''
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

