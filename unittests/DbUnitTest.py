'''
Created on 19.05.2014

@author: blicrain
'''

import viewdb
import unittest

class DbUnitTest(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self._updateCounter = 0
    
    def onUpdate(self):
        self._updateCounter = self._updateCounter+1
                
    def testPeristence(self):
        db = viewdb.DB()
        db.add("file", "lastviewed", "label")
        db.add("file2", "lastviewed2", "label2")
        self.assertEquals("DB(dictionary={'file2':('lastviewed2','label2'),'file':('lastviewed','label')})", str(db).replace("', '", "','"))
        
        onDisk = str(db)
        exec("db = viewdb."+onDisk)
        self.assertEquals("DB(dictionary={'file2':('lastviewed2','label2'),'file':('lastviewed','label')})", str(db).replace("', '", "','"))
        
    def testLoad(self):
        viewdb.load(["V1","DB(dictionary={'file2':('lastviewed2','label2'),'file':('lastviewed','label')})"])
        self.assertEquals("DB(dictionary={'file2':('lastviewed2','label2'),'file':('lastviewed','label')})", str(viewdb.db).replace("', '", "','"))
        

    def testAddingEntries(self):
        db = viewdb.DB()
        db.setOnUpdate(lambda : self.onUpdate())
        db.add("file", "lastviewed", "label")
        self.assertEquals(1, self._updateCounter)

        # adding same twice doesn't modify the counter
        db.add("file", "lastviewed", "label")
        self.assertEquals(1, self._updateCounter)

        # adding same twice doesn't modify the counter
        db.add("file", "lastviewedNew", "label")
        self.assertEquals(2, self._updateCounter)

        # adding same twice doesn't modify the counter
        db.add("file", "lastviewedNew", "labelNew")
        self.assertEquals(3, self._updateCounter)

if __name__ == "__main__":
    unittest.main()
