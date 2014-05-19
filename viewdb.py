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
        
    def __str__(self):
        """ Returns a string which can be executed to restore the DB. Used to persist this object"""
        
        repl = "DB(dictionary={"
        for entry in self._dictionary.keys():
            repl = repl + "'" + entry + "':" + str(self._dictionary[entry])+","
        if (len(self._dictionary.keys()) > 0):
            repl = repl[:-1]
        repl += "})"
        return repl
    
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


db = DB()

def load(configLines):
    if len(configLines) == 0:
        return
    if configLines[0] == "V1":
        exec("global db\ndb="+configLines[1])
    else:
        return
