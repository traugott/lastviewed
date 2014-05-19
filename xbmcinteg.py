'''
Created on 19.05.2014

@author: blicrain

Integration with xmbc 
'''

import xbmc

def getPlaying():
    """ No input params
    
    Returns a tuple (file,label,lastplayed)
    """
    
    try:
        response = ""
        exec("response = "+xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "Player.GetActivePlayers", "id": 1 }'))
        result = response["result"]
        if (len(result) > 0):
            if "video" == result[0]["type"]:
                response = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "Player.GetItem", "id": '+str(result[0]["playerid"])+', "params" : {"playerid":1,"properties":["lastplayed","file"]} }')
        
                filename = response["result"]["item"]["file"]
                label = response["result"]["item"]["label"]
                lastplayed = response["result"]["item"]["lastplayed"]
                return (filename,label,lastplayed)
        return None
                
    except Exception as inst:
        print type(inst)
        return None

