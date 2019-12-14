import json

configFile = 'static/config.json'

with open(configFile) as jsonFile:
    data = json.load(jsonFile)
    print(data['owAPI_key'])
