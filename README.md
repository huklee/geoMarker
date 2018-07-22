# geoMarker
photo geo information auto-marker

# usage

``` python
import geoMarker
geoMarker.modiExif(oriImgFile = "img/noGeo.jpg", \
         destImgFile = '_%s' % "new_nogeo.jpg",\
         lat = 37.810594,\
         lon = -122.476978,\
         date = "1999:07:14 19:42:19")
```
