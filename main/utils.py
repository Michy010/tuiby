from math import radians, cos, sin, asin, sqrt

# Our methods goes here
# The haversine method to calculate the difference in distance
def haversine(lon1, lat1, lon2, lat2):
    R = 6372.8

    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 -lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    a = sin(dLat/2)**2 + cos(lat1) * cos(lat2) * sin(dLon/2)**2
    c = 2*asin(sqrt(a))

    return R * c