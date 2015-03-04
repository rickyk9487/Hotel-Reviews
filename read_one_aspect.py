''' 
Extract an array of Overall + Seven Aspects from filename: 
Overall 0, Value 1, Room 2, Location 3, Cleanliness 4, 
Check In/Front Desk 5, Service 6, Business service 7 
'''

def open_parsed(filename):
	'''

	INPUT: filename of one hotel file with aspects.
	OUTPUT: array of user's aspect reviews from filename

	example usage:
	filename = hotel_269171_parsed_parsed.txt
	aspects = open_parsed(filename)
	overall, value, room, loc, clean, check, serv, biz = aspect
	''' 
	f = open(filename)
	text = f.read()
	f.close()
	text = [word.split('\t') for word in text.splitlines()]
	return text
"""
	# every review consists of 14 entries 
	# overall, value, room, loc, clean, check, serv, biz
	firstN = len(text) / 14 
	variables = [], [], [], [], [], [], [], []
	for x in xrange(firstN):
		# store the first firstN ratings for the aspects into arrays
	    variables[0].append(int(text[14 * x + 3][0][-1]))
	    for k in xrange(1, 8):
	        variables[k].append(int(text[14 * x + 3][k]))

	aspect = [[]]
	for j in xrange(8):
		# drop missing values indicated by -1 from values
	    aspect.append(filter(lambda a: a != -1, variables[j]))

	aspect.pop(0);
	return aspect
"""	