#!/usr/bin/python3

from urllib import request
from PIL import Image
import os
from math import *

'''
Tiles are 256 × 256 pixel PNG files
At zoom 0, the entire earth is in a 256 x 256 image => 1px = 156543.03 m
'''
EARTH_RADIUS = 6371000
LEN_EQUATOR = 40075.016686 # km
LEN_PER_PX_1 = 156543.03 # meter/px at zoom 1, 40075.016686 * 1000 / 256

SCALE = 2
HEIGHT_WATERMARK = 22 # px
TILE_SIZE = 640 - HEIGHT_WATERMARK # px, 640 is the max size without api key

class ImageDownloader:
    def __init__(self, API_key, length):
        self._zoom = 18 # ~ log2(LEN_PER_PX_1 * 640 / length) + 1
        #self._image_size = 2**(self._zoom - 1) * length / LEN_PER_PX_0
        self._image_size = 512 * SCALE
        self._API_key = API_key

    def GPS2Mercator(self, lat, lng):
    	x = EARTH_RADIUS * lng
    	y = EARTH_RADIUS * log(tan(pi/4 + lat/2))
    	return (x,y)

    def Mercator2GPS(self,x,y):
    	lng = x/EARTH_RADIUS
    	lat = 2*atan(exp(y/EARTH_RADIUS)) - pi/2
    	return (lng,lat)

    def download(self, lat, lng):
        lat_rad = (pi/180)*abs(lat)
        lng_rad = (pi/180)*abs(lng)
        xy_loc  = self.GPS2Mercator(lat_rad, lng_rad)

        url = 'https://maps.googleapis.com/maps/api/staticmap?'
        url += 'center='+str(lat)+','+str(lng)
        url += '&zoom='+str(self._zoom)
        url += '&size=640x640'
        url += '&maptype=satellite'
        url += '&scale=2'
        #print(url)
        if self._API_key:
            url += '&key='+self._API_key
        request.urlretrieve(url, 'tmp')
        img = Image.open('tmp')
        center = 320 * SCALE
        b_box = (center - self._image_size//2, center - self._image_size//2,
                 center + self._image_size//2, center + self._image_size//2)
        return img.crop(b_box).convert('RGB')

def test():
    gmap_key  = ""

    latitude, longitude = 47.61950703, 8.210134303
    map_size = 200 # meter

    downloader = ImageDownloader(gmap_key, map_size)
    img = downloader.download(latitude, longitude)
    img.save("test.jpg")

if __name__ == "__main__":
    test()
