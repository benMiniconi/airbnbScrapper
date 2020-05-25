from bs4 import BeautifulSoup
import requests
import moment
from datetime import datetime
from airbnbscrappercleaner.airbnbscrapperengine import getAnnonces, getDetailedAnnonce, getNextPages, getCurrentPage, searchNextPage



checkIn = moment.date("23/06/2020")
checkOut = moment.date("30/06/2020")

for key in range(0, 52):
    checkIn = checkIn.add(days=7)
    checkOut = checkOut.add(days=7)
    print("Periode:", checkIn.format("DD/MMMM/YYYY"), "key", key)
    print("Periode Fin:", checkOut.format("DD/MMMM/YYYY"), "key", key)
    url = "https://www.airbnb.fr/s/Lourmarin/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&source=structured_search_input_header&search_type=search_query&checkin="+checkIn.format("YYYY-MM-DD")+"1&checkout="+checkOut.format("YYYY-MM-DD")+"&query=Lourmarin&place_id=ChIJhRMRhe8YyhIR77MVXxVjb8M&price_min=200"
    print(url)
    searchNextPage(url, checkIn.format("DD/MM/YYYY"), "Lourmarin", checkIn.format("MMMMYYYY"))



