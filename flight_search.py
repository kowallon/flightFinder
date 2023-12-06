import requests


class FlighSearch:

    def __init__(self):
        self.codes_header = {
            "apikey": "NSYyMj8JGNy7xQjtxrz7-apQtLzoqV1L"
        }
        self.base_url = "https://api.tequila.kiwi.com/v2/search"

    def get_iata(self, city_name):
        codes = requests.get(
                url=f"https://api.tequila.kiwi.com/locations/query?term={city_name}&locale=en-US&location_types=city",
                headers=self.codes_header)
        city_code = codes.json()['locations'][0]['code']
        return city_code


    def search(self, starting_city, destination_city, date_from, date_to, minimal_stay, max_stay, stopovers):

        if date_to < date_from:
            print("Wrong date")
            return "Departure date is after return date"

        starting_airport = self.get_iata(starting_city)
        destination_airport = self.get_iata(destination_city)

        if stopovers == 1:
            no_stopovers = "&max_stopovers=0"
        else:
            no_stopovers = ""


        flights = requests.get(
            url=f"{self.base_url}?fly_from={starting_airport}&fly_to={destination_airport}&date_from={date_from}&date_to={date_to}&nights_in_dst_from={minimal_stay}"
                f"&nights_in_dst_to={max_stay}&curr=PLN{no_stopovers}",
            headers=self.codes_header)

        try:
            print(flights.json()['data'][0])
            return flights
        except:
            return "No flights found"


#print(FlighSearch().search("LCJ", "AGP", "01/03/2024", "20/02/2024", "3", "10").json())




