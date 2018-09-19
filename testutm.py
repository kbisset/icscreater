#!/opt/local/bin/python2.7
# This Python file uses the following encoding: utf-8

import utm
# N37° 10.83'	W121° 59.95'

ZONE_LETTERS = "CDEFGHJKLMNPQRSTUVWXX"

def latitude_to_zone_letter(latitude):
    if -80 <= latitude <= 84:
        print "Z", latitude, int(Number(latitude)+80) , int(latitude+80)>>3
        return ZONE_LETTERS[int(latitude + 80) >> 3]
    else:
        return None


def latlon_to_zone_number(latitude, longitude):
    if 56 <= latitude < 64 and 3 <= longitude < 12:
        return 32

    if 72 <= latitude <= 84 and longitude >= 0:
        if longitude <= 9:
            return 31
        elif longitude <= 21:
            return 33
        elif longitude <= 33:
            return 35
        elif longitude <= 42:
            return 37

    return int((longitude + 180) / 6) + 1

lat = 37.1805
lon = -121.999
print utm.from_latlon(lat, lon)

print latlon_to_zone_number(lat, lon)
print latitude_to_zone_letter(lat)
