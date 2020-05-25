from bs4 import BeautifulSoup
import requests
import moment
from datetime import datetime
from airbnbscrappercleaner.airbnbscrapperengine import getAnnonces, getDetailedAnnonce, getNextPages, getCurrentPage, searchNextPage



checkIn = moment.date("01/13/2021")
checkOut = moment.date("01/17/2021")


for key in range(0, 26):
    checkIn = checkIn.add(days=7)
    checkOut = checkOut.add(days=7)
    print("Periode:", checkIn.format("DD/MMMM/YYYY"), "key", key)
    print("Periode Fin:", checkOut.format("DD/MMMM/YYYY"), "key", key)
    url = "https://www.airbnb.fr/s/M%C3%A9nerbes/homes?tab_id=all_tab&refinement_paths%5B%5D=%2Fhomes&query=M%C3%A9nerbes&place_id=ChIJObj6GvQPyhIRiO_3c_OrqGM&checkin="+checkIn.format("YYYY-MM-DD")+"&checkout="+checkOut.format("YYYY-MM-DD")+"&source=structured_search_input_header&search_type=search_query&price_min=200"
    print(url)
    searchNextPage(url, checkIn.format("DD/MM/YYYY"), "Menerbes", checkIn.format("MMMMYYYY"))



