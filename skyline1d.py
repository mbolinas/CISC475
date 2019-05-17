

#calculates the 1D LBSQ for a single road segment

#road: an edge of the graph from graph_pickle, representing a single road
#poi_set: a set of elements, where each element is a POI on the given road segment
	#each element should have attributes distance and price
		#distance is relative, expressed as a fraction, representing how far along the road segment
		#it is placed
#road_pos: double, the position on the road the query originated from
def sky1d(road, poi_set, road_pos):

	if(road_pos > 1 | road_pos < 0):
		print("WARNING: road_pos is supposed to be a fraction s.t. 0 <= road_pos <= 1\n(continuing algorithm with incorrect road_pos...)")

	result_set = []
	left_set = []
	right_set = []
	#error_set = []

	#we divide the poi_set into a set of elements left of road_pos and right of road_pos
	for p in poi_set:
		if p.distance - road_pos < 0:
			left_set.add(p)
		elif p.distance - road_pos > 0:
			right_set.add(p)
		else:
			#what happens if a POI is placed exactly where the user is located?
			#presumably it automatically gets added into the result set - it's distance is 0, so
			#it cannot be dominated by definition

			#uncomment the following line if the above implementation is wanted:
			#result_set.add(p)
			print("a POI is placed exactly at road_pos, ignoring...\nsee skyline1d.py to change implementation")

	#remove dominated POIs
	for p in left_set:
		for r in left_set:
			#if p is farther away and more expensive than any other POI in the same set,
			#it is dominated, so remove it
			if(abs(p.distance - road_pos) > abs(r.distance - road_pos) & p.price > r.price):
				left_set.remove(p)
				continue

	#remove dominated POIs
	for p in right_set:
		for r in right_set:
			if(abs(p.distance - road_pos) > abs(r.distance - road_pos) & p.price > r.price):
				right_set.remove(p)
				continue

	for p in left_set:
		result_set.add(p)
	for p in right_set:
		result_set.add(p)


	return result_set

#def result_set_to_neighbors(result_set, road_pos):
	#result_set.add()
	#result_set.add()

