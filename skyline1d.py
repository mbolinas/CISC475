

#calculates the 1D LBSQ for a single road segment

#road: an edge of the graph from graph_pickle, representing a single road
#poi_set: a set of elements, where each element is a POI on the given road segment
	#each element should have attributes distance and price
		#distance is relative, expressed as a fraction, representing how far along the road segment
		#it is placed
#road_pos: double, the position on the road the query originated from
def sky1d(road, poi_set, road_pos):

	result_set = []
	left_set = []
	right_set = []
	#error_set = []


	for p in poi_set:
		if p.distance - road_pos < 0:
			left_set.add(p)
		elif p.distance - road_pos > 0:
			right_set.add(p)
		else:
			#print("user's road pos is the same as a poi\nunsure whether to add to left or right set")
			#error_set.add(p)

	for p in left_set:
		for r in left_set:
			#if p is farther away and more expensive than any other POI in the same set,
			#it is dominated, so remove it
			if(abs(p.distance - road_pos) > abs(r.distance - road_pos) & p.price > r.price):
				left_set.remove(p)
				continue

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

