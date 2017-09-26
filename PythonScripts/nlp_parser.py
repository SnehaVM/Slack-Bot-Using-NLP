import spacy
import re
from nltk import Tree
from nltk.corpus import stopwords
from file_reader import *
from generateQuery import *
from datetime import datetime
from nltk import word_tokenize
import parsedatetime as pdt # $ pip install parsedatetime
from word2num import *
from greenSheetResponse import *

cal = pdt.Calendar()

FROM_token = ''
cols = list()

CMD = ''
nlp = spacy.load('en')
subjectcode = ''
sectionname = ''
sectionperiod = ''
inputCmd = ''
resetFlag = 0
outputHeader = ''


def nlp_parseInput(command):

 try:  
    global CMD ,subjectcode ,sectionname, sectionperiod, dateValue,resetFlag,outputHeader,inputCmd,prefix
    print "************command ",command  
    inputCmd = command    
    dateChk = command.encode('ascii','ignore')    
    dateValue = ''
    # if (str(cal.parseDT(dateChk)[0]) != datetime.now().strftime('%Y-%m-%d %H:%M:%S')):         
    #     dateValue=str(cal.parseDT(dateChk)[0].date())    
    if (str(cal.parseDT(dateChk.strip('?'))[0]) != datetime.now().strftime('%Y-%m-%d %H:%M:%S')):         
        dateValue=str(cal.parseDT(dateChk.strip('?'))[0].date())        

    print dateValue 
    print "dateChk:", dateChk
    GREETLIST = ['hi','hello','hey','hi there','hey there','wassup','whatssup'] 
    if command in GREETLIST:
        response = "hello, try asking something from greesheet. For Example: cmpe273 section2 spring,2017 who is the instructor? and Type 'change' when you wish to change the course or term"
        return response       

    if len(command.strip().split()) <= 1:
        print "inside single token",dateChk
        print type(dateChk)
        if dateChk.strip() == 'change':
            print "inside change"
            resetFlag = 0  
            outputHeader=''
            print "outputHeader",outputHeader
            return "Resetting the course details. Submit your next query with the course details.For Example: cmpe273 section2 spring,2017, who is the instructor? and Type 'change' when you wish to change the course or term"
        else:    
            print 'else block'
            return None
  
    if resetFlag == 0:
        primaryKey = command.split(' ')        
        subjectcode = primaryKey[0]
        sectionname = primaryKey[1]
        sectionperiod = primaryKey[2].rstrip(',')
        if subjectcode.startswith('cmpe') and sectionname.startswith('section'):                
            #print sectionperiod
            outputHeader = "**%s**%s**%s**"%(subjectcode,sectionname,sectionperiod)
            print outputHeader
            occur = 3  
            indices = [x.start() for x in re.finditer(" ", command)]    
            command = command[indices[occur-1]+1:]
            resetFlag = 1
        else: 
            return "Please provide the course details you wish to query for"
    elif command.startswith('cmpe'):
        occur = 3  
        indices = [x.start() for x in re.finditer(" ", command)]    
        command = command[indices[occur-1]+1:]    

               
    command = word2int(command)
    print command
    CMD = command   
    print CMD
    parsedEx = nlp(command.decode('utf-8'))
    print parsedEx
    tokens = lemmatizeTokens(parsedEx)    
    print "tokens",tokens
    return "%s\n%s"%(outputHeader,removeStopWords(tokens))
    
 except:
    return None

def removeStopWords(tokens):
    global FROM_token,CMD
    #strCmd = CMD.split(",")[0:]
    STOPLIST = set(stopwords.words('english'))
    #customize stopwords to add/remove words    
    QUE_LIST = ['what','when','who','where','how']
    STOPLIST = [q for q in STOPLIST if q not in QUE_LIST]
    STOPLIST.append('?')
    tokens_filtered = [tok for tok in tokens if tok not in STOPLIST]   
    FROM_token = findTableorCol(tokens_filtered,"table")
    #if no table found, do not search for cols
    if(FROM_token):       
        cols = findTableorCol(CMD,"columns")
        if(len(cols) == 0):
            cols.append("*")
    #new sentence without stop words
    #new_sentence = ' '.join(tokens_filtered)       
    return dependecyParse(CMD)
     
