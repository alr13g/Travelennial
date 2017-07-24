from flask import Flask, render_template, request

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
	airport('Test', 'Te', 37.9045286, -122.1445772)
]

destination = airports

airport_by_key = {airport.key: airport for airport in airports}

@app.route("/")
def home():
	return render_template('home.html', airports = airports)

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