REMOTE_DBG = True 

import sys

# append pydev remote debugger
if REMOTE_DBG:
    # Make pydev debugger works for auto reload.
    # Note pydevd module need to be copied in XBMC\system\python\Lib\pysrc
    try:
        import pysrc.pydevd as pydevd
    # stdoutToServer and stderrToServer redirect stdout and stderr to eclipse console
        pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True)
    except ImportError:
        sys.stderr.write("Error: " +
            "You must add org.python.pydev.debug.pysrc to your PYTHONPATH.")
        sys.exit(1)

        
import xbmcplugin
import xbmcgui
import xbmc

addon_handle = int(sys.argv[1])

try:
#    response = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "JSONRPC.Introspect", "id": 1 }')
#    f = open("D:\\rcp.txt", "w")
#    f.write(response)
#    f.close()
    exec("response = "+xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "Player.GetActivePlayers", "id": 1 }'))
    result = response["result"]
    if (len(result) > 0):
        if "video" == result[0]["type"]:
            response = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "Player.GetItem", "id": '+str(result[0]["playerid"])+', "params" : {"playerid":1,"properties":["lastplayed","file"]} }')
    
            print response
except Exception as inst:
    print type(inst)


xbmcplugin.setContent(addon_handle, 'movies')

url = 'http://localhost/some_video.mkv'
li = xbmcgui.ListItem('My First Video!', iconImage='DefaultVideo.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

xbmcplugin.endOfDirectory(addon_handle)