def lemmatizeTokens(tokens):
    lemmas = []
    for tok in tokens:
        lemmas.append(tok.lemma_.lower().strip() if tok.lemma_ != "-PRON-" else tok.lower_)
    tokens = lemmas
    return tokens

#call file_reader module to find tablename & column name
def findTableorCol(tokens_filtered,key):
    global cols,CMD
    fromTable =''
    columnList = list()   
    if(key == "table"):
        parsedEx = nlp(CMD.decode('utf-8'))
        tokens = lemmatizeTokens(parsedEx)
        toks = ' '.join(tokens)
        lhLis= findLeafHead(toks,"leafhead")
        for l in lhLis:
            table_name = searchDictionary(tableDict,l)
            #read columns only when we know the table            
            if(table_name != None):         
                fromTable = table_name.strip("['']")
                columnDict.clear()
                readFromFile(fromTable,"columns")
                FROM_token = fromTable
                return FROM_token       
        if(fromTable == ''):
            lhLis= findLeafHead(toks,"headleaf")
            for l in lhLis:
                table_name = searchDictionary(tableDict,l)
            #read columns only when we know the table            
                if(table_name != None):      
                    fromTable = table_name.strip("['']")
                    columnDict.clear()
                    readFromFile(fromTable,"columns")
                    FROM_token = fromTable
                    return FROM_token
        if(fromTable == ''):
            for t in tokens_filtered:
                #print tokens_filtered
                table_name = searchDictionary(tableDict,str(t))
                #read columns only when we know the table            
                if(table_name != None):                   
                    fromTable = table_name.strip("['']")
                    columnDict.clear()
                    readFromFile(fromTable,"columns")
                    FROM_token = fromTable
                    return FROM_token
    #add columns to list
    elif (key == "columns"):
        lhLis = list()
        hList =list()
        parsedEx = nlp(tokens_filtered.decode('utf-8'))
        tokens = lemmatizeTokens(parsedEx)
        #new sentence without stop words
        toks = ' '.join(tokens)        
        lhLis= findLeafHead(toks,"leafhead")     
        if(len(lhLis) > 0):           
            for l in lhLis:
                col_name = searchDictionary(columnDict,str(l))
                if(col_name != None):
                    columnList.append(col_name.strip("['']"))
        #else search headleaf    
        hList= findLeafHead(toks,"headleaf")
        for l in hList:
            col_name = searchDictionary(columnDict,str(l))
            if(col_name != None):
                columnList.append(col_name.strip("['']"))
        if (len(columnList) == 0) or (" and " in CMD):
            print "CMD", CMD
            for t in tokens:
                col_name = searchDictionary(columnDict,str(t))
                if(col_name != None):
                    columnList.append(col_name.strip("['']"))
        cols = columnList               
        return cols


def to_nltk_tree(node):
    if node.n_lefts + node.n_rights > 0:
        return Tree(node.orth_, [to_nltk_tree(child) for child in node.children])
    else:
        return node.orth_

def findLeafHead(command,key):
    leafList = list()
    headList = list()
    parseDep = nlp(command.decode('utf-8'))
    for token in parseDep:
        leaf= str(token.orth_.encode('utf-8'))
        head=str(token.head.orth_.encode('utf-8')) 
        print leaf,head
        if(key=="leafhead"):
            if(head==leaf):
                leafList.append(leaf.strip())
            else:
                leafList.append(leaf.strip() + "_" + head.strip())            
        elif(key == "headleaf"):
            #print "hleaf",head.strip() + "_"+leaf.strip()
            if(head==leaf):
                headList.append(leaf.strip())
            else:
                headList.append(head.strip() + "_"+leaf.strip())  
    if(len(leafList)> 0):
        return leafList
    elif(len(headList)>0):       
        return headList
    else:
        return leafList

