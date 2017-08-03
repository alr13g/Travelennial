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

airports = [
	[30.395412, -84.3472458],
	[42.3656132, -71.0117489],
	[37.9045286, -122.1445772]
]

destination = airports

#airport_by_key = {airport.key: airport for airport in airports}

@app.route("/")
def home():
	return render_template('home.html', airports = airports)

@app.route("/test/")
def test():
	return render_template('test.html', destination = airports)

@app.route('/search/')
def search():
	return render_template('search.html', airports = airports)

@app.route('/search/map')
def show_route():
	#airport = airport_by_key.get(airport_code)
	if airport:
		return render_template('map.html', destination = destination)
	else:
		return render_template('search.html', airports = airports)

@app.route('/about/')
def about():
	return render_template('about.html')

@app.route('/information/')
def information():
	return render_template('information.html')

if __name__ == "__main__":
	app.run(debug=True)
