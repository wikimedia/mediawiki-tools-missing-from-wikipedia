#!/usr/bin/python
#encoding:utf-8
# Copyright 2013 Sumana Harihareswara
# GPL
# The point of this script is to take a giant list of 2126 names from the Dictionary of African Biography Oxford Reference, check which names do not have an English Wikipedia entry, and then spit out that resultant set.
# Note: to find out who actually did have an entry, do a simple set operation for difference between set(pagelist) and set(starterlist)

# testlist= [u'Kayibanda, Grégoire',u'Kayoya, Michel',u'Kazahendike, Urieta',u'Kazibwa, Specioza Wandira',u'Kebede Mikael',u'Keen, John',u'Keino, Kip',u'Kéita, Aoua',u'Keita, Fodéba',u'Keïta, Modibo',u'Keïta, Salif',u'Keïta, Seydou']

import requests
import pprint
import codecs

def getnamelist(filename):
    """Open the file and turn it into a list split up by newlines."""
    with codecs.open(filename, encoding='utf-8') as f:
        fstr = f.read()
        namelist = fstr.split("\n")
    return namelist

def massagenames(nlist):
    """massage each name in a list to make it firstname lastname, return a list of old-and-new tuples"""
    mlist= map(lambda elem:" ".join(elem.split(", ")[::-1]), nlist)
    return zip(nlist, mlist)

def leftout(nametuples, resultfile):
    """return list of people who don't have pages on English Wikipedia

    for each name, do a search to see whether the page exists on english wikipedia
    sample title that does not exist: Narrrgh
    /w/api.php?action=query&prop=info&format=json&titles=Narrrgh: if ["query"]["pages"] has a negative int like -1, -2, etc. as a key, and if a key within that dict has the value "missing" (value: ""), then the page is missing from enwiki
    TODO: use pipes, e.g. Narrgh|Call Me Maybe|NEVEREXISTS in titles= , to make multiple queries at once. Can use chunks of up to 50 titles in 1 query. Right now it is ~1200 names; as long as I do them in series with a maxlag param, I think that is fine.
    Currently accepts redirects as meaning the page exists. TODO: if the redirect is to a page that is NOT a biography (e.g., it redirects to the page for a war), then count that person as unsung."""

    headers = {'User-Agent': 'Sumana Harihareswara prototype (http://github.com/brainwane) using Python requests library'}
    for namepair in nametuples:
        payload = dict(titles=namepair[1])
        r = requests.get("http://en.wikipedia.org/w/api.php?action=query&prop=info&format=json&redirects=&maxlag=5", params=payload, headers=headers)
        if "-1" in r.json()["query"]["pages"].keys():
            if "missing" in r.json()["query"]["pages"]["-1"].keys():
                outputfile(namepair[0]), resultfile)

# spit out list of who is left out

def outputfile(input, filename):
    with codecs.open(filename, encoding='utf-8', mode='a') as u:
        u.write(input)
        u.write("\n")

def run(listfile, resultfile):
    listofnames = getnamelist(listfile)
    querynames = massagenames(listofnames)
    leftout(querynames, resultfile)

run("namelist.txt", "unsung.txt")
