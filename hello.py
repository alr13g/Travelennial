from flask import Flask, render_template

app = Flask(__name__)

#use for maps
mapKey = "AIzaSyCWvuV9bMA9iUGNCqqWdgKu4vuAfmlNAUk"

class airport:
	def __init__(self, name, key, lat, lng):
		self.name = name
		self.key = key
		self.lat = lat
		self.lng = lng

'''
This is just a tempate but from the video im watching he uses the key
as a part of the web page traversal. So im thinking when we crawl airports for
locations we see if they already exist within our database. if not we add them and make
their custom key be the first letter of each word. if we have a key conflict then
we take the second letter from the first word infront of the first words location.

We are also should store the information so that we dont backtrack but my idea is a list of lists ie

[[Airport1, Price1], [Airport2, Price2], ect]

price2 is amount of money from airport 1 to airport 2

We should also probably have them start and end at an airport. otherwise it might be too vauge for the result and our code.
Like do they want to be on the north side or south side of california?

Joey Testa
'''
airports = (
	airport('Tallhassee International Airport', 'TIA', 30.3954, 84.3451),
	airport('Test', 'Te', 37.9045286, -122.1445772)
)

airport_by_key = {airport.key: airport for airport in airports}

@app.route("/")
def home():
	return render_template('home.html', airports = airports)

@app.route('/search/')
def search():
	return render_template('search.html', airports = airports)

@app.route('/<airport_code>')
def show_route(airport_code):
	airport = airport_by_key.get(airport_code)
	if airport:
		return render_template('map.html', airport = airport)
	else:
		return render_template('search.html', airports = airports)

@app.route('/about/')
def about():
	return render_template('about.html')

if __name__ == "__main__":
	app.run(debug=True)
