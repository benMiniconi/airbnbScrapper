from bs4 import BeautifulSoup
import requests
import moment
from datetime import datetime
from airbnbscrappercleaner.airbnbscrapperengine import getAnnonces, getDetailedAnnonce, getNextPages, getCurrentPage, searchNextPage



checkIn = moment.date("06/23/2020")
checkOut = moment.date("06/30/2020")

"https://www.airbnb.fr/s/Saint~Martin~de~R%C3%A9/homes?refinement_paths%5B%5D=%2Fhomes&place_id=ChIJb35mS5z4A0gRAJLuYJLTBQQ&source=structured_search_input_header&search_type=filter_change&tab_id=home_tab&query=Saint-Martin-de-R%C3%A9%2C%20France&checkin=2020-06-01&checkout=2020-06-07&price_min=150&room_types%5B%5D=Entire%20home%2Fapt&property_type_id%5B%5D=2&property_type_id%5B%5D=36&property_type_id%5B%5D=11"

for key in range(0, 52):
    checkIn = checkIn.add(days=7)
    checkOut = checkOut.add(days=7)
    print("Periode:", checkIn.format("DD/MMMM/YYYY"), "key", key)
    print("Periode Fin:", checkOut.format("DD/MMMM/YYYY"), "key", key)
    url = "https://www.airbnb.fr/s/Saint~Martin~de~R%C3%A9--France/homes?place_id=ChIJb35mS5z4A0gRAJLuYJLTBQQ&refinement_paths%5B%5D=%2Fhomes&search_type=filter_change&tab_id=home_tab&query=Saint-Martin-de-R%C3%A9%2C%20France&checkin=" + checkIn.format(
        "YYYY-MM-DD") + "&checkout=" + checkOut.format(
        "YYYY-MM-DD") + "&adults=6&room_types%5B%5D=Entire%20home%2Fapt&amenities%5B%5D=7&price_min=250"
    print(url)
    searchNextPage(url, checkIn.format("DD/MM/YYYY"), "SaintMartin", checkIn.format("MMMMYYYY"))



