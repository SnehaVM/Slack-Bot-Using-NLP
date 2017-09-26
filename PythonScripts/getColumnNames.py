import time
import os
import MySQLdb



def getAllColumns(table):   
    allColumns = set()
    #global allColumns
    db = MySQLdb.connect("localhost","root","Apple@123","testdb" )
    cursor = db.cursor()
    sql = """ SHOW COLUMNS FROM %s """ %table
    cursor.execute(sql)
    fields=cursor.fetchall()
    counter = 0
    for field in fields:
            allColumns.add(field[0])
    cursor.close()
    db.close()
    return allColumns

def eliminateSelectColumns(selectColumns,allColumns):
    allColumns=set(allColumns)
    selectColumns=set(selectColumns)
    whereColumns = allColumns - selectColumns
    return whereColumns

#Sample Input
#table="CourseSchedule"
#allColumns=getAllColumns(table)    
#selectColumns=set()
#selectColumns.add("Week")
#whereColumns=eliminateSelectColumns(selectColumns,allColumns)
#print whereColumns

