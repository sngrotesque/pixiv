from .utils import *

def requestGET(self, url :str):
    return rget(url, headers = self.DEFINED_Headers, proxies = self.DEFINED_Proxy)

def initializeDownload(self, folder :str):
    self.DEFINED_Headers['Referer'] = Referer
    if not exists(folder): mkdir(folder)
    print(f'>>>> 开始下载作品.')

class pixiv:
    def __init__(self, HTTP_Cookie :str, Proxy :dict = None):
        self.DEFINED_Cookie       = HTTP_Cookie # 你在Pixiv网站上的Cookie
        self.DEFINED_Proxy        = Proxy       # 代理服务器
        self.DEFINED_Headers      = {"User-Agent": UserAgent, "Cookie": self.DEFINED_Cookie}
        self.totalNumberOfThreads = 8  # 多线程下载时使用的线程总数
        self.RESULTS_ArtistInfo   = {} # Json数据，用来存放关注列表中所有用户的ID和名字
        self.RESULTS_ArtworkLinks = [] # List数据，用来存放某位画师所有的作品链接
        self.RESULTS_PictureLinks = [] # List数据，用来存放某个作品链接中的所有图片链接

    def GetArtistInfo(self, YourOwnID :Union[str, int]):
        serialNumber = 1
        for page in range(0, 240001, 24):
            getTotalArtistAPI = \
                f'https://www.pixiv.net/ajax/user/{YourOwnID}/following?offset={page}&limit=24&rest=show'
            TotalArtistID = requestGET(self, getTotalArtistAPI).json()
            if not TotalArtistID['body']['users']:
                print('\n>>>> Done.')
                break
            
            for index in TotalArtistID['body']['users']:
                print(f">>>> 已获取{CYAN}{serialNumber:>4}{RESET}个ID")
                self.RESULTS_ArtistInfo[f'{serialNumber:0>4}'] = {
                    "ArtistUrl": f'https://www.pixiv.net/users/{index["userId"]}',
                    "userName" : index['userName']
                }
                serialNumber += 1

    def MultiThreadGetArtworks(self, artistID :Union[str, int]):
        print(f'>>>> 开始获取{artistID}的作品')
        getAllArtworkAPI = f'https://www.pixiv.net/ajax/user/{artistID}/profile/all?lang=zh'
        artworksIDList = [*requestGET(self, getAllArtworkAPI).json()['body']['illusts'].keys()]
        totalArtworks = len(artworksIDList)
        
        self.RESULTS_ArtworkLinks = [f'https://www.pixiv.net/artworks/{ID}' for ID in artworksIDList]
        print(f">>>> 已获取{CYAN}{totalArtworks:>4}{RESET}个作品链接.")
        
        def _getartwork(threadNumber):
            for ID in range(threadNumber, len(artworksIDList), self.totalNumberOfThreads):
                print(f'>>>>  Thread {threadNumber:0>2}: 正在获取下载链接.')
                dynamicGraphList  = requestGET(self,
                    f'https://www.pixiv.net/ajax/illust/{artworksIDList[ID]}/ugoira_meta?lang=zh').json()['body']
                staticDiagramList = requestGET(self,
                    f'https://www.pixiv.net/ajax/illust/{artworksIDList[ID]}/pages?lang=zh').json()['body']
                if dynamicGraphList: self.RESULTS_PictureLinks.append(dynamicGraphList['originalSrc'])
                else:
                    for index in staticDiagramList: self.RESULTS_PictureLinks.append(index['urls']['original'])
        executeMultithreading(_getartwork, self.totalNumberOfThreads)
        
        print(f">>>> 已获取{CYAN}{len(self.RESULTS_PictureLinks):>4}{RESET}个作品下载链接.")

    def MultiThreadDownloadArtwork(self, artworkUrl :List[str], folder :str, zipToMp4 :bool = True):
        initializeDownload(self, folder) # 初始化下载功能
        def _download(threadNumber):
            for artworkIndex in range(threadNumber, len(artworkUrl), self.totalNumberOfThreads):
                fileArchivePath = f'{folder}/{SetFileName(artworkUrl[artworkIndex])}'
                if exists(fileArchivePath):
                    print(f'>>>> {fileArchivePath}已存在，跳过...')
                    continue
                artworkContent = requestGET(self, artworkUrl[artworkIndex])
                if artworkContent.headers['Content-Type'] == 'application/zip':
                    if zipToMp4:
                        zipProcess(artworkUrl[artworkIndex], fileArchivePath, artworkContent.content, folder)
                    else:
                        fwrite(fileArchivePath, artworkContent.content)
                elif artworkContent.headers['Content-Type'] == 'image/jpeg' or 'image/png':
                    fwrite(fileArchivePath, artworkContent.content)
                print(f'>>>> Thread {threadNumber:0>2}: {CYAN}{artworkUrl[artworkIndex]}{RESET} saved.')
        executeMultithreading(_download, self.totalNumberOfThreads)
