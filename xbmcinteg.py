'''
Created on 19.05.2014

@author: blicrain

Integration with xmbc 
'''

import xbmc
import viewdb

def getPlaying():
    """ No input params
    
    Returns a tuple (file,label,lastplayed)
    """
    
    try:
        response = {}
        exec("response = "+xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "Player.GetActivePlayers", "id": 1 }'))
        result = response["result"]
        if (len(result) > 0):
            if "video" == result[0]["type"]:
                response = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "Player.GetItem", "id": '+str(result[0]["playerid"])+', "params" : {"playerid":1,"properties":["lastplayed","file"]} }')
                exec("result = "+response)
                
                filename = result["result"]["item"]["file"]
                label = result["result"]["item"]["label"]
                lastplayed = result["result"]["item"]["lastplayed"]
                return (filename,label,lastplayed)
        return None
                
    except Exception as inst:
        print type(inst)
        return None

def loadDb():
    try:
        import xbmcvfs, os
        configFile = xbmcvfs.File("special://home/lastviewed_db", "r")
        stringWithLines = ""
        stringWithLines = configFile.read()
        lines = stringWithLines.split(os.linesep)
        viewdb.load(lines)
        configFile.close()
    except:
        pass

def saveDb():
    try:
        viewdb.save()
    except:
        pass
        
