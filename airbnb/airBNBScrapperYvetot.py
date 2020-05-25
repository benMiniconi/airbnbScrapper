from bs4 import BeautifulSoup
import requests
import moment
from datetime import datetime
from airbnbscrappercleaner.airbnbscrapperengine import getAnnonces, getDetailedAnnonce, getNextPages, getCurrentPage, searchNextPage



checkIn = moment.date("12/25/2020")
checkOut = moment.date("01/01/2021")


for key in range(0, 26):
    checkIn = checkIn.add(days=7)
    checkOut = checkOut.add(days=7)
    print("Periode:", checkIn.format("DD/MMMM/YYYY"), "key", key)
    print("Periode Fin:", checkOut.format("DD/MMMM/YYYY"), "key", key)
    url = "https://www.airbnb.fr/s/Yvetot/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&source=structured_search_input_header&search_type=search_query&checkin="+checkIn.format("YYYY-MM-DD")+"&checkout="+checkOut.format("YYYY-MM-DD")+"0&query=Yvetot&place_id=ChIJ-wMbgzH04EcRk5fhrtl6Bnw&price_min=200"
    print(url)
    searchNextPage(url, checkIn.format("DD/MM/YYYY"), "Yvetot", checkIn.format("MMMMYYYY"))



