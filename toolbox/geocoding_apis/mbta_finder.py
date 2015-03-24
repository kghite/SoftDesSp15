"""
Geocoding and Web APIs Project Toolbox exercise

Find the MBTA stops closest to a given location.

Full instructions are at:
https://sites.google.com/site/sd15spring/home/project-toolbox/geocoding-and-web-apis
"""

import urllib   # urlencode function
import urllib2  # urlopen function (better than urllib version)
import json
import string
from pprint import pprint


# Useful URLs (you need to add the appropriate parameters for your requests)
GMAPS_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
MBTA_BASE_URL = "http://realtime.mbta.com/developer/api/v2/stopsbylocation"
MBTA_DEMO_API_KEY = "wX9NwuHnZU2ToO7GmGR9uw"

def get_lat_long(place_name):
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.

    See https://developers.google.com/maps/documentation/geocoding/
    for Google Maps Geocode API URL formatting requirements.
    """
    place_name = place_name.replace(' ', '%20').strip()
    url = GMAPS_BASE_URL + "?address=" + place_name
    f = urllib2.urlopen(url)
    response_text = f.read()
    response_data = json.loads(response_text)
    lat = response_data["results"][0]["geometry"]["location"]["lat"]
    lng = response_data["results"][0]["geometry"]["location"]["lng"]
    return(lat, lng)


def get_nearest_station(coordinates):
    """
    Given latitude and longitude strings, return a (station_name, distance)
    tuple for the nearest MBTA station to the given coordinates.

    See http://realtime.mbta.com/Portal/Home/Documents for URL
    formatting requirements for the 'stopsbylocation' API.
    """
    place = "&lat=" + str(coordinates[0]) + "&lon=" + str(coordinates[1]) + "&format=json"
    key = "?api_key=" + MBTA_DEMO_API_KEY
    url = MBTA_BASE_URL + key + place
    f = urllib2.urlopen(url)
    response_text = f.read()
    response_data = json.loads(response_text)
    closest_stop_name = response_data["stop"][0]["stop_name"]
    closest_stop_dist = response_data["stop"][0]["distance"]
    return closest_stop_name, closest_stop_dist

def find_stop_near(place_name):
    """
    Given a place name or address, print the nearest MBTA stop and the 
    distance from the given place to that stop.
    >>> find_stop_near("Fenway Park")
    (u'Brookline Ave opp Yawkey Way', u'0.0881209298968315')
    """
    nearest_stop = get_nearest_station(get_lat_long("Fenway Park"))
    print nearest_stop[0]
    print nearest_stop[1]
    print nearest_stop
    return nearest_stop

place_name = input('Enter your location enclosed in quotes: ')
find_stop_near(place_name)