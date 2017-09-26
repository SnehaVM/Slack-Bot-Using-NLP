
import MySQLdb


db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="greensheet",         # your username
                     passwd="root1234",  # your password
                     db="slackbot")    # name of the data base
cur = db.cursor()
query = "SELECT subject_code,section_name,section_period FROM greensheet1"
cur.execute(query)
cur.execute(query)
attributeToCheck = cur.fetchall()

def checkSubjectCode(Attributes):
    temp = str(attributeToCheck).replace("'","")
    temp2= str(Attributes).replace("[","").replace("]","")
    print temp2
    print temp
    if temp2 in temp:
        print "The macth was succefull"
        return True
    else:
        print " the match was not succefull"
        return False


db.close()
