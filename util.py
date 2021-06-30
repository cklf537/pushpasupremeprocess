# helper methods
 
import configparser

config = configparser.ConfigParser()
# configFile = 'config-dev.ini'

configDictionary = {}

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

# getConfigProperties(configFile)
