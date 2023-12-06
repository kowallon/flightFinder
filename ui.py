import tkinter as tk
from tkcalendar import DateEntry
from flight_search import FlighSearch
from datetime import datetime
import webbrowser



class FlightSearchUi:
    def __init__(self, root):
        self.root = root
        self.root.title("Flight Search")

        # Header
        header_label = tk.Label(root, text="Flight Search", font=("Helvetica", 16))
        header_label.grid(row=0, column=0, columnspan=4, pady=10)

        # Origin City
        origin_label = tk.Label(root, text="Origin City:")
        origin_label.grid(row=1, column=0)
        self.origin_entry = tk.Entry(root)
        self.origin_entry.grid(row=1, column=1)

        # Destination City
        dest_label = tk.Label(root, text="Destination City:")
        dest_label.grid(row=1, column=2)
        self.dest_entry = tk.Entry(root)
        self.dest_entry.grid(row=1, column=3)

        # Direct Flight Checkbox
        self.direct_flight_var = tk.IntVar()
        direct_flight_check = tk.Checkbutton(root, text="Direct flight only", variable=self.direct_flight_var,
                                             command=self.get_state)
        direct_flight_check.grid(row=2, column=0, columnspan=2)

        print(f"wartosc checkboxa: {self.direct_flight_var.get()}")

        # Start Date Calendar
        start_date_label = tk.Label(root, text="Start Date:")
        start_date_label.grid(row=2, column=2)
        self.start_date_entry = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2,
                                          date_pattern='dd/mm/yyyy'
                                          )
        self.start_date_entry.grid(row=2, column=3)

        # Last Date Calendar
        last_date_label = tk.Label(root, text="Last Date:")
        last_date_label.grid(row=3, column=0)
        self.last_date_entry = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2,
                                         date_pattern='dd/mm/yyyy')
        self.last_date_entry.grid(row=3, column=1)

        # Min Trip Length
        trip_length_label = tk.Label(root, text="Min trip Length:")
        trip_length_label.grid(row=3, column=2)
        self.trip_length_entry = tk.Entry(root)
        self.trip_length_entry.grid(row=3, column=3)

        # Max Trip Length
        max_trip_length_label = tk.Label(root, text="Max trip Length:")
        max_trip_length_label.grid(row=3, column=4)
        self.max_trip_length_entry = tk.Entry(root)
        self.max_trip_length_entry.grid(row=3, column=5)

        # Search Button
        search_button = tk.Button(root, text="Search", command=self.search_flights)
        search_button.grid(row=4, column=0, columnspan=4, pady=10)

        # Results
        results_label = tk.Label(root, text="Results:")
        results_label.grid(row=5, column=0, columnspan=4, pady=5)

        # Results Table
        table_headers = ["Origin City", "Destination City", "Departure Day", "Return Day", "Price", "Link to Buy"]
        self.header_labels = []
        for col, header in enumerate(table_headers):
            header_label = tk.Label(root, text=header, relief=tk.GROOVE, width=15)
            header_label.grid(row=6, column=col)
            self.header_labels.append(header_label)

        # Initialize result labels (you'll update these dynamically when the search is performed)
        self.result_labels = []


    def get_state(self):
        state = self.direct_flight_var.get()
        print(state)

    def open_link(self, url):
        webbrowser.open(url)

    def search_flights(self):

        results = FlighSearch()

        origin = self.origin_entry.get()
        destination = self.dest_entry.get()
        date_from = self.start_date_entry.get()
        date_to = self.last_date_entry.get()
        min_stay = self.trip_length_entry.get()
        max_stay = self.max_trip_length_entry.get()

        flight_data = results.search(starting_city=origin,
                           destination_city=destination,
                           date_from=date_from,
                           date_to=date_to,
                           minimal_stay=min_stay,
                           max_stay=max_stay,
                           stopovers=self.direct_flight_var.get()
                       )
        if type(flight_data) == str:
            wrong_date = tk.Label(self.root, text=flight_data)
            wrong_date.grid(row=6, column=0, columnspan=4, pady=5)
            for header_label in self.header_labels:
                header_label.grid_forget()
        else:

            try:
                city_from = flight_data.json()['data'][0]['cityFrom']
                airport_from_1 = flight_data.json()['data'][0]['flyFrom']
                city_to = flight_data.json()['data'][0]['cityTo']
                airport_to_1 = flight_data.json()['data'][0]['flyTo']

                airport_from_2 = flight_data.json()['data'][1]['flyFrom']
                airport_to_2 = flight_data.json()['data'][1]['flyTo']

                airport_from_3 = flight_data.json()['data'][2]['flyFrom']
                airport_to_3 = flight_data.json()['data'][2]['flyTo']

                departure_day = flight_data.json()['data'][0]['route'][0]['local_departure']
                formatted_departure = datetime.fromisoformat(departure_day[:-1]).strftime("%d/%m/%Y")

                return_day = flight_data.json()['data'][0]['route'][1]['local_departure']
                formatted_return = datetime.fromisoformat(return_day[:-1]).strftime("%d/%m/%Y")

                departure_day_2 = flight_data.json()['data'][1]['route'][0]['local_departure']
                formatted_departure_2 = datetime.fromisoformat(departure_day_2[:-1]).strftime("%d/%m/%Y")

                return_day_2 = flight_data.json()['data'][1]['route'][1]['local_departure']
                formatted_return_2 = datetime.fromisoformat(return_day_2[:-1]).strftime("%d/%m/%Y")

                departure_day_3 = flight_data.json()['data'][2]['route'][0]['local_departure']
                formatted_departure_3 = datetime.fromisoformat(departure_day_3[:-1]).strftime("%d/%m/%Y")

                return_day_3 = flight_data.json()['data'][2]['route'][1]['local_departure']
                formatted_return_3 = datetime.fromisoformat(return_day_3[:-1]).strftime("%d/%m/%Y")

            #print(flight_data.json())

                table_results = [
                    [f"{city_from} - {airport_from_1}", f"{city_to} - {airport_to_1}", formatted_departure, formatted_return,
                     f"{flight_data.json()['data'][0]['price']} zł", flight_data.json()['data'][0]['deep_link']],

                    [f"{city_from} - {airport_from_2}", f"{city_to} - {airport_to_2}", formatted_departure_2, formatted_return_2,
                     f"{flight_data.json()['data'][1]['price']} zł", flight_data.json()['data'][1]['deep_link']],

                    [f"{city_from} - {airport_from_3}", f"{city_to} - {airport_to_3}", formatted_departure_3, formatted_return_3,
                     f"{flight_data.json()['data'][2]['price']} zł", flight_data.json()['data'][2]['deep_link']]
                ]

                # Clear previous results
                for label in self.result_labels:
                    label.grid_forget()

                # Display new results
                for row, result in enumerate(table_results):
                    for col, value in enumerate(result):
                        label = tk.Label(self.root, text=value, relief=tk.GROOVE, width=15)

                        # Check if the value is a URL and make it clickable
                        if col == 5 and value.startswith("http"):
                            label.config(fg="blue", cursor="hand2", text="Buy")
                            label.bind("<Button-1>", lambda event, url=value: self.open_link(url))

                        label.grid(row=row + 7, column=col)
                        self.result_labels.append(label)


            except AttributeError:
                no_results = tk.Label(root, text="Unfortunately no flights were found")
                no_results.grid(row=6, column=0, columnspan=4, pady=5)
                for header_label in self.header_labels:
                    header_label.grid_forget()



if __name__ == "__main__":
    root = tk.Tk()
    app = FlightSearchUi(root)
    root.mainloop()
