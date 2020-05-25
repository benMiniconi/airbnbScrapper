import re
import csv
import os
from os import path

pricePattern = ["[0-9]{1},[0-9]{2,4}€", "[0-9]{1},[0-9]{2,4},[0-9]{2}€", "[0-9]{2,4}€"]
chambresPattern = ["[0-9] chambres"]
sdbPattern = ["[0-9] salles de", "[0-9] salle de", ]
airBnBresearchDic = {17: {"label": "UniqueKey"}, 20: {"label": "Titre de l'annonce"},
                     28: {"label": "Prix par nuit", "regex": "D"}, 23: {"label ": "Détails du Logement"},
                     24: {"label": "ExtraInformation"}}
piscinePattern = ["piscine"]
habitationType = ["villa", "chambre individuelle", "appartement"]


def extraxtCity(libele, cityList):
    for city in cityList:
        match = re.findall(city, libele)
        if len(match) > 0:
            print(match)
            return match[0]


def extractPiscine(libele):
    for pattern in piscinePattern:
        match = re.findall(pattern, libele)
        if len(match) > 0:
            return True


def extractTpeHabitation(libele):
    for pattern in habitationType:
        match = re.findall(pattern, libele)
        if len(match) > 0:
            return match[0]


def extractPricePerNight(libele):
    for pattern in pricePattern:
        match = re.findall(pattern, libele)
        if len(match) > 0 and len(re.findall("total", libele.lower())) == 0:
            return re.split("€", match[0])[0]


def extractNbChambres(libele):
    for pattern in chambresPattern:
        match = re.findall(pattern, libele)
        if len(match) > 0:
            return re.findall("[0-9]", match[0])[0]


def extractNbSDB(libele):
    for pattern in sdbPattern:
        match = re.findall(pattern, libele)
        if len(match) > 0:
            return re.findall("[0-9]", match[0])[0]


def extractAnnonceId(libele):
    match = re.findall("/[0-9]{6,10}", libele)
    if len(match) > 0:
        return match[0].replace("/", "")


def exportResult(annoncesList, city, periode):
    csv_columns = annoncesList[0].keys()
    csv_file = "airbnblist" + city + periode + ".csv"

    if path.exists(csv_file):
            csv_size = os.stat(csv_file).st_size
            try:
                with open(csv_file, 'a+') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                    if csv_size == 0:
                        writer.writeheader()
                    for data in annoncesList:
                        writer.writerow(data)
            except IOError:
                print("I/O error")
    else:
        try:
            with open(csv_file, 'w+') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for data in annoncesList:
                    writer.writerow(data)
        except IOError:
            print("I/O error")


def getNextPages(soup):
    pagesList = soup.find_all("li", {"data-id": re.compile("page-")})
    pages = []
    for page in pagesList:
        nextUrl = page.next
        if nextUrl.name == "a":
            pages.append("https://www.airbnb.fr" + nextUrl.attrs["href"])
        else:
            pages.append("current")
    return pages


def getCurrentPage(soup):
    pagesList = soup.find_all("li", {"data-id": re.compile("page-")})
    pages = []
    for pageKey in range(0, len(pagesList)):
        nextUrl = pagesList[pageKey].next
        pages.append(nextUrl.name)
    return pages