def cleanText(leaf1):  
  
    CheckLIST = set(stopwords.words('english'))   
    CheckLIST.add('?')    
    #print CheckLIST
    #print "three"
    if leaf1 not in CheckLIST:
        #print "token aftr: ", leaf1
        return leaf1
    else:       
        return None
        
   
#find dependency between words
def dependecyParse(command):
    global dateValue
    parseDep = nlp(command.decode('utf-8'))
  
    #process_command(command)
    print FROM_token
    print "---dependency tree----"
    [to_nltk_tree(sent.root).pretty_print() for sent in parseDep.sents] 
    if FROM_token and '*' not in cols:
        if dateValue:            
            output = generateQueryOne(FROM_token,cols,dateValue,subjectcode, sectionname,sectionperiod)
            if(output):
                return output
            else:
                return "No results found"
        for token in parseDep:           
                        
            #print(token.orth_.encode('utf-8'), token.dep_.encode('utf-8'), token.head.orth_.encode('utf-8'), [t.orth_.encode('utf-8') for t in token.lefts], [t.orth_.encode('utf-8') for t in token.rights])                
            #print token.orth_.encode('utf-8'),token.head.orth_.encode('utf-8')      
            leaf= str(token.orth_.encode('utf-8'))
            head=str(token.head.orth_.encode('utf-8'))
            #call generateQuery module
            #print "bef"
            lf = cleanText(leaf)
            #print "aft"
            hd = cleanText(head)  
            #print "aft2"        
            if(lf and hd):
                print "lf and hd:" ,lf,hd
                searchCondition = "%"+lf+"%""%"+hd+"%"                        
                output = generateQueryOne(FROM_token,cols,searchCondition,subjectcode, sectionname,sectionperiod )
                if output:
                    return output                                
                searchCondition = "%"+hd+"%""%"+lf+"%"        
                output = generateQueryOne(FROM_token,cols,searchCondition,subjectcode, sectionname,sectionperiod )
                if output:
                    return output
        for token in parseDep:
            print "token"
            tk= str(token.orth_.encode('utf-8'))  
            tk = cleanText(tk)
            print "orth: ",tk          
           # print "tk: ",tk        
            if(tk):
                if(len(tk)>1):
                    print "tk: ",tk      
                    token= "%"+str(tk)+"%" 
                    print "indiv token: ", token        
                    output = generateQueryOne(FROM_token,cols,token,subjectcode, sectionname,sectionperiod)
                    if output:
                        return output 
        print "calling..."       
        
        output = generateQueryTwo(FROM_token,cols,subjectcode, sectionname,sectionperiod)
        if(output):
            return output
        else:
            return "No results found"    
    else:
        return DB_Response(inputCmd)
#method to find nouns, verbs ..
def process_command(command):
    command = "when is lab30 due?"
    tokens = nlp(command.decode('utf-8'))
    verbArr =[]
    nounArr = []
    numArr =[]
    entityArr =[]
    AdverbArr = []
    #filter out nouns
    for np in tokens.noun_chunks:
        
        nounArr.append(np)
        #filter out entities
        for ent in tokens.ents:
            entityArr.append(ent)
            #filter out verbs, numbers and adverbs
            for token in tokens:
                #print token,token.pos_
                if "VERB" in token.pos_:
                    verbArr.append(token)
                elif "NUM" in token.pos_:
                    numArr.append(token)
                elif "ADV" in token.pos_:
                    AdverbArr.append(token)
    print "verbs: " ,verbArr
    print "nouns: " ,nounArr
    print "adverbs: ",AdverbArr
    #response = "Sure...write some more code then I can do that!"
    #else:
        #response = "I am CMPE bot. How can I help you? Use the *" + EXAMPLE_COMMAND + \
                      #"* command while asking questions."
    #return response
