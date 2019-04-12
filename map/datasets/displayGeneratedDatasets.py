'''
Same code as Yihan's, just adapted in some small ways
'''
import matplotlib.pyplot as plt
import numpy as np

intersectionInput = "intersectionsManhattan.csv"
roadSegmentInput = "roadSegmentsRoughManhattan.csv"
'''
N values for generated intersectionsX.csv is equal to number of rows.
For some reason using a function to calculate the rows doesn't
work (even though it returns the correct number), so here's some values:
Manhattan = 11105
Paris = 17331
...
The rest you'd just have to get the number from excel or something
'''
N=11105

###-----location of crosspoint----###
file = open(intersectionInput, "r")
k=0
print(N)
lat=np.tile(0.0,N)
lng=np.tile(0.0,N)
#id=[]
for s in file:
    items=s.rstrip().split(',')
    lat[k]=float(items[2])
    lng[k] = float(items[3])
    #id.append(items[4])
    k=k+1

###-----plot road segments----###
f_rs = open(roadSegmentInput, "r")
for line in f_rs:
    items=line.rstrip().split(',')
    plt.plot([float(items[1]), float(items[3])],[float(items[0]), float(items[2])],'-b',linewidth=0.1)

'''
###-----plot location of restaurants after mapping----###
res_f=open("./map/res_mapping_road_based.csv", "r")
k=0
N=4816
lat_res=np.tile(0.0,N)
lng_res=np.tile(0.0,N)
id=[]
for s in res_f:
    items=s.rstrip().split(',')
    lat_res[k]=float(items[3])
    lng_res[k]=float(items[4])
    k=k+1
'''

plt.plot(lng, lat,'bo',linewidth=0.1,markersize=0.2)
#plt.plot(lng_res, lat_res,'r.',linewidth=1,markersize=2)
plt.show()
