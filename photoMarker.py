from geoMarker import *
from PIL import Image
from IPython.display import display 
import os

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

def changeKo2En(countSet, word):
    suffixList = []
    for w in changeSet:
        if w in word:
            suffixList.append(changeSet[w])
    suffix = "_".join(suffixList)
    countNumber = countName(countSet, word[:11] + suffix)
    return word[:11] + suffix + "_" + countNumber + word[-4:]

def fixBrokenEncodingFileName(dirName):
    countSet = {}
    dList = sorted(os.listdir(dirName))
    for f in dList:
        if not f[-4:].lower() == ".jpg":
            continue
        fileName = decode(f)
        newName = changeKo2En(countSet, fileName)
        print(fileName, " ==> ", newName)
        os.rename(os.path.join(dirName, f), os.path.join(dirName, newName))   
    

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
    
def displayAllPictures(dirName):
    dList = sorted(os.listdir(dirName))
    for f in dList:
        if f[-4:].lower() != ".jpg":
            continue

        filePath = os.path.join(dirName, f)        
        pil_im = Image.open(filePath, 'r')
        display(pil_im)
        print(f)

# displayAllPictures("2008")
# markAllGeoDateDir("2008", "_2008")