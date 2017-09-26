import time
import os
import MySQLdb
from getColumnNames import *
from dateutil import parser
from datetime import datetime
import datetime

#Generate query 
def generateQueryOne(fromTable,selectColumns,searchCondition,subjectcode, sectionname,sectionperiod):
    #subjectcode = int(filter(str.isdigit, str(subjectcode)))
    allColumns = getAllColumns(fromTable)
    #print searchCondition
    selectColumns = set(selectColumns)       
    whereColumns = eliminateSelectColumns(selectColumns,allColumns)       
    db = MySQLdb.connect("localhost","root","*****","273bOT" )
    cursor = db.cursor()
    data=None       
    selectString=None        
    if len(selectColumns)>1:
        selectString = ', '.join(str(e) for e in selectColumns) 
        
    else:
        selectString= ','.join(str(s) for s in selectColumns)   
    print "selectColumns",selectColumns    
    #print "wherecol",whereColumns         
    for column in set(whereColumns):     
        #print column            
        #print "SELECT %s from %s where replace(%s,' ','') like ('%s') and subject_code=trim('%s') and section_name=trim('%s') and subject_term=trim('%s');"%(selectString,fromTable,column,searchCondition,subjectcode, sectionname,sectionperiod)
        rows_affected = cursor.execute("SELECT %s from %s where replace(%s,' ','') like ('%s') and subject_code=trim('%s') and section_name=trim('%s') and subject_term=trim('%s');"%(selectString,fromTable,column,searchCondition,subjectcode, sectionname,sectionperiod))                   
        data = cursor.fetchall()        
        if rows_affected >1:                                  
            cursor.execute("SELECT %s,%s from %s where replace(%s,' ','') like ('%s') and subject_code=trim('%s') and section_name=trim('%s') and subject_term=trim('%s');"%(column,selectString,fromTable,column,searchCondition,subjectcode,sectionname,sectionperiod))                           
            data = cursor.fetchall()
                  
        data='\n'.join(''.join(str(elems)) for elems in data)    
        data = data.replace("'","").replace('(', '').replace(')', '').replace('datetime.date', '')
          
        if data:                 
            if  "date" in selectColumns:
                data=data.replace(',','-')
                data=data.rstrip('-')
            print "Output : %s " % data 
            data = data.rstrip(',')
            return data 
    return None


def generateQueryTwo(fromTable,selectColumns,subjectcode, sectionname,sectionperiod):
    #subjectcode = int(filter(str.isdigit, str(subjectcode)))   
    allColumns = getAllColumns(fromTable)
    selectColumns = set(selectColumns)        
    print "all cols", allColumns        
    db = MySQLdb.connect("localhost","root","*****","273bOT" )
    cursor = db.cursor()
    data=None       
    selectString=None        
    if len(selectColumns)>1:
        selectString = ', '.join(str(e) for e in selectColumns) 
        
    else:
        selectString= ','.join(str(s) for s in selectColumns)  
    #print "SELECT %s from %s where subject_code=trim('%s') and section_name=trim('%s') and subject_term=trim('%s');"%(selectString,fromTable,subjectcode, sectionname,sectionperiod)

    rows_affected = cursor.execute("SELECT %s from %s where subject_code=trim('%s') and section_name=trim('%s') and subject_term=trim('%s');"%(selectString,fromTable,subjectcode, sectionname,sectionperiod))                   
    data = cursor.fetchall()        
    data='\n'.join(''.join(str(elems)) for elems in data)    
    data = data.replace("'","").replace('(', '').replace(')', '').replace('datetime.date', '')
    print "data",data      
    if data:                 
        if  "date" in selectColumns:
                data=data.replace(',','-')
                data=data.rstrip('-')
        print "Output : %s " % data 
        data = data.rstrip(',')
        return data
    return None
