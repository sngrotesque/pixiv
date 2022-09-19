from hashlib  import sha256 as Hashlib_SHA256
from requests import get    as rget
from json     import dumps  as jdump
from os.path  import exists
from lxml     import etree
from os       import mkdir

import ctypes, cv2, re, threading, os

# 终端输出颜色
BLACK,  RED,   GREEN    = "\x1b[90m", "\x1b[91m", "\x1b[92m"
YELLOW, BLUE,  MAGENTA  = "\x1b[93m", "\x1b[94m", "\x1b[95m"
CYAN,   WHITE, RESET    = "\x1b[96m", "\x1b[97m", "\x1b[0m"

# 宏定义
UserAgent = 'Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0'
Referer   = 'https://www.pixiv.net/'

# 预览Pixiv中的指定数据(图片，压缩包等)
def PixivPreview(url :str, DirectoryName :str, OpenTheFile :bool = True):
    ProxyInfo = {"http": "http://127.0.0.1:1080", "https": "http://127.0.0.1:1080"}
    
    print(f'>>>> 检查{DirectoryName}目录...')
    if not exists(DirectoryName):
        print(f'>>>> 不存在{DirectoryName}目录，创建.')
        os.mkdir(DirectoryName)
    
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

# 获取数据的SHA-256哈希值
def sha256(content :object):
    a = Hashlib_SHA256()
    a.update(content)
    return a.hexdigest()

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

# 通过SHA-256值比较两个文件
def filecmp(fn_1 :str, fn_2 :str):
    with open(fn_1, 'rb') as f: data_1 = f.read()
    with open(fn_2, 'rb') as f: data_2 = f.read()
    return sha256(data_1) == sha256(data_2)

# 将dict类型变量转存为str类型(不对数据转码)
def jdumps(data :dict):
    return jdump(data, ensure_ascii=False)

# 显示图片的各种大小(Bytes, Kb, Mb)
def PictureSizeView(name :str, n :int):
    Kb = n/1024; Mb = n/1024**2
    print(f'>>>> {name} Picture Info.\n>>>> {n} Bytes, {Kb:.2f} Kb, {Mb:.2f} Mb.\n')

# # 随机休眠时间
# from random import uniform
# from time import sleep
# def timeSleep(min_value :float = 0, max_value :float = None):
#     sleep(rand_float(min_value, max_value))
