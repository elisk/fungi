from math import *
import numpy as np
import pylab as pl
from matplotlib import collections  as mc
global storage
global numPrec
global lenMatrix
global xMax
global xMin
global yMax
global yMin
global bigcounter
storage=[]
numPrec=5

lenMatrix={}
xMax=0
xMin=0
yMax=0
yMin=0
bigcounter=0

#~~~~~~~~~~~~~~~~~UTILITY~~~~~~~~~~~~~~~~~~~~
def listprint(lt):
    for elt in lt:
        print(elt)
        
        
def matrixTransform(matrix,minSize=1100):
#MODIFY ME~~~~~~~~~~~~~~~~~~~~~~~~~^^^^
    newMatrix=[]
    if xMax-xMin>yMax-yMin:
        span=xMax-xMin
    else:
        span=yMax-yMin
    if span >= minSize:
        minSize=span
    buffer=round((minSize-(span))/2)
    print("buffer:")
    print(buffer)
    for x in range(buffer):
        newCol=[]
        for y in range(minSize):
            newCol.append(0)
        newMatrix.append(newCol)
    for x in range(xMin,xMin+span+1):
        newCol=[]
        for y in range(buffer):
            newCol.append(0)
        for y in range(yMin,yMin+span+1):
            if x in matrix:
                if y in matrix[x]:
                    newCol.append(matrix[x][y])
                else:
                    newCol.append(0)
            else:
                newCol.append(0)
        for y in range(buffer-1):
            newCol.append(0)
        newMatrix.append(newCol)
    for x in range(buffer):
        newCol=[]
        for y in range(minSize):
            newCol.append(0)
        newMatrix.append(newCol)
    return newMatrix


def cshift(tup,angle,distance):
    global numPrec
    return (tup[0]+round(distance*cos(angle),numPrec),tup[1]+round(distance*sin(angle),numPrec))

def angshift(picker,ang, dirct=0):
    angles=[]
    pick=picker.split("_")
    if pick[0]=="radiate":
        branchnumber=int(pick[1])
        for a in range(branchnumber):
            angles.append(a*2*pi/branchnumber+dirct)
        
    if pick[0]=="bi":
        angles.append(ang/2+dirct)
        angles.append(-ang/2+dirct)
    if pick[0]=="tri":
        angles.append(ang+dirct)
        angles.append(dirct)
        angles.append(-ang+dirct)
        
    return angles
    
def lenshift(number,picker="constant",length=sqrt(2)):
    lengths=[]
    pick=picker.split("_")
    if pick[0]=="constant":
        multiply=float(pick[1])
        for ii in range(number):
            lengths.append(length*multiply)

    if pick[0]=="zero":
        for ii in range(number):
            lengths.append(0)
        
    return lengths

"""    
def lenevolve(function, iter, inpt):
    if function=="switch":
        if iter<3*depth/4:
            return inpt
        else:
            return 1/inpt
    if function=="ratio":
        return inpt
"""        
        
def snipper(x0,y0,x1,y1,angle):
    global numPrec
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
    for kk in range(len(xlist)-1):
        segLen=sqrt((xlist[kk+1]-xlist[kk])**2+(ylist[kk+1]-ylist[kk])**2)
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
                lenMatrix[xStart][yStart]=round(segLen*.0018+lenMatrix[xStart][yStart],numPrec)
            else:
                lenMatrix[xStart][yStart]=round(segLen,numPrec)*.0018
        else:
            lenMatrix[xStart]={}
            lenMatrix[xStart][yStart]=round(segLen,numPrec)*.0018
    
        
    
def listmaker(firstlist,size):
    newlist=[]
    for number in range(size):
        if number<len(firstlist):
            newlist.append(firstlist[number])
        else:
            newlist.append(firstlist[len(firstlist)-1])
    return newlist



def branch(angstyle, lenstyle, angRatios, dist, initAng, depth, initDir=0, loc1=(0,0), count=0):
    global storage
    newAng=initAng*angRatios[count]
    anglist=angshift(angstyle[count],newAng,initDir)
    lenlist=lenshift(len(anglist),lenstyle[count],dist)
    newloc=[]
    for ct in range(len(anglist)):
        newloc.append(cshift(loc1,anglist[ct],lenlist[ct]))
        
        snipper(loc1[0],loc1[1],newloc[ct][0],newloc[ct][1],anglist[ct])
        storage.append([loc1,newloc[ct]])
    
    count=count+1
    if count<depth:
        for ct2 in range(len(anglist)):
            branch(angstyle, lenstyle, angRatios, lenlist[ct2], newAng, depth, anglist[ct2], newloc[ct2], count)
            


def run(angSet,lenSet,angRatSet,scale,angleScale,maxIter):
    global storage
    global lenMatrix
    global xMax
    global xMin
    global yMax
    global yMin
    global bigcounter

    branch(listmaker(angSet,maxIter), listmaker(lenSet,maxIter), listmaker(angRatSet,maxIter), scale, angleScale, maxIter)
    
    grid=matrixTransform(lenMatrix)

    #~~~~~~~~plotting
    lp=mc.LineCollection(storage)
    fig, ax = pl.subplots()
    ax.add_collection(lp)
    ax.set_aspect('equal', 'datalim')
    ax.margins(0.1)
    pl.show()
    pl.savefig("branches"+str(bigcounter)+".png")
    
    pl.matshow(grid, cmap=pl.cm.jet)
    pl.show()
    
    #~~~~~~~~~~saving data
    fileout=open('lenMatrix'+str(bigcounter)+'.txt','w')
    for item in grid:
        for thing in item:
            fileout.write(str(thing)+"\t")
        fileout.write("\n")
    fileout.close()
    pl.savefig("density"+str(bigcounter)+".png")
    print(len(grid))
    
    #~~~~~~~~~resetting variables
    storage=[]
    lenMatrix={}
    xMax=0
    xMin=0
    yMax=0
    yMin=0
    
    bigcounter=bigcounter+1
"""
#depth=8
run(["radiate_3","bi"],["zero","constant_1"],40)
run(["radiate_5","bi"],["zero","constant_1"],40)
#depth=7
run(["radiate_3","radiate_3","bi"],["constant_5","constant_1"],40)
run(["radiate_5","radiate_5","bi"],["constant_5","constant_1"],40)
"""

run(["radiate_10","bi"],["constant_2","constant_.75","constant_1","constant_.7"],[1,.5,1.5,.75],40,pi/2,4)

run(["radiate_3","radiate_1","tri","bi"],["constant_2","constant_3","constant_.2","constant_1"],[1,1,0.3,1],40,pi/2,5)