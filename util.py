# helper methods
 
import configparser

config = configparser.ConfigParser()
# configFile = 'config-dev.ini'

configDictionary = {}
dbxAssetIds = []

def getConfigProperties(config_file):
    config.read(config_file)
    configSections = config.sections()
    for secKey, section in enumerate(configSections):
        configDictionary.update({section: []})
        if section is not None:
            for (k,v) in config.items(section):
                # configSection = configDictionary[section]
                configDictionary[section].append({k:v})
    return configDictionary

def stripAndCompareFBAndDBXId(dbxObject, gsObject):
    gsFbPosId = stripGsObject(gsObject)
    dbxAssetIds = stripDbxObjectId(dbxObject)

def stripGsObject(gs_Object):
    gsIds = gs_Object.split('/')
    return gsIds[len(gsIds)-1][:7]

def stripDbxObjectId(dbx_Object):
    dbxIdDict = {}
    for k, val in enumerate(dbx_Object):
        dbxIds = val[0].split('/')
        dbxId = ((dbxIds[len(dbxIds)-1]).split('_')[1])[:7]
        dbxIdDict.update({dbxId:val[0]})
    return dbxIdDict


# getConfigProperties(configFile)
