import spacy
from SpellCheck import SpellCheckResponse
from checkGreensheetAttribute import checkSubjectCode
from pattern import
nlp = spacy.load('en')
i=0
flag1 = 1

def checkSpelling(command,flag2):
    mainAttributes = []
    responseAttributes = []
    doc1 = nlp(command.decode("utf-8"))
    if flag2 == 0:
        for word in doc1:
             if word.pos_ == "NOUN":
                if i < 3:
                    print "input mainAtrr"
                    mainAttributes.append(word)


                elif i > 2:
                    print "Input response Att"
                    responseAttributes.append(word)
                i = i + 1

        checkGreensheet = checkSubjectCode(mainAttributes)
        if checkGreensheet == False:
            return "Hello there, I cannot find the GreenSheet you are seeking for try seaching for Something GreenSheet."

        for word in responseAttributes:
            print  "Checking spell check response"
            if SpellCheckResponse(word) == False:
                print "found an spelling error"
                temp = str(word)
                tem_str = suggest(temp)
                return "Hey I see There Is something wrong with the Spelling you provided. Do you mean " + str(
                    tem_str) + "  instead of " + "'" + str(word) + "'"
                flag1 = 0

        if flag1 == 1:
            return 1

    else:
        for word in doc1:
            if word.pos_ == "NOUN":
             print "input mainAtrr"
             mainAttributes.append(word)

            for word in mainAttributes:
             print  "Checking spell check response"
             if SpellCheckResponse(word) == False:
                 print "found an spelling error"
                 temp = str(word)
                 tem_str = suggest(temp)
                 return "Hey I see There Is something wrong with the Spelling you provided. Do you mean " + str(
                     tem_str) + "  instead of " + "'" + str(word) + "'"
                 flag1 == 1

        if flag1 == 1:
            return 1
