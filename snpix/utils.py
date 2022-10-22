from requests import get as rget
from json     import dumps
from zipfile  import ZipFile
from os.path  import exists
from os       import mkdir, remove, rmdir
from typing   import Union, List
import ctypes, cv2, re, threading

# 终端输出颜色
RED, GOLD, CYAN, RESET = "\x1b[91m", "\x1b[93m", "\x1b[96m", "\x1b[0m"

# 宏定义
UserAgent = 'Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0'
Referer   = 'https://www.pixiv.net/'

# 预览Pixiv中的指定数据(图片，压缩包等)
def PixivPreview(url :str, DirectoryName :str, OpenTheFile :bool = True):
    ProxyInfo = {"http": "http://127.0.0.1:1080", "https": "http://127.0.0.1:1080"}
    
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
    imgData = rget(url, headers = {'user-agent': UserAgent, 'Referer': Referer},
        proxies = ProxyInfo).content
    print(f'>>>> 保存至文件: {fileName}')
    fwrite(fileName, imgData)
    
    if OpenTheFile:
        try:
            print(f'>>>> 预览文件.')
            img = cv2.imread(fileName)
            cv2.imshow(DirectoryName, img)
            cv2.waitKey(0)
        except cv2.error:
            print(f'>>>> 非图片文件，不采取预览的操作。\n>>>> fileName: {fileName}')
            ctypes.windll.shell32.ShellExecuteW(None, 'open', fileName.replace('/','\\'), None, None, 1)

# 以二进制格式写入文件
def fwrite(filePath :str, fileData :bytes):
    with open(filePath, 'wb') as f:
        f.write(fileData)

# 以二进制格式读取文件
def fread(filePath :str):
    with open(filePath, 'rb') as f:
        return f.read()

# 将json数据保存至文件
def fwriteJson(filePath :str, fileData :bytes):
    fwrite(filePath, jdumps(fileData).encode())

# 将dict类型变量转存为str类型(不对数据转码)
def jdumps(data :dict):
    return dumps(data, ensure_ascii=False)

# 判断目录是否存在，不存在就创建
def CheckDirectory(name):
    if not exists(name):
        mkdir(name)

# 用Pixiv的下载链接命名文件
def SetFileName(url :str):
    fileName = re.findall( # 为文件命名
        r'\w+://[a-zA-Z0-9.\-\_]+/[a-zA-Z\-\_]+/img/'
        r'([0-9a-zA-Z./\_]+)', url, re.S | re.I)[0]
    fileName = fileName.replace('/', '_')
    return fileName

# 一堆jpg转mp4
def jpg2mp4(in_path :List[str], out_path :str, fps :int = 15):
    img_array = []
    for filename in in_path:
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)
    out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()

def zipProcess(link, fileArchivePath :str, content :Union[ZipFile, bytes], folder :str):
    fwrite(fileArchivePath, content)
    zipData = ZipFile(fileArchivePath, 'r')
    zipName = zipData.namelist()

    jpgToGifTempArchivePath = f'{fileArchivePath}_temp/'
    if not exists(jpgToGifTempArchivePath):
        mkdir(jpgToGifTempArchivePath)
    zipData.extractall(jpgToGifTempArchivePath)
    zipData.close()
    
    jpgPath = [f'{jpgToGifTempArchivePath}/{fn}' for fn in zipName]
    gifFileName = SetFileName(link).replace('zip', 'mp4')
    
    jpg2mp4(jpgPath, f'{folder}/{gifFileName}')
    for fn in jpgPath:
        remove(fn)
    remove(fileArchivePath)
    rmdir(jpgToGifTempArchivePath)

def executeMultithreading(function :object, totalNumberOfThreads :int):
    TotalThread = [threading.Thread(target = function, args = (threadNumber, ))
        for threadNumber in range(totalNumberOfThreads)]
    for singleThread in TotalThread: singleThread.start()
    for singleThread in TotalThread: singleThread.join()
