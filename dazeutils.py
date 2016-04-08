from datetime import date
from datetime import timedelta
import json
import sys
import os


locationLog = '/Users/mikayla/Code/sandbox/python/daze/newLocationLog.json'

class Daze:
    def __init__(self, json):
        self.json = json
        self.deserialize(json)


    def findPlace(self, placename):
        for (p, alts) in self.places.items():
            if placename == p:
                return p
            if placename in alts:
                return p
        return None


    def serialize(self):
        return {'places': self.places,
                'log': {k.isoformat():v for (k, v) in self.dateDict.items()}
               }


    def deserialize(self, dazejson):
        self.places = dazejson['places']
        self.dateDict = {toDate(k):self.findPlace(v) for (k, v) in dazejson['log'].items()}
        self.placeDict = {k:[] for k in self.places.keys()}
        for (d, p) in self.dateDict.items():
            try:
                self.placeDict[self.findPlace(p)].append(d)
            except KeyError:
                print(p)
                print(self.findPlace(p))


    def add(self, indate, place):
        if type(indate) is str:
            indate = toDate(indate)
        if place not in self.places.keys():
            place = self.findPlace(place)

        self.dateDict[indate] = place
        self.placeDict[place].append(indate)


    def remove(self, outdate):
        if type(outdate) is str:
            outdate = toDate(outdate)
        place = self.dateDict.pop(outdate)
        self.placeDict[place].remove(outdate)


    def summarize(self, firstdate=date.min, lastdate=date.max):
        summary = {}
        def isInDateRange(xdate):
            return firstdate <= xdate <= lastdate

        for p in self.places.keys():
            summary[p] = len(list(filter(isInDateRange, self.placeDict[p])))

        actualfirst = max(firstdate, min(self.dateDict.keys()))
        actuallast = min(lastdate, max(self.dateDict.keys()))

        return summary, sum(summary.values()), actualfirst, actuallast




def toDate(datestring):
    return date(*[int(x) for x in datestring.split('-')])


def fileToDaze(filename):
    if filename is None:
        try:
            with open(os.path.expanduser("~/.daze/settings.json"), 'r') as f:
                settings = json.load(f)
            filename = os.path.expanduser(settings['log'])
        except:
            print("Had an error getting log file from settings.")
            filename = locationLog
    with open(filename, 'r') as f:
        data = json.load(f)
    return Daze(data)

def dazeToFile(daze, filename):
    if filename is None:
        try:
            with open(os.path.expanduser("~/.daze/settings.json"), 'r') as f:
                settings = json.load(f)
            filename = os.path.expanduser(settings['log'])
        except:
            print("Had an error getting log file from settings.")
            filename = locationLog
    with open(filename, 'w') as f:
        json.dump(daze.serialize(), f)

