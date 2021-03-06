import re
hotel_regex = re.compile(r"_[\d]+_")

def get_hotel_info():
	
	''' 
	INPUT: hotel_price_location.txt 

	OUTPUT: list consisting of [hotel_id, price, location] entries
	
	USAGE: hotel_info = get_hotel_info()

	NOTE: 1674 out of 1850 hotels have prices. Missing prices are 
		  indicated by -1
	'''
	
	# filename = "C:\Users\Kwok\Dropbox\Zipfian\winter2015\hobby\TripAdvisor\hotel-reviews\Hotel-Reviews\hotel_price_location.txt"
	filename = "C:\Users\Rickz\Dropbox\Zipfian\winter2015\hobby\TripAdvisor\hotel-reviews\Hotel-Reviews\hotel_price_location.txt"
	f = open(filename)
	text = f.read()
	f.close()
	text = [word.split('\t') for word in text.splitlines()]
	hotel_info = []
	for i in xrange(1, len(text)):
		''' Iterate through entire file storing price if exists. '''
		# regular expression for hotel_id from <filename>
		hotel_id = re.findall(hotel_regex, text[i][0])
		price = text[i][1]
		location = text[i][2]

		if price.isdigit():
			if int(price) > 0 and location != "Unknown":
				hotel_info.append((int(hotel_id[0][1:-1]), int(price), location))
				
	return tuple(hotel_info)
