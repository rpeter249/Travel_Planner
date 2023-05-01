'''
Name : Python Bytes
Team Members : Kayla (kmcfarla) , David (dsanche2), Ruth (rpeter)
'''


import requests
from bs4 import BeautifulSoup

city_list = {'new york': 'New York City'}
#  This function scrapes https://www.holidify.com/ for hotels given a city
#  It returns 20 different hotel options along with the starting price for them
def scrapeHolidify(destination):

    destination = city_list.get(destination, destination).replace(" ", "-").lower()
    dest = destination
    url = f"https://www.holidify.com/places/{destination}/hotels-where-to-stay.html"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # On holidify, the hotels are grouped by cards (which contains hotel name & price)
    hotelSummary = soup.find(id="hotelSummary")
    hotelNames = hotelSummary.find_all(class_="card-heading")
    hotelPrices = hotelSummary.find_all(class_="price default")

    hotels = list()

    # pick top 20 hotels
    for i in range(20):
        name = hotelNames[i].get_text().strip()
        price = hotelPrices[i].get_text().strip()
        hotels.append((name, price))

    print(f"\n\nTop 20 Hotels in {dest}:\n-----------------------------")

    for hotel in hotels:
        name, price = hotel
        print(f"{name}, {price}\n")

    return hotels

# scrapeHolidify("New York City")
# scrapeHolidify("Las Vegas")
# scrapeHolidify("Los Angeles")
