import requests
from bs4 import BeautifulSoup
from time import time
import csv
import argparse
import sys

def parse(locality):
    print "Scraper Inititated for Locality:%s"%locality
    print "Finding search result page URL"
    geo_url = 'https://www.tripadvisor.com/TypeAheadJson?action=API&startTime='+str(int(time()))+'&uiOrigin=GEOSCOPE&source=GEOSCOPE&interleaved=true&types=geo,theme_park&neighborhood_geos=true&link_type=hotel&details=true&max=12&injectNeighborhoods=true&query='+locality
    api_response  = requests.get(geo_url).json()
    #getting the TA url for th equery from the autocomplete response
    url_from_autocomplete = "http://www.tripadvisor.com"+api_response['results'][0]['url']
    print 'URL found %s'%url_from_autocomplete
    geo = api_response['results'][0]['value'] 

    r = requests.get(url_from_autocomplete)
    soup = BeautifulSoup(r.text, "html.parser")

   


if __name__ == '__main__':    
    locality = sys.argv[1]
    print("Locality = " + locality)

    data = parse(locality)
    