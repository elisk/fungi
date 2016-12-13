import math
import numpy
import pylab as pl

global final
global Ivalues
global ImaxPA
global ImaxPpl
global KminPA
global KminPpl
global Vcell
global PminA
global PminPl

final = []
Ivalues = []

#Constants
ImaxPA = 1.21 * (10**-7)
ImaxPpl = 1.21 * (10**-7)
KminPA = 1.4 * (10**-5)
KminPpl = 1.4 * (10**-5)
Vcell = 1.1664 *(10**-8) #2.0 * (10**-9) #cm cubed
PminA = 2.8 * (10**-10)
PminPl = 2.8 * (10**-10)

# 
# def magList(list, size):
#     newList = []
#     for x in range(size):
#         row = []
#         for y in range(size):
#             oldVal = list[x][y]
#             newVal = (10**10) * oldVal
#             
#             row.append(newVal)
#         newList.append(row)
#     return newList



def useList(fileName):
    fileN = open(fileName, 'r')
    #fileN = open('lenMatrix_small.txt', 'r')

    uncleanlist = fileN.read()
    
    list1 = uncleanlist.split("\n")
    list2=[]
    for line in list1:
        blankrow=[]
        row=line.split("\t")
        for itm in row:
            #print("___"+itm+"____")
            if itm!="":
                blankrow.append(float(itm))
        if blankrow!=[]:
            list2.append(blankrow)
    return list2


"Makes surface area matrix"
def makeSAmatrix(lenMatrix, size):
    saMatrix = []
    for x in range(size):
        row = []
        for y in range(size):
            val = math.pi * 0.005 * lenMatrix[x][y]
            
            row.append(val)
            
        saMatrix.append(row)
        
    return saMatrix
            
            

"Create initial soil Matrix"
def buildSoil(size):
    global Ivalues

    soilMatrix = []
    for x in range(size):
        row = []
        for y in range (size):
            p= Ivalues[1]
            row.append(p)
        soilMatrix.append(row)
        
    #print(soilMatrix)      
    return soilMatrix

"Create inital fungi Matrix"
def fungiInit(lenList, size):
    fungiInitMatrix = []
    for x in range(size):
        row = []
        for y in range(size):
            if lenList[x][y] == 0:
                NutConc_Fungi = 0
                row.append(NutConc_Fungi)
            else:
                NutConc_Fungi = 0 #(Ivalues[0] #- 0.0001)
                row.append(NutConc_Fungi)
        fungiInitMatrix.append(row)
    
    #print(fungiInitMatrix)
    return fungiInitMatrix


""""Uptake equations"""
def plantUptake(SAroot, soilVal):   #plantUptake(SAroot, soilVal):    # This doesn't make sense to  use...?
    global ImaxPpl
    global Vcell
    global PminPl
    global KminPpl
    
    plantUptake = (SAroot*ImaxPpl)*((soilVal/Vcell) - PminPl)/(KminPpl + ((soilVal/Vcell) - PminPl))
    
    return plantUptake

def fungiUptake(saMatrixVal, soilVal):
    global ImaxPA
    # global Vcell
    global KminPA
    global PminA

    fungiUptake = (saMatrixVal*ImaxPA)*((soilVal/Vcell) - PminA)/(KminPA + ((soilVal/Vcell) - PminA))
    if fungiUptake > soilVal:
        fungiUptake = soilVal
           
    if fungiUptake<0:
        fungiUptake = 0
    
    return fungiUptake


"""update equations"""

def soilUpdate(previousVal, saMatrixVal):
    newSoilVal = previousVal - fungiUptake(saMatrixVal, previousVal) #- plantUptake(saMatrixVal, previousVal)    #currently using sa for hyphe inplant uptake but should be root sa value
    #print(fungiUptake(saMatrixVal,previousVal))
    return newSoilVal

def fungiUpdate(previousfungiVal, saMatrixVal, previousSoilVal):
    newFungiVal = previousfungiVal + fungiUptake(saMatrixVal, previousSoilVal)
    #print(fungiUptake(saMatrixVal, previousSoilVal))
    return newFungiVal
    

"Caclulate soil concentrations for steps timesteps"
def soilConc(steps, size, initialMatrix, saMatrix, Vs):
    #soilMatrix = loopMatrix(initialMatrix, size, steps, soilUpdate, saMatrix, Vs)
    soilMatrix = []
    soilMatrix.append(initialMatrix) 
    
    #magIntList = magList(initialMatrix, size)
    
    pl.matshow(initialMatrix, cmap = pl.cm.jet, vmin = 0, vmax = 2 * (10 **(-13)))
    pl.show() 
    
    for num in range(steps):
        #print('timestep', num)
        previousTS = soilMatrix[num]
        #print("previousTS", previousTS)
        flowMatrix = inflow(previousTS, size)
        #print('flowM', flowMatrix)
        addFlowMatrix = []
        
        for x in range(size):
            row = []
            for y in range(size):
                flowAdd = flowMatrix[x][y]
                row.append(flowAdd)
            addFlowMatrix.append(row)

        #print('AFM', addFlowMatrix)  
        
        timestep = []  
        
        for x in range(size):
            row = []
            for y in range(size):
                previousVal = soilMatrix[num][x][y]
                saMatrixVal = saMatrix[x][y]
                newVal = soilUpdate(previousVal, saMatrixVal) + addFlowMatrix[x][y]
                row.append(newVal)
            timestep.append(row)  
        
        pl.matshow(timestep, cmap = pl.cm.jet, vmin = 0, vmax = 2 * (10 **(-13)))
        pl.show()
        
        soilMatrix.append(timestep)
    
    

    
    return soilMatrix

