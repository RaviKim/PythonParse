import json

def readFiles(sFileLocation, sFromFileName):
    with open(sFileLocation + sFromFileName, mode="rt", encoding='utf-8') as f:
        stringList = f.readlines()
        item = stringList[0]
        print(item)

        for item in stringList:
            jsonObject = json.loads(item)
            print(jsonObject['startTimestamp'] + " " + jsonObject['endTimestamp'])

fileLocation = "./"
readFiles(fileLocation, "output_cleand.txt")
