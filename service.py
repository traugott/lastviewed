'''
Created on 17.05.2014

@author: blicrain
'''

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

        
import viewdb
import xbmcinteg

xbmcinteg.loadDb()

viewdb.db.setOnUpdate(lambda :viewdb.db.save())
    
while True:
    import service_impl,time
    service_impl.doService(xbmcinteg.getPlaying)
    time.sleep(5)
