from geoMarker import *
from PIL import Image
from IPython.display import display 
import os
import re


changeSet = {"카이스트" : "KAIST",
             "오션월드" : "OceanWorld",
             "문래동" : "Mullae-dong",
             "크리스마스" : "Mullae-dong",             
        }


def decode(s):
    return s.encode('utf-8', 'surrogateescape').decode('UTF-8')


def countName(countSet, name):
    if name not in countSet:
        countSet[name] = -1
    countSet[name] += 1
    return str(countSet[name])


def getKo2En(w):
    suffixList = []
    for koWord in changeSet:
        if koWord in w:
            suffixList.append(changeSet[koWord])
    suffix = "_".join(suffixList)
    return suffix

def longestEnWord(w):
    base = os.path.basename(w)
    fileName, ext = os.path.splitext(base)
    p = re.compile("[a-zA-Z ]")
    pos = ([m.start() for m in p.finditer(fileName[11:])])
    if len(pos) < 2:
        return ""
    else:
        return "".join([fileName[11 + i] for i in pos]).strip()

def fixBrokenEncodingFileName(dirName):
    countSet = {}
    dList = sorted(os.listdir(dirName))
    for f in dList:
        _, ext = os.path.splitext(f)
        if not ext.lower() == ".jpg":
            continue
            
        # convert ko into en
        fileName = decode(f)
        ko2EnName = getKo2En(fileName)
        enName = longestEnWord(fileName)
        nameSet = [ko2EnName, enName]
        if "" in nameSet: nameSet.remove("");

        # put Count Number & ext
        newName = f[:11] + "_".join(nameSet)
        countNumber = countName(countSet, newName)
        newFileName = "_".join([newName, countNumber]) + ext
        
        print(fileName, "==>", newFileName)
        os.rename(os.path.join(dirName, f), os.path.join(dirName, newFileName))  

        
locationSet = {
    "KAIST":(36.372902, 127.360034),
    "OceanWorld":(37.648157, 127.685571),
}


def getLocationSet(word):
    for l in locationSet:
        if l in word:
            return locationSet[l]
    return (None, None)


def getDate(fileName):
    (year, month, day) = (fileName[:4], fileName[5:7], fileName[8:10])
    return "%s:%s:%s 00:00:00" % (year, month, day)
    

def markAllGeoDateDir(dirName, newdirName=""):
    dList = sorted(os.listdir(dirName))
    for f in dList:
        if f[-4:].lower() != ".jpg":
            continue

        filePath = os.path.join(dirName, f)        
        print(f)


        newPath = os.path.join(newdirName, f)
        lat, lon = getLocationSet(f)
        modiExif(filePath, newPath, lat, lon, getDate(f))
    
def displayAllPictures(dirName, maxCount=99999):
    dList = sorted(os.listdir(dirName), key=lambda x:decode(x))
    count = 0
    for f in dList:
        if f[-4:].lower() != ".jpg":
            continue

        if count < maxCount:
            count += 1
        else:
            break
            
        filePath = os.path.join(dirName, f)        
        pil_im = Image.open(filePath, 'r')
        display(pil_im)
        print(decode(filePath))

# displayAllPictures("2008")
# markAllGeoDateDir("2008", "_2008")