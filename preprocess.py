

##purpose of file:
##after the algorithm has been run, we have a set of POIs that are 'valid'
##the script that displays the map takes in a file containing all the POIs
##so this file will write to file the POIs that were relevant for a specific location



##takes in a set of POIs, usually given from the algorithms, and intersects that set with the set
##of all POIs (./map/res_mapping_road_based.csv)





##this functions is going to have to take in a set of 'correct' POIs and the location that 
##the algorithm was run on
def export_poi_set():
	result = open("./map/" + , "w");

	res_f = open("./map/res_mapping_road_based.csv", "r")
	for s in res_f:
		items = s.rstrip().split(',')
		for name in poi_list:	#there's gotta be a way to perform an intersection that isn't O(n^2)
			if items[0] == name:
				#write to file

