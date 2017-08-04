from __future__ import print_function
from flask import Flask, render_template, request
from flightData import getFlightData
from parseFlights import parse_all_flights
from getAirports import get_all_airports
from hotels import getHotels
from parseHotels import parse_all_hotels
import json
import requests
from lxml import html
from collections import OrderedDict
import argparse
import sys

app = Flask(__name__)

#use for maps
mapKey = "AIzaSyD_3OXGut2rO_V_aH1DFxuJdaqmHtlSofU"
global iteneraryItems 
global global_flight_list 
global start_date
global end_date
global city_name

class airport:
	def __init__(self, name, key, lat, lng):
		self.name = name
		self.key = key
		self.lat = lat
		self.lng = lng

'''
Right now i am having issues with multiple markers. i cant have the tuple i made here properly work with the html file.
However, if the data is on the html side it does work. REFERENCE test.html
We are also should store the information so that we dont backtrack but my idea is a list of lists ie
[[Airport1, Price1], [Airport2, Price2], ect]
price2 is amount of money from airport 1 to airport 2
We should also probably have them start and end at an airport. otherwise it might be too vauge for the result and our code.
Like do they want to be on the north side or south side of california?
Joey Testa
'''
airports = [
	airport('Tallhassee International Airport', 'TIA', 30.395412, -84.3472458),
	airport('Boston Logan International Airport', 'BOS', 42.3656132, -71.0117489),
	airport('Test', 'Te', 37.9045286, -122.1445772)]

destination = airports

airport_by_key = {airport.key: airport for airport in airports}

reload(sys)
sys.setdefaultencoding("utf-8")

@app.route("/")
def home():	
	allAirports = []
	allAirports = get_all_airports()
	for airportitem in allAirports:
		print(airportitem[0] + " " + airportitem[1])
	return render_template('home.html', airport_list = allAirports)

@app.route("/", methods = ["POST", "GET"])
def home_post():
	print("hereeeeeee!!")
	global start_date
	source = request.form['from_id']
	print("Source: " + str(source))
	destination = request.form['to_id']
	print("Destination: " + str(destination))
	date = request.form['date_id']
	print("Date " + str(date))
	start_date = str(date)

	argparser = argparse.ArgumentParser()
	argparser.add_argument('source',help = 'Source airport code')
	argparser.add_argument('destination',help = 'Destination airport code')
	argparser.add_argument('date',help = 'MM/DD/YYYY')

	print("Getting flight details")
	scraped_data = getFlightData(source, destination, date)
	print("Writing data to JSON file")

	if scraped_data == 'no data':
		return render_template('oops.html')


	else:
		with open('%s-%s-flight-results.json'%(source,destination),'w') as fp:
			json.dump(scraped_data,fp,indent = 4)

		flight_list = parse_all_flights(scraped_data, source, destination)
		global global_flight_list 
		global_flight_list = flight_list

		allAirports = []
		coords = []
		allAirports = get_all_airports()
		for airportitem in allAirports:

			if airportitem[1] == source:
				coords.append([airportitem[2], airportitem[3]])

			if airportitem[1] == destination:
				coords.append([airportitem[2], airportitem[3]])

		return render_template('map.html', flight_list = flight_list, temp=airport, destination=coords)


@app.route("/returnFlight", methods = ["POST", "GET"])
def return_flight_post():
	global end_date

	print("hereeeeeee!!")
	source = request.form['from_id']
	print("Source: " + str(source))
	destination = request.form['to_id']
	print("Destination: " + str(destination))
	date = request.form['date_id']
	print("Date " + str(date))
	end_date = str(date)

	argparser = argparse.ArgumentParser()
	argparser.add_argument('source',help = 'Source airport code')
	argparser.add_argument('destination',help = 'Destination airport code')
	argparser.add_argument('date',help = 'MM/DD/YYYY')

	print("Getting flight details")
	scraped_data = getFlightData(source, destination, date)
	print("Writing data to JSON file")

	if scraped_data == 'no data':
		return render_template('oops.html')


	else:
		with open('%s-%s-flight-results.json'%(source,destination),'w') as fp:
			json.dump(scraped_data,fp,indent = 4)

		flight_list = parse_all_flights(scraped_data, source, destination)
		global global_flight_list 
		global_flight_list = flight_list

		allAirports = []
		coords = []
		allAirports = get_all_airports()
		for airportitem in allAirports:

			if airportitem[1] == source:
				coords.append([airportitem[2], airportitem[3]])

			if airportitem[1] == destination:
				coords.append([airportitem[2], airportitem[3]])

		return render_template('return_map.html', flight_list = flight_list, temp=airport, destination=coords)


