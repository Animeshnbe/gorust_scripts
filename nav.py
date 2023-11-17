from matplotlib import pyplot as plt
import random

n = 10
# a matrix of size n*n
a = [[[] for _ in range(n)] for _ in range(n)]

def slope(src,dest, tpy=False):
    slope = 100
    # if not tpy:
    #     print("Src", src)
    #     print("Dest", dest)
    if src[0]!=dest[0]:
        slope = (dest[1]-src[1])/(dest[0]-src[0])
    return slope

def between(pt,road):
    if pt[0]>=road[0][0] and pt[0]<=road[1][0] and pt[1]>=road[0][1] and pt[1]<=road[1][1]:
        return True
    return False

def issameroad(roads, src, dest,w):
    for i in range(len(roads)):
        road = roads[i]
        # print(road)
        if slope(road[0],road[1])==slope(src,dest,True) and between(src,road):
            if between(dest,road):
                return road,0
            roads[i] = [road[0],dest,road[2]]
            return [road[0],dest,road[2]],2
    return [src,dest,w],1

roads = [] # (x1,y1,x2,y2)

def setroad(i,j,here):
    for (x,y,w) in here:
        if (x!=i and y!=j):
            print(x,y)
        d, op = issameroad(roads, (i,j), (x,y), w)
        if (x!=i and y!=j):
            print(d)
        if op==1:
            roads.append(d)

for i in range(n):
    for j in range(n):
        chance = random.random()
        if chance < 0.5:
            here = []
            slot = random.random()
            if slot < 0.33:
                if random.random()<0.5: # vertical
                    x = i
                    y = random.randint(j+1,n)
                    w = random.randint(1,5)
                else: # horizontal
                    x = random.randint(i+1,n)
                    y = j
                    w = random.randint(1,5)
                here.append((x,y,w))
            else:
                x = i
                y = random.randint(j+1,n)
                w = random.randint(1,5)
                here.append((x,y,w))
                x = random.randint(i+1,n)
                y = j
                w = random.randint(1,5)
                here.append((x,y,w))
                if slot > 0.66:
                    diff = random.randint(1,min(n-i,n-j))
                    x = i+diff
                    y = j+diff
                    # print(i,j,x,y)
                    w = random.randint(1,5)
                    here.append((x,y,w))
            setroad(i,j,here)
            
print("here")
# plot
fig, ax = plt.subplots()
for road in roads:
    src, dest, w = road
    src_x, src_y = src
    dest_x, dest_y = dest
    print(src, dest)
    ax.plot([src_x, dest_x], [src_y, dest_y], marker='o', linewidth = w/10, markersize=1)

plt.show()