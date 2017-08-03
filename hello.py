from __future__ import print_function
from flask import Flask, render_template, request
from flightData import getFlightData
from parseFlights import parse_all_flights
from getAirports import get_all_airports
import json
import requests
from lxml import html
from collections import OrderedDict
import argparse
import sys

app = Flask(__name__)

#use for maps
mapKey = "AIzaSyD_3OXGut2rO_V_aH1DFxuJdaqmHtlSofU"

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
	source = request.form['from_id']
	print("Source: " + str(source))
	destination = request.form['to_id']
	print("Destination: " + str(destination))
	date = request.form['date_id']
	print("Date " + str(date))

	argparser = argparse.ArgumentParser()
	argparser.add_argument('source',help = 'Source airport code')
	argparser.add_argument('destination',help = 'Destination airport code')
	argparser.add_argument('date',help = 'MM/DD/YYYY')

	print("Getting flight details")
	scraped_data = getFlightData(source, destination, date)
	print("Writing data to JSON file")
	with open('%s-%s-flight-results.json'%(source,destination),'w') as fp:
		json.dump(scraped_data,fp,indent = 4)

	flight_list = parse_all_flights(scraped_data, source, destination)

	allAirports = []
	coords = []
	allAirports = get_all_airports()
	for airportitem in allAirports:

		if airportitem[1] == source:
			coords.append([airportitem[2], airportitem[3]])

		if airportitem[1] == destination:
			coords.append([airportitem[2], airportitem[3]])

	return render_template('map.html', flight_list = flight_list, temp=airport, destination=coords)

@app.route("/returns/")
def returns():
	allAirports = []
	allAirports = get_all_airports()
	for airportitem in allAirports:
		print(airportitem[0] + " " + airportitem[1])
	return render_template('returns.html', airport_list = allAirports)

@app.route("/source_flight/<string:flight_id>")
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

@app.route('/about/')
def about():
	return render_template('about.html')

if __name__ == "__main__":
	app.run(debug=True)