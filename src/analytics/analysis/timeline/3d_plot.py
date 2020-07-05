import json
import matplotlib.cm as cm

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

# Fixing random state for reproducibility
np.random.seed(19680801)

def get_events():
    with open("data/892388108.json") as file:
        data = json.loads(file.read())
    # Get initial positions
    initpos= {index: list(pframe[u"position"].values()) for index, pframe in data[u"frames"][0][u"participantFrames"].items()}
    
    # Process events
    points = []
    for frame in data[u"frames"]:
        # Store events
        for event in frame[u"events"]:
            if event[u"type"] == "ITEM_PURCHASED" or event[u"type"] == "ITEM_SOLD":
                index = str(event[u"participantId"])
                points.append( [initpos[index][0], initpos[index][1], event[u"timestamp"], event[u"participantId"]] )
            elif event[u"type"] == "CHAMPION_KILL":
                points.append( [event[u"position"][u"x"], event[u"position"][u"y"], event[u"timestamp"], event[u"killerId"]] )
        # Store participantFrames
        for pframe in frame[u"participantFrames"].values():
            if u"position" in pframe:
                points.append( [pframe[u"position"][u"x"], pframe[u"position"][u"y"], frame[u"timestamp"], pframe[u"participantId"]] )
            else:
                points.append( [0, 0, frame[u"timestamp"], pframe[u"participantId"]] )
    return points

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

step = 100
colors = [ (0, 0, 0) ]

p = get_events()
s = [[] for i in range(11)]
xline = []
yline = []
tline = []
for i in range(1, 11):
    s[i] = [point[:-1] for point in p if point[3]==i]

temp_xline = []
temp_yline = []
temp_tline = []

for plist in s:
    for j in plist:
        if not j:
            continue
        temp_xline.append( j[0] )
        temp_yline.append( j[1] )
        temp_tline.append( j[2] )
    xline.append(temp_xline)
    yline.append(temp_yline)
    tline.append(temp_tline)

for k in s:
    #ax.scatter(k[0], k[1], k[2])
    pass
plt.plot(xline[3], yline[3], tline[3], '-o')

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('T Label')

plt.show()
