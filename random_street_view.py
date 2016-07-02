import argparse
import os
import random
import shapefile  # http://code.google.com/p/pyshp/
import sys
import urllib
import getcolor
import config

# Optional, http://stackoverflow.com/a/1557906/724176
try:
    import timing
except:
    pass

# Determine if a point is inside a given polygon or not
# Polygon is a list of (x,y) pairs.
# http://www.ariel.com.au/a/python-point-int-poly.html
def point_inside_polygon(x, y, poly):
    n = len(poly)
    inside = False
    p1x, p1y = poly[0]
    for i in range(n+1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def getImage(country):
    HOME_PATH = os.path.dirname(os.path.realpath(__file__))
    API_KEY = config.getKey()
    GOOGLE_URL = ("http://maps.googleapis.com/maps/api/streetview?sensor=false&"
                  "size=640x640&key=" + API_KEY)
    IMG_PREFIX = "img_"
    IMG_SUFFIX = ".jpg"

    print "Loading borders"
    shape_file = HOME_PATH + "/TM_WORLD_BORDERS-0.3.shp"
    if not os.path.exists(shape_file):
        print("Cannot find " + shape_file + ". Please download it from "
              "http://thematicmapping.org/downloads/world_borders.php "
              "and try again.")
        sys.exit()

    sf = shapefile.Reader(shape_file)
    shapes = sf.shapes()

    print "Finding country"
    for i, record in enumerate(sf.records()):
        if record[2] == country.upper():
            print record[2], record[4]
            print shapes[i].bbox
            min_lon = shapes[i].bbox[0]
            min_lat = shapes[i].bbox[1]
            max_lon = shapes[i].bbox[2]
            max_lat = shapes[i].bbox[3]
            borders = shapes[i].points
            break

    print "Getting images"
    attempts, country_hits, imagery_hits, imagery_misses = 0, 0, 0, 0
    MAX_URLS = 25000
    IMAGES_WANTED = 1

    try:
        while(True):
            attempts += 1
            rand_lat = random.uniform(min_lat, max_lat)
            rand_lon = random.uniform(min_lon, max_lon)
            # print attempts, rand_lat, rand_lon
            # Is (lat,lon) inside borders?
            if point_inside_polygon(rand_lon, rand_lat, borders):
                print "  In country"
                country_hits += 1
                lat_lon = str(rand_lat) + "," + str(rand_lon)
                outfile = os.path.join(
                    HOME_PATH + '/images', IMG_PREFIX + 'test' + IMG_SUFFIX)
                url = GOOGLE_URL + "&location=" + lat_lon
                try:
                    urllib.urlretrieve(url, outfile)
                except KeyboardInterrupt:
                    sys.exit("exit")
                except:
                    pass
                if os.path.isfile(outfile):
                    print lat_lon
                    # get_color returns the main color of image
                    color = getcolor.get_color(outfile)
                    print color
                    if color[0] == '#e3e2dd' or color[0] == "#e3e2de":
                        print "    No imagery"
                        imagery_misses += 1
                        os.remove(outfile)
                    else:
                        print "    ========== Got one! =========="
                        imagery_hits += 1
                        if imagery_hits == IMAGES_WANTED:
                            break
                if country_hits == MAX_URLS:
                    break
    except KeyboardInterrupt:
        print "Keyboard interrupt"

    print "Attempts:\t", attempts
    print "Country hits:\t", country_hits
    print "Imagery misses:\t", imagery_misses
    print "Imagery hits:\t", imagery_hits

    return lat_lon
# End of file
