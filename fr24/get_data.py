from FlightRadar24.api import FlightRadar24API
from pprint import pprint

fr_api = FlightRadar24API()


def get_flight_details(details):
    # airline_name = details["airline"]["name"]

    try:
        photo_url = details["aircraft"]["images"]["large"][0]["link"]
    except TypeError:
        photo_url = None

    try:
        aircraft_model = details["aircraft"]["model"]["text"]
    except TypeError:
        aircraft_model = "N/A"

    try:
        aircraft_reg = details["aircraft"]["registration"]
    except TypeError:
        aircraft_reg = "N/A"

    try:
        destination_airport = f'{details["airport"]["destination"]["code"]["iata"]} - {details["airport"]["destination"]["name"]}, {details["airport"]["destination"]["position"]["country"]["name"]}'
    except TypeError:
        destination_airport = "N/A"

    try:
        origin_airport = f'{details["airport"]["origin"]["code"]["iata"]} - {details["airport"]["origin"]["name"]}, {details["airport"]["origin"]["position"]["country"]["name"]}'
    except TypeError:
        origin_airport = "N/A"

    try:
        flight_number = details["identification"]["number"]["default"]
    except TypeError:
        flight_number = "N/A"

    info = f"{aircraft_model} - {aircraft_reg}\n" \
           f"Flight {flight_number}\n" \
           f"From:  {origin_airport}\n" \
           f"To:  {destination_airport}"
    return {"photo": photo_url, "info": info}


def get_flights(airline_icao):
    airline_flights = fr_api.get_flights(airline=airline_icao)
    flights_list = []
    for flight in airline_flights:
        details = fr_api.get_flight_details(flight.id)
        flights_list.append(get_flight_details(details))
    return flights_list
