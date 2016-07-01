import config
import Image
import urllib
import os

CLAVE = config.getKey()
HOME_PATH = os.path.dirname(os.path.realpath(__file__))

API_URL = "https://maps.googleapis.com/maps/api/streetview?size=640x300&location=46.414382,10.013988&heading=151.78&pitch=0&key=" + CLAVE

urllib.urlretrieve(API_URL, HOME_PATH + "/images/test.jpg")

print "Hecho!"
