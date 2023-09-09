import math


locations = [
    {"name": "HOME", "lat": 53.1, "lon": 52.92},
    {"name": "FRIENDS", "lat": 1.15, "lon": 56.81},
    {"name": "WORK", "lat": 99.04, "lon": 72.66},
    {"name": "GROCERY", "lat": 38.56, "lon": 52.92},
    {"name": "GRANDPARENTS", "lat": 47.42, "lon": 68.9},
    {"name": "SCHOOL", "lat": 72.64, "lon": 87.04},
    {"name": "GYM", "lat": 27.34, "lon": 15.37},
    {"name": "BEACH", "lat": 73.37, "lon": 64.99},
    {"name": "MOUNTAIN", "lat": 60.55, "lon": 17.69},
    {"name": "PARIS", "lat": 67.49, "lon": 6.8}
]

def distance(x1, y1, x2, y2):
    return round(math.sqrt((x1-x2)**2 + (y1-y2)**2), 2)

def close_locations(radius, lat, lon):

    res = []

    for loc in locations:
        d = distance(loc["lat"], loc["lon"], lat, lon) 
        if d <= radius:
            loc["distance"] = d
            res.append(loc)

    res.sort(key=lambda loc: loc["distance"])

    return res

