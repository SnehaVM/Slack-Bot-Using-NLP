import spacy
from SpellCheck import SpellCheckResponse
import MySQLdb
import enchant
from checkGreensheetAttribute import checkSubjectCode
import getColumnandTableName
import enchant



d = enchant.Dict("en_US")
nlp = spacy.load('en')
def DB_Response(command,gloBalVariable):

    db = MySQLdb.connect(host="127.0.0.1",  # your host, usually localhost
                         user="greensheet",  # your username
                         passwd="root1234",  # your password
                         db="slackbot")  # name of the data base

    cur = db.cursor()
    i = 0
    flag = 0

    mainAttributes = []
    responseAttributes = []
    doc1 = nlp(command.decode("utf-8"))
    for word in doc1:
            if word.pos_ == "NOUN":
                if i <3:
                    print "input mainAtrr"
                    mainAttributes.append(word)


                elif i > 2:
                    print "Input response Att"
                    responseAttributes.append(word)
                i = i + 1

    checkGreensheet =  checkSubjectCode(mainAttributes)
    if checkGreensheet == False:
        return "Hello There I cannot find the GreenSheet you are seeking for try seaching for someother GreenSheet."

    for word in responseAttributes:
           print  "Checking spell check response"
           if SpellCheckResponse(word) == False:
            print "found an spelling error"

            temp = str(word)
            tem_str=d.suggest(temp)
            return "Hey I see There Is something wrong with the Spelling you provided. Do you mean " + str(tem_str)  + "  instead of "+ "'"+ str(word)+"'"



    if flag == 1:
        print "Finally got every thing All right"
        tempColoumn, table = getColumnandTableName.getColumnAndTableName(responseAttributes)
        if tempColoumn == None:
            return "Hey I cannot fetch the result for your query, please try re-phrashing the question"
        print tempColoumn
        query = "SELECT " + str(tempColoumn) + " FROM " + str(table) +" where subject_code=" + "'" + str(mainAttributes[0]) + "' and section_name =" + "'" + str(mainAttributes[1]) + "' and subject_term=" + "'" + str(mainAttributes[2]) + "';"
        print query
        cur.execute(query)
        response = cur.fetchall()
        return str(response).replace("(","").replace(")","")
    else:
        print "Test from Hello"
        response = 'Hello There there, Try asking me something from your greesheet For Example: cmpe273 section2 spring,2017, who is the instructor?'
        return response
    cur.close()
    db.close()
