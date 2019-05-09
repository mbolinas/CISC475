'''
Same code as Yidan's, just adapted in some small ways
'''
import matplotlib.pyplot as plt
import numpy as np

# True if you want to plot poi's, else False
PLOT_POI = False;
SHOW_PLOT = False;
# length and width in inches
LENGTH = 20
WIDTH = 20

#--------------------------parse config file--------------------------------
with open('bBoxConfig.txt', "r") as bBoxFile:
    lines = bBoxFile.readlines()
name = lines[1].rstrip('\n')
intersectionInput = "./generated_map_data/intersections{}.csv".format(name)
roadSegmentInput = "./generated_map_data/roadSegments{}.csv".format(name)
# --------------------------------------------------------------------------

plt.figure(figsize=(LENGTH,WIDTH))

###-----location of crosspoint----###
N=sum(1 for line in open(intersectionInput)) # number of lines in input
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
    plt.plot([float(items[3]), float(items[5])],[float(items[2]), float(items[4])],'-b',linewidth=0.3)


###-----plot location of restaurants after mapping----###
if PLOT_POI:
    poiInput = "./generated_map_data/poiYelp{}.csv".format(name)
    N=sum(1 for line in open(poiInput)) # number of lines in input
    print(N)
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
    plt.plot(lng_res, lat_res,'r.',linewidth=0.1,markersize=.5)

###-----plot crosspoints----###
plt.plot(lng, lat,'bo',linewidth=0.1,markersize=0.2)

# save to file. sometimes these autosaved images might not look very nice. in that case
# its better to resize the plot and save manually
plt.savefig('./map_data_images/autosaved{}.png'.format(name), bbox_inches='tight')

if SHOW_PLOT:
    plt.show()
