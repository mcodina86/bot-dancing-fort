import config
import Image
import urllib
import os
import subprocess
import random_street_view
import random
import requests
import glob
import gifcreator
from twython import Twython
from shutil import copyfile



CLAVE = config.getKey()
HOME_PATH = os.path.dirname(os.path.realpath(__file__))
PAISES = ["ARG","CHL","URY","PER","BOL","BRA","ECU","COL","ZAF","ISR","NZL","AUS","PHL","SGP","THA","KHM","TWN","BGD","LKA",'HKG','JPN','BTN','TUR','BGR','ROU','GRC','UKR','MKD','SRB','HRV','SVK','SVN','HUN','POL','CZE','LTU','LVA','EST','SWE','FIN','NOR','ITA','ESP','PRT','NLD','BEL','FRA','GBR','IRL','DNK','USA','MEX']
ELEGIDO = random.choice(PAISES)
TWITTER = config.getTwitterKeys()
print "El pais elegido es: " + ELEGIDO

def getImage():
    lat_lon = random_street_view.getImage(ELEGIDO)
    return lat_lon

def getAddress(lat_lon):
    URL_REVERSE = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + lat_lon + "&key=AIzaSyC7e8qywg4vWmaj7nJvEfSWRHOUdsiCp30&language=ES"
    response = requests.get(URL_REVERSE)
    data = response.json()
    return data['results'][0]['formatted_address']

def createGif():
    size = 320, 320
    Image.open(HOME_PATH + "/images/img_test.jpg").convert('RGBA').save(HOME_PATH + "/images/img_test.png","PNG")
    old_background = Image.open(HOME_PATH + "/images/img_test.png")
    old_background.thumbnail(size, Image.ANTIALIAS)
    old_background.save(HOME_PATH + "/images/img_test.png")
    images = []
    for x in range(0, 52):
        y = str(x)
        src = HOME_PATH + "/images/img_test.png"
        dst = HOME_PATH + "/images/temp/bg_" + y + ".png"
        copyfile(src, dst)

        background = Image.open(HOME_PATH + "/images/temp/bg_" + y + ".png")
        foreground = Image.open(HOME_PATH + "/images/fort/frame_" + y + ".png")
        background.paste(foreground, (100, 130), foreground)
        background.save(HOME_PATH + "/images/temp/bg_" + y + ".png")
        tempImage = Image.open(HOME_PATH + "/images/temp/bg_" + y + ".png")
        images.append(tempImage)
    # background.show()
    # images = [Image.open(image) for image in glob.glob(HOME_PATH + "/images/temp/*")]
    filename = HOME_PATH + "/images/test.gif"
    gifcreator.writeGif(filename, images, duration=0.1)
    return "HOLA"

def getApi():
    cfg = config.getTwitterKeys()
    twitter = Twython(cfg['consumer_key'], cfg['consumer_secret'],cfg['access_token'], cfg['access_token_secret'])
    return twitter

def sendTweet(address):
    api = getApi()
    tweet = "Ricardo Fort en " + address
    photo = open(HOME_PATH + '/images/test.gif', 'rb')
    response = api.upload_media(media=photo)
    status = api.update_status(status=tweet, media_ids=[response['media_id']])
    print tweet

def main():
    address = getAddress(getImage())
    createGif()
    sendTweet(address)

# print "La latitud y la longitud son: " + lat_lon + " en el pais " + ELEGIDO
main()
