tableDict = {}
columnDict = {}

#test paths
path_tables = '/home/poojitha/Documents/tables.txt'
path_columns = '/home/poojitha/Documents/Project/'

def createDictionary():    
    readFromFile(path_tables,"tables")
   
#reads from text file and create dictionaries
def readFromFile(filePath, category):    
    if(category == "columns"):
        #build path for fetching columns
        filePath = path_columns + filePath +"/columns.txt"
    try:
        infile = open(filePath,'r')
        for line in infile:
            line = line.strip()            
            name = str(line.split(";")[0:1])
            line = str(line.split(";")[1])
            parts = [p.strip() for p in line.split(",")]            
            if(category == "tables"):
                tableDict[name] = (parts[0:])                
            elif (category == "columns"):
                #columnDict[parts[0]] = (parts[1:])
                columnDict[name] = (parts[0:])
    except IOError:
        print "Could not read file:", filePath

#search dictionary values to find the key
def searchDictionary(dict_name,word_input):
    for k, v in dict_name.iteritems():
       if word_input in v:
          return k
