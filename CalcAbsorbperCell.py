from NewCode import*


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


def totalLength(size):
    
    lengthMatrix = useList('lenMatrix_199.txt')
    
    lengthTotal = 0
    
    for x in range(size):
        for y in range(size):
            val = lengthMatrix[x][y]
            lengthTotal = lengthTotal + val
            
    return lengthTotal
    
def sumListFinal(list, pos):
    listtotalFinal= 0
    for x in range(199):
        for y in range(199):
            val = list[pos][x][y]
            #print(val)
            
            listtotalFinal = listtotalFinal + val
            
    return listtotalFinal
   
   
def sumListTS(list):
    tsSUMList = []
    
    for step in range(30):
       
        tsSUM = sumListFinal(list, step)
    
        tsSUMList.append(tsSUM)
        
    print(tsSUMList)
    
    return tsSUMList
            
    

def totalAbPbyLength():
    final = main(30, 199)
    fungi = final[1]
    #print(fungi)
    
    tL = totalLength(199)
    #print(tL)
    
    fungiPTotal = sumListFinal(fungi, 29)
    
    
    ratioFinal = fungiPTotal/tL
    
    tsListVals = sumListTS(fungi)
    tsRatioList = []
    for step in range(30):
        ratioVal = tsListVals[step]/tL
        
        tsRatioList.append(ratioVal)
        
        
    
    return tsRatioList
    
    
    
print(totalAbPbyLength())
    
    
    
    
    
    