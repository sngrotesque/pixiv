from .utils import *

def Pixiv_img_preview(url :str, DirectoryName :str, OpenTheFile :bool = False):
    UserAgent = 'Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0'
    ProxyInfo = {"http": "http://127.0.0.1:1080", "https": "http://127.0.0.1:1080"}
    BasicReferer = 'https://www.pixiv.net/'
    
    print(f'>>>> 检查{DirectoryName}目录...')
    if not exists(DirectoryName):
        print(f'>>>> 不存在{DirectoryName}目录，创建.')
        mkdir(DirectoryName)
    
    print(f'>>>> 为文件创建名称.')
    fileName = re.findall( # 为文件命名
        r'\w+://[a-zA-Z0-9.\-\_]+/[a-zA-Z\-\_]+/img/'
        r'([0-9a-zA-Z./\_]+)', url, re.S | re.I)[0]
    fileName = fileName.replace('/', '_')
    fileName = f'000_{fileName}'
    fileName = f'{DirectoryName}/{fileName}'
    
    print(f'>>>> 获取文件数据.')
    imgData = rget(url, headers = {'user-agent': UserAgent, 'Referer': BasicReferer},
        proxies = ProxyInfo).content
    print(f'>>>> 保存至文件: {fileName}')
    fwrite(fileName, imgData)
    
    try:
        print(f'>>>> 预览文件.')
        img = cv2.imread(fileName)
        cv2.imshow(DirectoryName, img)
        cv2.waitKey(0)
    except cv2.error:
        print(f'>>>> 非图片文件，不采取预览的操作。\n>>>> fileName: {fileName}')
        if OpenTheFile:
            ctypes.windll.shell32.ShellExecuteW(None, 'open', fileName.replace('/','\\'), None, None, 1)

class pixiv:
    """
    ArtistID    是可选，这个值代表想爬取的那个画师的ID。
    HTTP_Cookie 是可选的，这个值为你自己的Pixiv Cookie数据。
    Proxy       是可选的，使用代理加VPN对Pixiv官网进行访问。
    """
    def __init__(self, ArtistID :str = None, HTTP_Cookie :str = None, Proxy :dict = None):
        self.DEFINED_ArtistID = ArtistID
        self.DEFINED_Cookie = HTTP_Cookie
        self.DEFINED_Proxy = Proxy
        
        self.DEFINED_UserAgent = 'Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0'
        self.DEFINED_BQ = 24 # 基本量(Basic quantity)
        self.DEFINED_HTTP_Headers = {
            "User-Agent": self.DEFINED_UserAgent,
            "Cookie": self.DEFINED_Cookie}
        
        self.RESULTS_ArtistNameID = {}
        self.RESULTS_ArtistArtworks = {}
        self.RESULTS_ArtworkPictureLinks = {}

    def GetAllUsersNameID(self, YourOwnID :str):
        '''YourOwnID   是必须的，这个值代表你自己的PixivID，是网址栏的ID
        获取关注列表所有的用户ID与用户名称'''
        ForLoopMaxValue = self.DEFINED_BQ * 8192 + 1 # 最大页数
        serialNumber = 1 # 序号
        
        for page in range(0, ForLoopMaxValue, self.DEFINED_BQ):
            # 单页关注用户的链接，每页最多显示self.DEFINED_BQ个用户
            url = f'https://www.pixiv.net/ajax/user/{YourOwnID}/following?offset={page}&limit={self.DEFINED_BQ}&rest=show'
            TotalArtistID = rget(url,
                headers = self.DEFINED_HTTP_Headers, proxies = self.DEFINED_Proxy, timeout = 3).json()
            if not TotalArtistID['body']['users']: break # 如果获取的用户列表为空就终止循环
            for ID_Index in TotalArtistID['body']['users']:
                print(f"\r>>>> 已获取{serialNumber:>4}个ID | 本轮用户数: {len(TotalArtistID['body']['users'])}", end='')
                self.RESULTS_ArtistNameID[f'{serialNumber:0>4}'] = {
                    "userId": f'https://www.pixiv.net/users/{ID_Index["userId"]}',
                    "userName": ID_Index['userName']}
                serialNumber += 1
        print("")








