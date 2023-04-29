import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

url_list = ["https://www.holidify.com/country/usa/places-to-visit.html"
    ,"https://www.holidify.com/country/usa/places-to-visit.html?pageNum=1","https://www.holidify.com/country/usa/places-to-visit.html?pageNum=2"]

places = []


for url in url_list :
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        for content_card in soup.find_all('div', {'class': 'content-card'}):
            href = content_card.find('a')['href']
            place_url = 'https://www.holidify.com/' + href
            place_response = requests.get(place_url)
            if place_response.status_code == 200:
                soup = BeautifulSoup(place_response.content, 'html.parser')
                ## fetch the state
                state_div = soup.find('div', {'class': 'mb-2 font-smaller'})
                state = state_div.find('a').text.strip()

                ## description, duration, best time
                description = soup.find('div', {'class': 'readMoreText'}).text.strip().replace("Read More", "")
                ideal_duration = soup.find_all('div', {'class': 'col-12 col-md-6'})[1].find('p') \
                    .text.strip().replace("Ideal duration:", "")
                best_time = soup.find_all('div', {'class': 'col-12 col-md-6'})[2].find('p') \
                    .text.strip().replace('Best Time:', '').replace("Read More", "")

                # fetch image
                div_element = soup.find('div', {'class': 'atf-cover-image'})
                style_attr = div_element['style']
                url_pattern = re.compile(r'url\(\'(.+?)\'\)')
                url_match = url_pattern.search(style_attr).group(1)

            else:
                print("Failed to get webpage content")

            card_heading = content_card.find('h3', {'class': 'card-heading'}).text.strip()
            rank = card_heading.split('.')[0]
            attraction = card_heading.split('.')[1]
            print(rank)
            places.append({'rank': rank, 'attraction': attraction, 'state': state,
                           'ideal_duration': ideal_duration, 'best_time': best_time, 'description': description,
                           'url_match': url_match})

        # Print the extracted data for all the places
        # for place in places:
        #     print(place['attraction'], place['href'], place['rank'], place['state'])

    else:
        print("Failed to get webpage content")

# create a sample dataframe
df = pd.DataFrame(places)

# generate the CSV file
df.to_csv('tourist_attractions.csv', index=False)
