from NewCode import*

desiredTS = 200
desiredSize = 199

def CalcED(ts, size):
    ratioList = []
    BioMassRatioList = []
    finalMainList =  main(ts, size)
    fungiList = finalMainList[1]

    lengthMatrix = useList('lenMatrix_199.txt')
    
    lengthTotal = 0
    for x in range(size):        #Adds up length of all hyphe in system
        for y in range(size):
            val = lengthMatrix[x][y]
            lengthTotal = lengthTotal + val
    #print("total length", lengthTotal)
    
    IndividualStepSums = []    
    for steps in range(ts):
        sumTotal = 0
        for x in range(size):
            for y in range(size):
                val = fungiList[steps][x][y]
                sumTotal =  sumTotal + val
        IndividualStepSums.append(sumTotal)
    #print(IndividualStepSums)
    #print("length", len(IndividualStepSums))
    
    mass = lengthTotal * 0.2 * math.pi * (0.0025**2)
     
    #print(IndividualStepSums)

    
    for steps in range(ts):
        
        ratio = IndividualStepSums[steps]/lengthTotal
        BMratio = IndividualStepSums[steps]/mass
        
        ratioList.append(ratio)
        BioMassRatioList.append(BMratio)
        
    #(BioMassRatioList)
    
    return BioMassRatioList

rList = CalcED(desiredTS, desiredSize)


def calDiff(list):
    derivList = []
    
    for step in range(len(list)):
        #print(step)
        if step == 0:
            pass
        else:
            val = list[step] - list[step - 1]
            
            derivList.append(val)
    
    #print(derivList)
    return derivList
  
  
#TestList = [2, 3, 4, 5]
    
deriv = calDiff(rList)



strTest =""

for elt in rList:
    strTest=strTest+str(elt)+"\n"
#print(strTest)
#print(type(strTest))

file = open("BioByLengtht.txt", "w")

file.write(strTest)

file.close()


rTest =""

for elt in deriv:
    rTest=rTest+str(elt)+"\n"
#print(strTest)
#print(type(strTest))

file = open("DerivList.txt", "w")

file.write(rTest)

file.close()