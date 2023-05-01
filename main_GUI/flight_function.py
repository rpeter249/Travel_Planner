import requests
import json
import pandas as pd

'''
General overview of the method: 
Using the skyscanner API, and using an origin and a destination string
location as an input
(cities), I will 
1) Get IATA codes from city of origin as well as destination 
2) Use IATA codes and dates to get flight info
3) filter flight info to get only the information we need
4) return a list of flight infos (maybe the first 10 or so)
'''


def flight_information(origin, destination, travel_date, return_date):
    '''
    travel_date, return_date: must be of the form: yyyy-mm-dd
    '''

    # define he url as well as the header
    url = "https://skyscanner50.p.rapidapi.com/api/v1/searchAirport"
    headers = {
        "X-RapidAPI-Key": "927611d5c5mshdc4877177c039a3p1cba94jsn144cdd17b204",
        "X-RapidAPI-Host": "skyscanner50.p.rapidapi.com"
    }

    ''' 
    Getting IATA code for Airports from the origin 
    '''
    origin = origin.lower()
    querystring = {"query": origin}
    origin_response = requests.get(url, headers=headers, params=querystring)
    origin_data = json.loads(origin_response.content.decode('utf-8'))
    print(origin_data)
    origin_airports = pd.DataFrame(origin_data['data'])

    ''' 
    Getting IATA code for airports from the destination 
    '''
    destination = destination.lower()
    querystring = {"query": destination}
    dest_response = requests.get(url, headers=headers, params=querystring)
    dest_data = json.loads(dest_response.content.decode('utf-8'))
    dest_airports = pd.DataFrame(dest_data['data'])

    '''
    Consider any data that isn't None
    '''
    origin_IATA = origin_airports['IataCode'][0]
    dest_IATA = dest_airports['IataCode'][0]

    ''' Searching flights given the origin and destination IATA code '''
    url = "https://skyscanner50.p.rapidapi.com/api/v1/searchFlights"
    querystring = {"origin": origin_IATA, "destination": dest_IATA, "date": travel_date,
                   "returnDate": return_date, "currency": "USD",
                   "countryCode": "US", "market": "en-US"}
    headers = {
        "X-RapidAPI-Key": "927611d5c5mshdc4877177c039a3p1cba94jsn144cdd17b204",
        "X-RapidAPI-Host": "skyscanner50.p.rapidapi.com"
    }

    ''' Getting the flight info '''
    flight_response = requests.get(url, headers=headers, params=querystring)
    flight_data = json.loads(flight_response.content.decode('utf-8'))
    # all_flights = pd.DataFrame(flight_data['data'])
    print(flight_data)

    flights = []

    for flight in flight_data['data']:
        info = dict()

        leg0 = {'origin': flight['legs'][0]['origin']['name'],
                'destination': flight['legs'][0]['destination']['name'],
                'departure': flight['legs'][0]['departure'],
                'arrival': flight['legs'][0]['arrival'],
                'duration': flight['legs'][0]['duration'],
                'price': flight['price']['amount']}

        leg1 = {'origin': flight['legs'][1]['origin']['name'],
                'destination': flight['legs'][1]['destination']['name'],
                'departure': flight['legs'][1]['departure'],
                'arrival': flight['legs'][1]['arrival'],
                'duration': flight['legs'][1]['duration'],
                'price': flight['price']['amount']}

        info.update({'leg0': leg0})
        info.update({'leg1': leg1})

        flights += [info]

    return flights
