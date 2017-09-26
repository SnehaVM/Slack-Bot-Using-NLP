import json
import os


def saveWordsToFile(list):
        with open("trainingData.txt", "r+") as f:
            fileContent = f.read()
            jsonDataDict = {}
            if os.path.getsize("trainingData.txt") > 0:
                jsonDataDict = json.loads(fileContent)

            jsonDataDict[str(list)] = "toBeTrained"

            f.seek(0)
            json_data = json.dumps(jsonDataDict, encoding='ascii')
            f.write(json_data)
            f.truncate()