@app.route("/itenerary/departure", methods = ["POST", "GET"])
def itenerary_postdeparture():
	global city_name
	print("IM IN HERE YO")
	flight_choice = request.form['flight_depart_choice']
	print(flight_choice)
	print("Printed flight choice")
	global iteneraryItems
	depart_flight = []
	global global_flight_list

	print(global_flight_list)
	iteneraryItems = []

	for flight in global_flight_list:
		if flight[7] == flight_choice:
			print(flight)
			depart_flight = flight

	allAirports = []
	allAirports = get_all_airports()
	for airportitem in allAirports:
		print(airportitem[0] + " " + airportitem[1])

	iteneraryItems.append(['departure_flight', depart_flight])
	city_name = depart_flight[0]

	return render_template('returns.html', airport_list = allAirports)

@app.route("/itenerary/hotel", methods=["POST", "GET"])
def itenerary_posthotel():
	hotel_choice = request.form['hotels_choice']
	print(hotel_choice)
	global iteneraryItems
	iteneraryItems.append(['hotels', hotel_choice])

	return render_template('information.html')

@app.route("/itenerary/return", methods = ["POST", "GET"])
def itenerary_postreturn():
	flight_choice = request.form['flight_return_choice']
	print(flight_choice)
	print("Printed flight choice")
	global iteneraryItems

	return_flight = []
	global global_flight_list

	print(global_flight_list)

	for flight in global_flight_list:
		if flight[7] == flight_choice:
			print(flight)
			return_flight = flight

	iteneraryItems.append(['return_flight', return_flight])
	return render_template('information.html')

@app.route("/returns/")
def returns():
	allAirports = []
	allAirports = get_all_airports()
	for airportitem in allAirports:
		print(airportitem[0] + " " + airportitem[1])
	return render_template('returns.html', airport_list = allAirports)


@app.route("/itenerary_info")
def showItenerary():
	global iteneraryItems
	return render_template('itenerary.html', itenerary_items = iteneraryItems)


@app.route("/return_flight/<string:flight_info>")
def itenerary(flight_id):
	return render_template('itenerary.html', source_flight = flight_id)

@app.route("/test/")
def test():
	return render_template('test.html', destination = airports)

@app.route('/search/')
def search():
	return render_template('search.html', airports = airports)

@app.route('/search/<airport_code>')
def show_route(airport_code):
	airport = airport_by_key.get(airport_code)
	if airport:
		return render_template('map.html', temp = airport, destination = destination)
	else:
		return render_template('search.html', airports = airports)

@app.route("/hotel", methods = ["POST", "GET"]) 
def hotel():
	global start_date
	global end_date
	global city_name

	temp = start_date[6]+ start_date[7] + start_date[8] + start_date[9]
	temp1 = start_date[0] + start_date[1]
	temp2 = start_date[3] + start_date[4]
	new_date = temp + "/" + temp1 + "/" + temp2

	temp = end_date[6]+ end_date[7] + end_date[8] + end_date[9]
	temp1 = end_date[0] + end_date[1]
	temp2 = end_date[3] + end_date[4]
	new2_date = temp + "/" + temp1 + "/" + temp2
	allHotels = []
	allHotels = getHotels(new_date, new2_date, "popularity", city_name)
	more_hotels = []
	more_hotels = parse_all_hotels(allHotels)

	print(more_hotels)

	return render_template('hotel.html', hotels = more_hotels)

@app.route('/information/')
def information():
	return render_template('information.html')

@app.route('/about/')
def about():
	return render_template('about.html')


if __name__ == "__main__":
	app.run(debug=True)