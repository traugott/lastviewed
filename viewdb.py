'''
Created on 19.05.2014
Contains the db for lastviewed and the unit tests

@author: blicrain
'''

class DB():
    """ The poor-mans-db for the lastviewed addon. Class contains a dictionary pointing from filename to a tuple(lastviewed, label) where
    lastviewed is a sortable string representation of the last viewing point in time and label can be displayed in the xbmc gui
    """
    
    def __init__(self, **params):
        """Inits the DB.
        
        The following params are supported:
        dictionary:
            The dictionary has to have the form
            {<file>:(<lastviewed>, <label>)*}
            file, lastviewed and label are all strings.
            Used to restore the db from disk
            
        onUpdate:
            gets called if there is an update of the db. Used to save the db to disk
        """
        
        if ("dictionary" in params):
            self._dictionary = params["dictionary"]
        else:                
            self._dictionary = {}
        
        if ("onUpdate" in params):
            self._onUpdate = params["onUpdate"]
        else:
            self._onUpdate = lambda : ""

    def setOnUpdate(self, onUpdate):
        """ Sets the onUpdate listener. gets called if there is an update of the db. Used to save the db to disk """
        
        self._onUpdate = onUpdate
    
    def __quote(self, text):
        import urllib
        return urllib.quote(text)
    
    def __unquote(self, text):
        import urllib
        return urllib.unquote(text)
        
    def __str__(self):
        """ Returns a string which can be executed to restore the DB. Used to persist this object"""
        
        arr = []
        for entry in self._dictionary.keys():
            t = (self.__quote(entry), self.__quote(str(self._dictionary[entry][0])),self.__quote(self._dictionary[entry][1]))
            arr.append(t)
        return str(arr)
    
    def add(self, filename, lastviewed, label):
        """ Adds an Entry to this db. Returns True if db has changed, otherwise False"""
        if (filename in self._dictionary):
            lv, lab = self._dictionary[filename]
            if lv != lastviewed or lab != label:
                self._dictionary[filename] = (lastviewed, label)
                self._onUpdate()
                return True
            return False
        else:
            self._dictionary[filename]=(lastviewed, label)
            self._onUpdate()
            return True
    
    def getOrderedLastViewedList(self):
        """ Return [(label:string, filename:string, lastviewed:int)*], ordered by lastviewed-date"""
        returnList = []
        for filename in self._dictionary.keys():
            t = self._dictionary[filename]
            returnList.append((t[1], filename, t[0]))
        returnList = sorted(returnList, key=lambda x:x[2], reverse=True)
        return returnList

    def load(self, configLines):
        """ Loads the db from the config lines 
        First line is the version
        "V1" - not supported anymore
        "V2" - next line is an array in the following form [(<file>,<lastviewed>,<label>)*]
        """
        if len(configLines) == 0:
            return
        if configLines[0] == "V1":
            global db  # Sorry, old format is not supportable anymore
            db = DB()
        elif configLines[0] == "V2":
            arr=[]
            exec("arr="+configLines[1])
            self._dictionary.clear()
            for t in arr:
                t = (self.__unquote(t[0]),self.__unquote(t[1]),self.__unquote(t[2]))
                self.add(*t)

    def save(self):
        try:
            import os, xbmcvfs
            
            configFile = xbmcvfs.File("special://home/lastviewed_db", "w")
            configFile.write("V2"+os.linesep)
            configFile.write(str(db)+os.linesep)
            configFile.close()
        except Exception as e:
            print e

    def clear(self):
        self._dictionary.clear()
db = DB()

