import config
import Image
import urllib
import os
import subprocess
import random_street_view

CLAVE = config.getKey()
HOME_PATH = os.path.dirname(os.path.realpath(__file__))
PAISES = [
    "ARG",
    "CHL",
    "URY",
    "PER",
    "BOL",
    "BRA",
    "ECU",
    "COL",
    "ZAF",
    "BWA"
]

# API_URL = "https://maps.googleapis.com/maps/api/streetview?size=640x300&location=46.414382,10.013988&heading=151.78&pitch=0&key=" + CLAVE

# urllib.urlretrieve(API_URL, HOME_PATH + "/images/test.jpg")

# subprocess.call([HOME_PATH + '/random_street_view.py', 'ARG'])
# subprocess.Popen((HOME_PATH + "/random_street_view.py", 'USA',), shell=True)

lat_lon = random_street_view.getImage("FRA")

print "La latitud y la longitud son: " + lat_lon
