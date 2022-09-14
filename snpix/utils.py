from requests import get as rget, post as rpost
from json import dumps as jdump, loads as jload
from hashlib import sha256 as Hashlib_SHA256
from random import uniform as rand_float
from os.path import exists, isfile
from threading import Thread
from lxml import etree
from time import sleep
from os import mkdir
import re
import cv2

def sha256(content):
    a = Hashlib_SHA256()
    a.update(content)
    return a.hexdigest()

def fwrite(filePath :str, fileData :bytes):
    with open(filePath, 'wb') as f:
        f.write(fileData)

def fread(filePath :str):
    with open(filePath, 'rb') as f:
        return f.read()

def timeSleep(min_value :float = 0, max_value :float = None):
    sleep(rand_float(min_value, max_value))

def jdumps(data :dict):
    return jdump(data, ensure_ascii=False)
