import piexif
import pickle
from PIL import Image

# convert six-digits representation into one-digit representation
def six2one(gps):
    gps = abs(gps)
    res = 0
    _gps = [x[0] for x in gps]
    for i, d in enumerate(_gps):
        res += d / (60**i)
    return res

# convert one-digit representation into six-digits representation
def one2six(gps):
    gps = abs(gps)
    res = []
    for i in range(3):
        res.append(int(gps))
        gps = (gps - int(gps))*60.0
    return tuple([(x,1) for x in res])

def convLatitudeRef(lat):
    if lat < 0:
        return b"S"
    else:
        return b"N"
    
def convLongitudeRef(log):
    if log < 0:
        return b"W"
    else:
        return b"E"

# modify exif with 
def modiExif(oriImgFile, destImgFile, lat, lon, date, exif_pickle="exif_jpg.pkl"):
    assert oriImgFile[-4:].lower() == ".jpg" or oriImgFile[-5:].lower() == ".jpeg"
    
    img = Image.open(oriImgFile)
    # exif_dict = piexif.load(img.info['exif'])

    exif_dict = pickle.load(open(exif_pickle, "rb"))
    exif_dict['GPS'][piexif.GPSIFD.GPSLatitude] = one2six(lat)
    exif_dict['GPS'][piexif.GPSIFD.GPSLatitudeRef] = convLatitudeRef(lat)
    exif_dict["GPS"][piexif.GPSIFD.GPSLongitude] = one2six(lon)
    exif_dict["GPS"][piexif.GPSIFD.GPSLongitudeRef] = convLongitudeRef(lon)
    exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = str.encode(date)

    exif_bytes = piexif.dump(exif_dict)
    img.save(destImgFile, "jpeg", exif=exif_bytes)

if __name__ == "__main__":
    # example
    modiExif(oriImgFile = "img/noGeo.jpg", \
        destImgFile = '_%s' % "new_nogeo2.jpg",\
        lat = 37.810594,\
        lon = -122.476978,\
        date = "1999:07:14 19:42:19")
