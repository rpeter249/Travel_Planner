'''
Name : Python Bytes
Team Members : Kayla (kmcfarla) , David (dsanche2), Ruth (rpeter)
'''


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

'''
To install, use 'pip install amadeus'
'''
from amadeus import Client, ResponseError

''' 
API token insert here
'''

amadeus = Client(
    client_id='QUnGGNVNqBGVy5o8GmMzvwNsHQfGSy8C',
    client_secret='GswNEsgc1kAJeH76'
    )


def flight_info(origin, destination, departure_date, return_date):
    
    try:
        '''
        Get the response of the api for both the origin and destination
        '''
        origin_response = amadeus.reference_data.locations.get(
            subType='CITY',
            keyword=origin
            )
        
        dest_response = amadeus.reference_data.locations.get(
            subType='CITY',
            keyword=destination
            )
        
        '''
        Get the iata code ,if there is one, of both the origin 
        and destination
        '''
        
        if (origin_response.data == [] or dest_response.data == []):
            return None
        
        origin_iata = origin_response.data[0]['iataCode']
        print(origin_iata)
        dest_iata = dest_response.data[0]['iataCode']
        print(dest_iata)

        if (origin_iata == "" or dest_iata == ""):
            print('No valid airline')
            return None
        else:
            '''
            Get all flight info given origin, destination, departure date,
            and return date, with a maximum of 10 flights
            '''
            flight_response = amadeus.shopping.flight_offers_search.get(
                originLocationCode=origin_iata,
                destinationLocationCode=dest_iata,
                departureDate=departure_date,
                returnDate=return_date,
                adults=1,
                nonStop='true',
                currencyCode='USD',
                max=10
                )
            
            if (flight_response.data == []):
                return None
            
            flights = []
            for flight in flight_response.data:
                info = dict()
                
                itinerary1 = {'duration':str(pd.Timedelta(flight['itineraries'][0]['duration'])),
                              'departure':flight['itineraries'][0]['segments'][0]['departure']['iataCode'],
                              'departure_time':flight['itineraries'][0]['segments'][0]['departure']['at'],
                              'arrival':flight['itineraries'][0]['segments'][0]['arrival']['iataCode'],
                              'arrival_time':flight['itineraries'][0]['segments'][0]['arrival']['at']}
                
                itinerary2 = {'duration':str(pd.Timedelta(flight['itineraries'][1]['duration'])),
                              'departure':flight['itineraries'][1]['segments'][0]['departure']['iataCode'],
                              'departure_time':flight['itineraries'][1]['segments'][0]['departure']['at'],
                              'arrival':flight['itineraries'][1]['segments'][0]['arrival']['iataCode'],
                              'arrival_time':flight['itineraries'][1]['segments'][0]['arrival']['at']}
                
                info.update({'itinerary1':itinerary1})
                info.update({'itinerary2':itinerary2})
                info.update({'price':float(flight['price']['total'])})
                
                flights += [info]
                
            return flights
    except ResponseError:
        print('Not a valid city')
        return None
