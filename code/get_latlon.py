#!/usr/bin/env python2.7 -B

import sys
import urllib2
import json
from numpy import nan


def from_address(address):
    """Get the latitude and longitude of an address or location.

    INPUT: str -- address or location
    OUTPUT: tupled (lat, lon) -- top result of google map api search 
    """

    baseurl = "http://maps.googleapis.com/maps/api/geocode/json?address={}&sensor=false"
    url = baseurl.format(urllib2.quote(address))

    request = urllib2.Request(url)
    print 'query: {}'.format(url)

    try:
        page = urllib2.urlopen(request)
    except urllib2.URLError, e:
        if hasattr(e, 'reason'):
            print 'Failed to reach url'
            print 'Reason: ', e.reason
            sys.exit()
        elif hasattr(e, 'code'):
            if e.code == 404:
                print 'Error: ', e.code
                sys.exit()

    results = json.loads(page.read(), strict=False)['results']

    coords = []
    for result in results:
        lat = result['geometry']['location']['lat']
        lon = result['geometry']['location']['lng']
        coords.append((lat, lon))

    if not coords:
        print "not found: {}".format(address) 
        coords = [(nan, nan)]

    return coords[0]


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print "search: {}".format(sys.argv[1])
        print from_address(sys.argv[1])
