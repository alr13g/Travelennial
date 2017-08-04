import requests

all_hotels = []

def parse_all_hotels(get_hotels):
	print("IN HERE")

	for hotel in get_hotels:
		provider = hotel.get("booking_provider")
		features = hotel.get("hotel_features")
		city = hotel.get("locality")
		url = hotel.get("url")
		checkin = hotel.get("checkIn")
		price = hotel.get("price_per_night")
		checkout = hotel.get("checkOut")
		hot_name = hotel.get("hotel_name")
		rating = hotel.get("tripadvisor_rating")


		print("\n\n\n")

		all_hotels.append([hot_name, city, checkin, checkout, features, price, rating, provider, url])

	print get_hotels

		

	return all_hotels
