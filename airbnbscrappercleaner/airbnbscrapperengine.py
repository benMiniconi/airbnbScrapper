from bs4 import BeautifulSoup
import requests
import time
import moment
from datetime import datetime

import csv
import re
import pandas as pd
from coordonatesmodules import distancehelper
from airbnbscrappercleaner.airbnbcleaner import extraxtCity, extractNbSDB, extractNbChambres, extractPricePerNight, \
    extractAnnonceId, getNextPages, exportResult, getCurrentPage, extractPiscine, extractTpeHabitation

cityDF = pd.read_csv("villes_france_with_coord.csv")
elligibleCities = distancehelper.getElligibleCities(cityDF)
cityList = elligibleCities['villeLowerCase'].array




def getDetailedAnnonce(link, annonce):
    response = requests.get(link)
    time.sleep(5)
    data = response.text
    soup = BeautifulSoup(data, "html.parser")
    details = soup.find_all("a", {"class": re.compile("_")})
    detailsTitle = soup.find_all("h1")
    detailsEquipement = soup.find_all("div", {"data-plugin-in-point-id":"AMENITIES_DEFAULT"})
    if response.status_code != 200:
        #print("details", len(details))
    #else:
        print(response.status_code)
    # Extracting annonceId
    annonceId = extractAnnonceId(link)
    if annonceId:
        annonce["id"] = annonceId
    if annonceId:
        annonce["url"] = link
    rangeBounderies = 20 if len(details) > 20 else 0
    rangeBounderiesDebut = 5 if len(details) > 20 else 0
    for detail in detailsEquipement:
        equipements = detail.find_all(("div", {"class": re.compile("_")}))
        for equipment in equipements:
            rawText = equipment.text.lower().replace("-", " ").replace("'", " ").replace("é", "e").replace("è","e").replace(
            "à", "a")
            piscine = extractPiscine(rawText)
            if piscine:
                annonce["piscine"] = piscine

    for detail in detailsTitle:
        rawText = detail.text.lower().replace("-", " ").replace("'", " ").replace("é", "e").replace("è",
                                                                                                             "e").replace(
            "à", "a")
        typeH = extractTpeHabitation(rawText)
        if typeH:
            annonce["type"] = typeH
    #check bounderies size
    #print("detailedBounderis", rangeBounderies)
    for detail in range(rangeBounderiesDebut, rangeBounderies):
        # cleaning Label before extracting
        rawText = details[detail].text.lower().replace("-", " ").replace("'", " ").replace("é", "e").replace("è",
                                                                                                             "e").replace(
            "à", "a")
        # Extracting nb city
        # if len(re.findall("autres options a", rawText)) > 0:
        city = extraxtCity(rawText, cityList)
        if city:
            annonce["city"] = city




def getAnnonces(soup, periode, city, file):
    annonces = soup.find_all("div", {"itemprop": "itemListElement"})
    annoncesList = []
    for annonce in annonces:
        annonceDetail = {"pricePerNight": "", "nbChambres": "", "city": "", "zipCode": "", "nbSallesDeBain": "",
                         "Date": periode, "piscine": False, "url": "", "type": "",
                         "id": ""}
        logementDetails = annonce.findAll("span")
        logementOtherDetails = annonce.findAll("div")
        detailedLinkGet = annonce.findAll("a", {"href": re.compile("/rooms/")})
        detailedLink = "https://www.airbnb.fr" + detailedLinkGet[0].attrs["href"]
        detailKey = 0
        otherDetailKey = 0
        getDetailedAnnonce(detailedLink, annonceDetail)

        for otherDetailKey in range(0, len(logementOtherDetails)):
            # print("otherDetailsKey: ", otherDetailKey, logementOtherDetails[otherDetailKey].text)
            if logementOtherDetails[otherDetailKey].text:
                rawText = logementOtherDetails[otherDetailKey].text
                # ExtractingPricePerNight
                pricePerNight = extractPricePerNight(rawText)
                if pricePerNight:
                    annonceDetail["pricePerNight"] = pricePerNight
                # Extracting nb Chambres
                nbChambres = extractNbChambres(rawText)
                if nbChambres:
                    annonceDetail["nbChambres"] = nbChambres

                #piscine = extractPiscine(rawText)
                #if piscine:
                #    annonce["piscine"] = piscine

                # Extracting nb SDB
                nbSDB = extractNbSDB(rawText)
                if nbSDB:
                    annonceDetail["nbSallesDeBain"] = nbSDB

                # Extracting nb city
                # city = extraxCity(rawText)
                # if city:
                # annonceDetail["city"] = city

            otherDetailKey = otherDetailKey + 1
        annoncesList.append(annonceDetail)
    exportResult(annoncesList, city, file)


def searchNextPage(url, periode, city, file):
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, "html.parser")
    getAnnonces(soup, periode, city, file)
    currentPageList = getCurrentPage(soup)
    try:
        currentPage = currentPageList.index("div")
    except IndexError:
        currentPage = -1
    except ValueError:
        currentPage = -1


    pages = getNextPages(soup)
    print("currentPage", currentPage+1, "pageList", len(pages))
    if currentPage >= 0 and currentPage+1 < len(pages):
        if pages[currentPage+1] != url:
            searchNextPage(pages[currentPage+1], periode, city, file)


# tags = soup.find_all("div", {"itemprop": "itemListElement"})

# for tag in tags:
# print(tag.text)