def fungiConc(steps, size, initialMatrix, saMatrix, soilMatrix):
    fungiFinal = []
    fungiFinal.append(initialMatrix)
    
    for num in range(steps):
        #print('ts = ', num)
        previousTS = fungiFinal[num]
        timestep = []
        
        for x in range(size):
            row = []
            for y in range(size):
                previousVal = fungiFinal[num][x][y]
                previousSoilVal = soilMatrix[num][x][y]
                saMatrixVal = saMatrix[x][y]
                
                newVal = fungiUpdate(previousVal, saMatrixVal, previousSoilVal)
                row.append(newVal)
            timestep.append(row)
    
   
        fungiFinal.append(timestep)
    
    return fungiFinal    



"Inflow Function"
def inflow(tstepList, size):
    inflowValGrid = []
    d = 0.0018 #cm
    alpha = 8.1 * (10 ** -7)
    cons = 1.1664 * (10 **(-12))  # P per cell
    for row in range(size):
        #print("row", row)
        flowRow = []
        for col in range(size):
            #print("col", col)
            
            #print((row,col), tstepList[row][col])
            Center = tstepList[row][col]
            
            if (row - 1) < 0 and (col-1) < 0:
                #print('upper left')
                
                Top = cons
                Bottom = tstepList[row + 1][col]
                Right = tstepList[row][col + 1]
                Left = cons
                
                
            elif (row + 1) == size and (col - 1) < 0:
                #print('bottom left')
                Top = tstepList[row - 1][col]
                Bottom = cons
                Right = tstepList[row][col + 1]
                Left = cons                
     
            elif (row -1) < 0 and (col + 1) == size:
                #print('bottom left')
                Top = cons
                Bottom = tstepList[row + 1][col]
                Right = cons 
                Left = tstepList[row][col - 1]
                
                    
            elif (row + 1) == size and (col + 1) == size:
                Top = tstepList[row - 1][col]
                Bottom = cons
                Right = cons
                Left = tstepList[row][col - 1]                
                        
            elif (row - 1) < 0:
                Top = cons
                Bottom = tstepList[row + 1][col]
                Right = tstepList[row][col + 1]
                Left = tstepList[row][col - 1]                
                
            elif (row + 1) == size:
                Top = tstepList[row - 1][col]
                Bottom = cons
                Right = tstepList[row][col + 1]
                Left = tstepList[row][col - 1]
                
                
            elif (col - 1) < 0:
                Top = tstepList[row - 1][col]
                Bottom = tstepList[row + 1][col]
                Right = tstepList[row][col + 1]                
                Left = cons
            
            elif (col + 1) == size:
                Top = tstepList[row - 1][col]
                Bottom = tstepList[row + 1][col]                
                Right = cons
                Left = tstepList[row][col - 1]
                
  
            else:            
                Top = tstepList[row - 1][col]
                Bottom = tstepList[row + 1][col]
                Right = tstepList[row][col + 1]
                Left = tstepList[row][col - 1]
                
                
            #print(Top, Bottom, Right, Left)         
              
            lap = alpha * (((Top + Bottom + Right + Left) - (4 * tstepList[row][col]))/(d**2)) 
            
            #print('lapa', lap)
            
            flowRow.append(lap)
            
        inflowValGrid.append(flowRow)
        
    return inflowValGrid



"main function to call, intakes desired number of timesteps and size."
def main(steps, size):
    global final
    global Ivalues
    global Vcell
    
    #Parameters
    TotalVolume = 0.00008 #cm^3
    Vs = Vcell
    #Ma = 10  
    
    #Initial values
    PSti = 2 * (10 **(-13))  #grams of phosphorus
    PAti = 0
    Ivalues = [PAti, PSti]
    
    #Inital Matrices
    InitalSoilMatrix = buildSoil(size)
    #print(InitalSoilMatrix)
    
    lenMatrix = useList('lenMatrix_199.txt')
    
    #lenMatrix = useList('lenMatrix0.txt') #close 
    
    #lenMatrix = useList('lenMatrix1.txt') #far
    
    #print('lengthval', len(lenMatrix))
    
    fungiMatrix = fungiInit(lenMatrix, size)
    #print(fungiMatrix)
    
    SAmatrix = makeSAmatrix(lenMatrix, size)
    
    #Updating soil and fungi matrices
    soil = soilConc(steps, size, InitalSoilMatrix, SAmatrix, Vs)
    fungi = fungiConc(steps, size, fungiMatrix, SAmatrix, soil)
    
    #Append soil and fungi matrices
    final.append(soil)
    final.append(fungi)
    #print('Soil:  ', soil)
    #print('Fungi: ', fungi)

    return final


desiredTS = 15
desiredSize = 199 # long 841 #short 471
main(desiredTS, desiredSize)