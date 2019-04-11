import matplotlib.pyplot as plt
import numpy as np

###-----location of crosspoint----###
file = open("./map/crosspoint_final.csv", "r")
k=0
N=2677
lat=np.tile(0.0,N)
lng=np.tile(0.0,N)
id=[]
for s in file:
    items=s.rstrip().split(',')
    lat[k]=float(items[1])
    lng[k] = float(items[2])
    id.append(items[4])
    k=k+1

###-----plot road segments----###

f_rs = open("./map/road_segment.csv", "r")
for line in f_rs:
    items=line.rstrip().split(',')
    plt.plot([float(items[3]), float(items[5])],[float(items[2]), float(items[4])],'-b',linewidth=0.5)

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

plt.plot(lng, lat,'bo',linewidth=1,markersize=1.5)
plt.plot(lng_res, lat_res,'r.',linewidth=1,markersize=2)
plt.show()
