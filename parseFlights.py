import json
import requests

all_flights = []

def parse_all_flights(scraped_datas, source, destination):
	print("IN HERE")

	file_name = "{0}-{1}-flight-results.json".format(source, destination)
	print(file_name)
	with open(file_name) as data_file:
		allFlights = json.load(data_file)

	for flight in allFlights:
		arrival = flight.get("arrival")
		arrival_airport = flight["timings"][0]["arrival_airport"]
		arrival_time = flight["timings"][0]["arrival_time"]
		departure_airport = flight["timings"][0]["departure_airport"]
		departure_time = flight["timings"][0]["departure_time"]
		airline = flight.get("airline")
		print(airline)

		flight_duration = flight.get("flight duration")
		plane_code = flight.get("plane code")
		plane = flight.get("plane")
		departure = flight.get("departure")
		stops = flight.get("stops")
		ticket_price = flight.get("ticket price")
		print(ticket_price)

		if float(ticket_price) < 201:
			price_category="p1"
		elif float(ticket_price) >=201 and float(ticket_price) <= 300:
			price_category="p2"
		elif float(ticket_price) >= 301 and float(ticket_price) <= 400:
			price_category="p3"
		elif float(ticket_price) >=401 and float(ticket_price) <= 500:
			price_category="p4"
		elif float(ticket_price) >= 501 and float(ticket_price) <= 600:
			price_category="p5"
		else:
			price_category="p6"

		airline_category = ""
		
		if airline == "Delta":
			airline_category = "Delta"
		elif airline == "American Airlines":
			airline_category = "AmericanAirlines"
		elif airline == "United":
			airline_category = "United"
		elif airline == "Frontier":
			airline_category = "Frontier"
		elif airline == "Jet Blue Airways":
			airline_category = "JetBlue"
		elif airline == "Spirit Airlines":
			airline_category = "Spirit"
		elif airline == "Alaska Airlines":
			airline_category = "Alaska"
		elif airline == "Sun Country Airlines":
			airline_category = "SunCountry"
		elif airline == "Virgin America":
			airline_category="VirginAmerica"

		#print(price_category)
		#print(airline_category)

		print("\n\n\n")


		all_flights.append([arrival, arrival_airport, arrival_time, departure_airport, departure_time, airline, flight_duration, plane_code, plane, departure, stops, ticket_price, price_category, airline_category])

		

	return all_flights
