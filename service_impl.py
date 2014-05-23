'''
Created on 23.05.2014

@author: blicrain
'''


import viewdb
import time


lastviewed = 0
lastfilename = "";
lastlabel = "";
timeGetter = lambda : int(round(time.time()))
def doService(getPlaying):
    """ request the currently played video from xbmc and stores it in the database

    getPlaying is a function to be called and has to return (filename, label) or None    
    This method should be called frequently
    """
    
    try:
        t = getPlaying()
        if t != None:
            global lastviewed, lastfilename, lastlabel
            filename, label = t
            if lastfilename != filename or lastlabel != label:
                lastfilename = filename
                lastlabel = label
                lastviewed = timeGetter()
                viewdb.db.add(filename, lastviewed, label)
        else:
            lastfilename = None
    except Exception as inst:
        print type(inst)

def clear():
    global lastviewed, lastfilename, lastlabel
    lastviewed = 0
    lastfilename = "";
    lastlabel = "";

def setTimeGetter(getTime):
    global timeGetter
    timeGetter = getTime    