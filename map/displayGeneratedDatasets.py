'''
Same code as Yidan's, just adapted in some small ways
'''
import matplotlib.pyplot as plt
import numpy as np

intersectionInput = "./generated_map_data/intersectionsNewark.csv"
roadSegmentInput = "./generated_map_data/roadSegmentsNewark.csv"
poiInput = "./generated_map_data/poiNewark.csv"

###-----location of crosspoint----###
'''
N values for generated intersectionsX.csv is equal to number of rows.
For some reason using a function to calculate the rows doesn't
work (even though it returns the correct number), so here's some values:
Manhattan = 11105
Paris = 17331
LA = 126994
Newark = 979
...
The rest you'd just have to get the number from excel or something
'''
N=979
file = open(intersectionInput, "r")
k=0
print(N)
lat=np.tile(0.0,N)
lng=np.tile(0.0,N)
#id=[]
for s in file:
    items=s.rstrip().split(',')
    lat[k]=float(items[1])
    lng[k] = float(items[2])
    #id.append(items[4])
    k=k+1

###-----plot road segments----###
f_rs = open(roadSegmentInput, "r")
for line in f_rs:
    items=line.rstrip().split(',')
    plt.plot([float(items[3]), float(items[5])],[float(items[2]), float(items[4])],'-b',linewidth=0.1)


###-----plot location of restaurants after mapping----###

# Same as above N.
N=10000
res_f=open(poiInput, "r")
k=0
lat_res=np.tile(0.0,N)
lng_res=np.tile(0.0,N)
#id=[]
for s in res_f:
    items=s.rstrip().split(',')
    lat_res[k]=float(items[1])
    lng_res[k]=float(items[2])
    k=k+1


plt.plot(lng, lat,'bo',linewidth=0.1,markersize=0.2)
plt.plot(lng_res, lat_res,'r.',linewidth=0.1,markersize=.4)
plt.show()
