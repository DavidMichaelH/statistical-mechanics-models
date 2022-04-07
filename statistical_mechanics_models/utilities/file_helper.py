 
class FileHelper:
    
    def WriteListToCsv(listToWrite,FILE_NAME):
        file = open(FILE_NAME, "a")
        for itr in range(len(listToWrite)):    
            outstr = str(listToWrite[itr])
            file.write(outstr[1:-1] + "\n")
        file.close()
        
        
        
    def ReadCsvToList(FILE_NAME):
        file = open(FILE_NAME, "r")
        inputStr = file.read()
        linesArray = inputStr.split("\n")
        numArray = []
        for itr in range(len(linesArray)):
            
            if linesArray[itr].replace(" ", "") == "":
                continue 
            
            values = linesArray[itr].split(",")
            
            lineArray = []
            
            for v in range(len(values)):
                lineArray.append(float(values[v]))
            
            
            numArray.append(lineArray)
        
        return numArray
 