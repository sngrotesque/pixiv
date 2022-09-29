from .utils import *

def requestGET(self, url :str):
    return rget(url, headers = self.DEFINED_Headers, proxies = self.DEFINED_Proxy)

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
            getTotalArtistAPI = f'https://www.pixiv.net/ajax/user/{YourOwnID}/following?offset={page}&limit=24&rest=show'
            TotalArtistID = requestGET(self, getTotalArtistAPI).json()
            if not TotalArtistID['body']['users']:
                print('\n>>>> Done.')
                break
            
            for index in TotalArtistID['body']['users']:
                snprint(f"\r>>>> 已获取{CYAN}{serialNumber:>4}{RESET}个ID")
                self.RESULTS_ArtistInfo[f'{serialNumber:0>4}'] = {
                    "ArtistUrl": f'https://www.pixiv.net/users/{index["userId"]}',
                    "userName" : index['userName']
                }
                serialNumber += 1

    def GetArtworks(self, artistID :Union[str, int]):
        getAllArtworkAPI = f'https://www.pixiv.net/ajax/user/{artistID}/profile/all?lang=zh'
        artworksIDList = [*requestGET(self, getAllArtworkAPI).json()['body']['illusts'].keys()]
        
        serialNumber = 1
        for ID in artworksIDList:
            self.RESULTS_ArtworkLinks.append(f'https://www.pixiv.net/artworks/{ID}')
            snprint(f"\r>>>> 已获取{CYAN}{serialNumber:>4}{RESET}个作品链接.")
            serialNumber += 1
        print('')
        
        for artworkID in artworksIDList:
            dynamicGraphURL   = f'https://www.pixiv.net/ajax/illust/{artworkID}/ugoira_meta?lang=zh'
            staticDiagramURL  = f'https://www.pixiv.net/ajax/illust/{artworkID}/pages?lang=zh'
            dynamicGraphList  = requestGET(self, dynamicGraphURL).json()['body']
            staticDiagramList = requestGET(self, staticDiagramURL).json()['body']
            
            if dynamicGraphList:
                self.RESULTS_PictureLinks.append(dynamicGraphList['originalSrc'])
            else:
                for index in staticDiagramList:
                    self.RESULTS_PictureLinks.append(index['urls']['original'])
            
            snprint(f"\r>>>> 已获取{CYAN}{len(self.RESULTS_PictureLinks):>4}{RESET}个作品下载链接.")
        print('')

    def DownloadArtwork(self, artworkUrl :List[str], folder :str, zipToGif :bool = True):
        self.DEFINED_Headers['Referer'] = "https://www.pixiv.net/"
        if not exists(folder): mkdir(folder)
        
        for link in artworkUrl:
            fileArchivePath = f'{folder}/{SetFileName(link)}'
            if exists(fileArchivePath):
                snprint(f'\r>>>> {fileArchivePath}已存在，跳过...')
                continue
            artworkContent = requestGET(self, link)
            if artworkContent.headers['Content-Type'] == 'application/zip':
                if zipToGif:
                    zipProcess(link, fileArchivePath, artworkContent.content, folder)
                else:
                    fwrite(fileArchivePath, artworkContent.content)
            elif artworkContent.headers['Content-Type'] == 'image/jpeg' or 'image/png':
                fwrite(fileArchivePath, artworkContent.content)
            
            snprint(f'\r>>>> 已保存{CYAN}{link}{RESET}')
        print('')

    def MultiThreadDownloadArtwork(self, artworkUrl :List[str], folder :str, zipToGif :bool = True):
        self.DEFINED_Headers['Referer'] = "https://www.pixiv.net/"
        if not exists(folder): mkdir(folder)
        self.totalNumberOfThreads = 8
        
        def download(threadNumber):
            for artworkIndex in range(threadNumber, len(artworkUrl), self.totalNumberOfThreads):
                fileArchivePath = f'{folder}/{SetFileName(artworkUrl[artworkIndex])}'
                if exists(fileArchivePath):
                    snprint(f'\r>>>> {fileArchivePath}已存在，跳过...')
                    continue
                artworkContent = requestGET(self, artworkUrl[artworkIndex])
                if artworkContent.headers['Content-Type'] == 'application/zip':
                    if zipToGif:
                        zipProcess(artworkUrl[artworkIndex], fileArchivePath, artworkContent.content, folder)
                    else:
                        fwrite(fileArchivePath, artworkContent.content)
                elif artworkContent.headers['Content-Type'] == 'image/jpeg' or 'image/png':
                    fwrite(fileArchivePath, artworkContent.content)
                snprint(f'\r>>>> {threadNumber} 已保存{CYAN}{artworkUrl[artworkIndex]}{RESET}')
        
        TotalThread = [threading.Thread(target = download, args = (x, ))
            for x in range(self.totalNumberOfThreads)]
        for x in TotalThread:
            x.start()
        for x in TotalThread:
            x.join()


