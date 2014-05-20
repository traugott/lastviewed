REMOTE_DBG = False 

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
import viewdb
import xbmcinteg

xbmcinteg.loadDb()

addon_handle = int(sys.argv[1])

xbmcplugin.setContent(addon_handle, 'movies')

l = viewdb.db.getOrderedLastViewedList()
for t in l:
    li = xbmcgui.ListItem(t[0], iconImage='DefaultVideo.png')
    xbmcplugin.addDirectoryItem(addon_handle, t[1], li)

xbmcplugin.endOfDirectory(addon_handle)
