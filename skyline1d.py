

#calculates the 1D LBSQ for a single road segment

#road: 
#poi_set: 
#road_pos: double, the position on the road the query originated from 
#road_pos_proj: tuple, optional, the location the query originated if not on the road
def sky1d(road, poi_set, road_pos, road_pos_proj = None):
	if road_pos_proj is not None:
		#project road_pos onto the road
		#optimization problem, road is a line, derive road formula, etc

	result_set = [];
	left_set = [];
	right_set = [];
	error_set = [];

	for p in poi_set:
		if p.distance - road_pos < 0:
			left_set.add(p)
		else if p.distance - road_pos > 0:
			right_set.add(p)
		else:
			print("user's road pos is the same as a poi\nunsure whether to add to left or right set")
			error_set.add(p)

	for p in left_set:
		add = False
		for r in result_set:
			if(abs(p.distance - road_pos) < abs(r.distance - road_pos) && p.price < r.price):
				result_set.remove(r)
				add = True

		for r in result_set:
			if(abs(p.distance - road_pos) < abs(r.distance - road_pos) || p.price < r.price):
				add = True

		if add is True:
			result_set.add(p)

	for p in result_set:
		for r in result_set:
			if(abs(p.distance - road_pos) < abs(r.distance - road_pos) && p.price < r.price):
				result_set.remove(r)


	#todo: add verification POIs in preprocessing
	#todo: query result verification

	return result_set

