from math import *
import numpy as np
import pylab as pl
from matplotlib import collections  as mc
global storage
storage=[]
numPrec=5
depth=8

global lenMatrix
global xMax
global xMin
global yMax
global yMin
xMax=0
xMin=0
yMax=0
yMin=0

lenMatrix={}

#~~~~~~~~~~~~~~~~~UTILITY~~~~~~~~~~~~~~~~~~~~
def listprint(lt):
    for elt in lt:
        print(elt)


def cshift(tup,angle,distance):
    return (tup[0]+round(distance*cos(angle),numPrec),tup[1]+round(distance*sin(angle),numPrec))

def angshift(picker="bi",ang=pi/2, dirct=0):
    angles=[]
    if "radiate" in picker:
        branchnumber=int(picker[-1:])
        for a in range(branchnumber):
            angles.append(a*2*pi/branchnumber+dirct)
        
    if picker=="bi":
        angles.append(ang/2+dirct)
        angles.append(-ang/2+dirct)
        
    return angles
    
def lenshift(number,picker="constant",length=sqrt(2)):
    lengths=[]
    if picker=="constant":
        for ii in range(number):
            lengths.append(length)
    if picker=="zero":
        for ii in range(number):
            lengths.append(0)
        
    return lengths
    
def lenevolve(function, iter, inpt):
    if function=="switch":
        if iter<3*depth/4:
            return inpt
        else:
            return 1/inpt
    if function=="ratio":
        return inpt
        
def snipper(x0,y0,x1,y1,angle):
    #print("~"*20)
    #print(x0,y0,x1,y1,angle)
    global lenMatrix
    global xMax
    global xMin
    global yMax
    global yMin
    x0=x0+.5
    y0=y0+.5
    x1=x1+.5
    y1=y1+.5
    angle=angle % (pi*2) #Finds angle mod 2pi
    xlist=[x0,x1] #puts endpoints into x and y lists
    ylist=[y0,y1]
    if (x1-x0)!=0:
        slope = (y1-y0)/(x1-x0)
        intcpt = y0-slope*x0
        xmin=min(x0,x1)
        xmax=max(x0,x1)
        ymin=min(y0,y1)
        ymax=max(y0,y1)
        for xnum in range(int(ceil(xmin)),int(floor(xmax))+1): #Finds crosspoints between gridlines and points
    
            xlist.append(xnum)
            ylist.append(xnum*slope+intcpt)
        if slope!=0:
            for ynum in range(int(ceil(ymin)),int(floor(ymax))+1):
            
                
                xlist.append((ynum-intcpt)/slope)
                ylist.append(ynum)
    else:
        ymin=min(y0,y1)
        ymax=max(y0,y1)
        for ynum in range(int(ceil(ymin)),int(floor(ymax))+1):
        
            
            xlist.append(x0)
            ylist.append(ynum)
        
        
    if angle <= pi/2:
        xlist.sort()
        ylist.sort()
    elif angle <= pi:
        xlist.sort()
        ylist.sort()
        ylist.reverse()
    elif angle <= 3*pi/2:
        xlist.sort()
        ylist.sort()
    else:
        xlist.sort()
        ylist.sort()
        ylist.reverse()
    #print(xlist,ylist)
    for kk in range(len(xlist)-1):
        segLen=sqrt((xlist[kk+1]-xlist[kk])**2+(ylist[kk+1]-ylist[kk])**2)
        #print(xlist[kk],ylist[kk],segLen)
        xStart=floor(min(xlist[kk],xlist[kk+1])) 
        yStart=floor(min(ylist[kk],ylist[kk+1]))
        if xStart>xMax:
            xMax=xStart
        elif xStart<xMin:
            xMin=xStart
        
        if yStart>yMax:
            yMax=yStart
        elif yStart<yMin:
            yMin=yStart

        if xStart in lenMatrix:
            if yStart in lenMatrix[xStart]:
                #lenMatrix[xStart][yStart]=segLen+lenMatrix[xStart][yStart]
                lenMatrix[xStart][yStart]=round(segLen+lenMatrix[xStart][yStart],4)
            else:
                #lenMatrix[xStart][yStart]=segLen
                lenMatrix[xStart][yStart]=round(segLen,4)
        else:
            lenMatrix[xStart]={}
            #lenMatrix[xStart][yStart]=segLen
            lenMatrix[xStart][yStart]=round(segLen,4)
    
        
    




def branch(loc1=(0,0), count=0, dist=sqrt(2), initAng=(1/.9)*pi/2, initDir=0, angstyle="radiate3", lenstyle="zero"):
    global storage
    count=count+1
    
    anglist=angshift(angstyle,initAng,initDir)
    lenlist=lenshift(len(anglist),lenstyle,dist)
    newloc=[]
    for ct in range(len(anglist)):
        newloc.append(cshift(loc1,anglist[ct],lenlist[ct]))
        
        snipper(loc1[0],loc1[1],newloc[ct][0],newloc[ct][1],anglist[ct])
        storage.append([loc1,newloc[ct]])
    
    #print(loc1,newloc, count)
    if count<depth:
        for ct in range(len(anglist)):
            branch(newloc[ct], count, dist*lenevolve("ratio",count,.75), initAng*.9, anglist[ct], "bi", "constant")
            
def matrixTransform(matrix):
    newMatrix=[]
    for x in range(xMin,xMax+1):
        newCol=[]
        for y in range(yMin,yMax+1):
            if y in matrix[x]:
                newCol.append(matrix[x][y])
            else:
                newCol.append(0)
        newMatrix.append(newCol)
    return newMatrix
"""
snipper(0.0, 0.0, -0.75, 0.75,.9*pi) #ok check what's happening here
print(lenMatrix)
lenMatrix={}

snipper(0.0, 0.0, 0.75, -0.75,1.6*pi) #fine
print(lenMatrix)
lenMatrix={}
snipper(0.0, 0.0, 0.75, 0.75,.4*pi) #fine
print(lenMatrix)
lenMatrix={}
snipper(0.0, 0.0, -0.75, -0.75,1.4*pi) #fine
print(lenMatrix)
lenMatrix={}
"""

branch()

grid=matrixTransform(lenMatrix)

listprint(grid)
lp=mc.LineCollection(storage)
fig, ax = pl.subplots()
ax.add_collection(lp)
ax.set_aspect('equal', 'datalim')
ax.margins(0.1)
pl.show()
pl.matshow(grid, fignum=100)#, cmap=pl.cm.prism)
pl.show()
fileout=open('lenMatrix.txt','w')
fileout.write(str(grid))
fileout.close()
"""
for line in grid:
    for elt in line:
        fileout.write(str(elt))
        fileout.write('\t')
    fileout.write('\n')
fileout.close()
"""
#pl.savefig("branches.png")
