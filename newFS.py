import math
from inflow import*
from lengthCode import*

global final
global PAtV
global PStV
global lengthMatrix
global saMatrix
global VdepPA

#global fungFinal

#fungFinal = []

lengthMatrix = []
final = []
saMatrix = []
PAtV = 0
PStV = 0
VdepPA = 0

#Constants
Ma = 10
Vs = 10 #10000
ImaxPA = 1.21 * (10**-7)
KminPA = 1.4 * (10**-5)

SAhyp = 15   #constant right now
Lhyp = 5    #constant right now
Rhyp = 2    #constant right now



#Initial Values
PSti = Vs
PAti = 0.001*Ma
PminA = 2.8 * (10**(-10))

Ivalues = [PAti, PSti]




def PdepA(PdepAval = 1, inflowVal = 1):
    PdepAnew = PdepAval + inflowVal
    return PdepAnew


"""Initial soil and fungi phosphorus concentration grid builidng"""
def buildSoil(size):
    soilMatrix = []
    for y in range(size):
        row = []
        for x in range (size):
            p= Ivalues[1]
            row.append(p)
        soilMatrix.append(row)
            
    return soilMatrix

def fungiInit(size):
    fI = []
    for y in range(size):
        row = []
        for x in range(size):
            PcF = (Ivalues[0] - 0.0001)
            row.append(PcF)
        fI.append(row)
    return fI



"Phos uptake from fungi from soil and plant from fungi"
def PuptA(PAt, VdepPA, SA):
    "Calculates the P uptake rate"
    PuptA = (SA * ImaxPA)* ((((PdepA(1,1) / VdepPA) - PminA) / (KminPA + ((PdepA(1,1) / VdepPA) - PminA))) * (1 - (1000 * PAt/Ma)))  # Calculated number is really really small
    return PuptA

def PuptPLfA(PAt):
    x = 0.025
    PuptPl = PAt*x
    return PuptPl 



"Amount of P in Fungi and soil at time t"
def PAt(PAtV, VdepPA, SA):
    "Takes in previous time step gram value of phos in A and returns new value"
    #print('PAt func PAtV value', PAtV)
    
    
    PAtN = PAtV +  PuptA(PAtV, VdepPA, SA) - PuptPLfA(PAtV)

    return PAtN

def PSt(PStV, PAtV, VdepPA, SA):
    "Takes in previous time step gram value of phos in S and returns new value"
    PStN = PStV - PuptA(PAtV, VdepPA, SA) 

    return PStN



"Determines new amount of P in fungi based on previous for TIMESTEPS"
def FungiC(timeStep, size, SAList, LMatrix):
    global PAtV
    
    Ma = 10
    Vs = 10 #10000
    ImaxPA = 1.21 * (10**-7)
    KminPA = 1.4 * (10**-5)
    
    SAhyp = 15   #constant right now
    Lhyp = 5    #constant right now
    Rhyp = 2    #constant right now
    
    
    
    fungFinal = []
    fungiInt = fungiInit(size)

    for xI in range(size):
        intTime = []
        for yI in range(size):
            intTime.append(fungiInt)
    
    fungFinal.append(fungiInt)
    
    for num in range(timeStep):

        timestep=[]
        for y in range(size):
            fungiList=[]
            for x in range(size):
                saVal = SAList[y][x]
                Lhyp = LMatrix[y][x]
                
                VdepPA = min((math.pi*Lhyp*((0.0018 + Rhyp)**2) - (Rhyp**2)), Vs)   

                previousF = fungFinal[num][y][x]
                
                PAtN = round(PAt(previousF, VdepPA, saVal), 9)  #PAtV
                fungiList.append(PAtN)
            timestep.append(fungiList)
        fungFinal.append(timestep)
        PAtV = PAtN

    return fungFinal



"Determines new amount of P in soil based on previous for TIMESTEPS"

def SoilC(timeStep, size, fungList, SAList, LMatrix):
    global PAtV
    global PStV
    global lengthMatrix
    
    Ma = 10
    Vs = 10 #10000
    ImaxPA = 1.21 * (10**-7)
    KminPA = 1.4 * (10**-5)
    
    SAhyp = 15   #constant right now
    Lhyp = 5    #constant right now
    Rhyp = 2    #constant right now
    
    
    #global fungFinal

    soilFinal = []
    soilInt = buildSoil(size)

    soilFinal.append(soilInt)    
    for num in range(timeStep):
        #print(num)
        timestep=[]
        for x in range(size):
            soilList=[]
            for y in range(size):
                saVal = SAList[x][y]
                
                Lhyp = LMatrix[y][x]
                
                VdepPA = min((math.pi*Lhyp*((0.0018 + Rhyp)**2) - (Rhyp**2)), Vs) #Phosphorus depletion zones for Arb. Works. cm^3   Not actually a constant
                
                previousS = soilFinal[num][x][y]

                previousF = fungList[num][x][y]

                PStN = round(PSt(previousS, previousF, VdepPA, saVal), 9)  #PAtV
                soilList.append(PStN)
            timestep.append(soilList)
            
            
        flowGrid = inflow(timestep, size)
        
        #print("ts", timestep)
        #print("flow", flowGrid)
        
        timeStepNew = []
        for x in range(size):
            row = []
            for y in range(size):
                newVal = timestep[x][y] + flowGrid[x][y]
                row.append(newVal)
            
            timeStepNew.append(row)
                
        soilFinal.append(timeStepNew)
    
    return soilFinal



"Calls on functions to create grids, and interate over them for TIMESTEPS and outputs a list of both lists of fungi and soil P amounts for every timestep for each cell in the grid"

def main(Steps, size):
    lengthMatrix = findLength()
    #print(lengthMatrix[8][8])
    for row in range(size):
        rowList = []
        for col in range(size):
            if lengthMatrix[row][col] == 0:
                SAval = 0
            else:
                SAval = (2 * math.pi * 0.0005 * (lengthMatrix[row][col])) #+ (2 * math.pi * (0.0005**2))
            rowList.append(SAval)
            
        saMatrix.append(rowList)
        
    #print(saMatrix)
            
    
    SoilInt = buildSoil(size)
    #print(SoilInt)
    
    PAtV = (Ivalues[0] - 0.0001) # added because uptake will calculate to zero otherwise
    #print(PAtV)
    PStV = Ivalues[1]
    #print(PStV)
        
    fung = FungiC(Steps, size, saMatrix, lengthMatrix)
    
    soil = SoilC(Steps, size, fung, saMatrix, lengthMatrix)
    
    final.append(fung)
    final.append(soil)
    print('fungi', final[0])         #final[fungi = 0, soil = 1][timestep][row][column]
    print('soil', final[1])
    
    print('Final', final)
    
    return final

final = main(3, 9)


    

    

"Writes text files to plot amounts"
#fung = final[0]

#soil = final[1]

#fungTest = ""

#for elt in fung:
    #fungTest=fungTest+str(elt)+"\n"
#print(fungTest)
#print(type(fungTest))

#file = open("funText.txt", "w")

#file.write(fungTest)

#file.close()

#soilTest = ""

#for elt in soil:
    #soilTest=soilTest+str(elt)+"\n"
#print(soilTest)
#print(type(soilTest))

#file = open("soilText.txt", "w")

#file.write(soilTest)

#file.close()

