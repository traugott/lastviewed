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
        self.assertEquals("DB(dictionary={r'file2':(r'lastviewed2',r'label2'),r'file':(r'lastviewed',r'label')})", str(db).replace("', '", "','"))
        
        onDisk = str(db)
        exec("db = viewdb."+onDisk)
        self.assertEquals("DB(dictionary={r'file2':(r'lastviewed2',r'label2'),r'file':(r'lastviewed',r'label')})", str(db).replace("', '", "','"))
        
    def testLoad(self):
        viewdb.load(["V1","DB(dictionary={r'file2':(r'lastviewed2',r'label2'),r'file':(r'lastviewed',r'label')})"])
        self.assertEquals("DB(dictionary={r'file2':(r'lastviewed2',r'label2'),r'file':(r'lastviewed',r'label')})", str(viewdb.db).replace("', '", "','"))
        
    def testAddingEntries(self):
        db = viewdb.DB()
        db.setOnUpdate(lambda : self.onUpdate())
        db.add("file", "lastviewed", "label")
        self.assertEquals(1, self._updateCounter)

        # adding same twice doesn't modify the counter
        db.add("file", "lastviewed", "label")
        self.assertEquals(1, self._updateCounter)

        # change view name
        db.add("file", "lastviewedNew", "label")
        self.assertEquals(2, self._updateCounter)

        # change label
        db.add("file", "lastviewedNew", "labelNew")
        self.assertEquals(3, self._updateCounter)

        # adding new name
        db.add("newfile", "lastviewedNew", "labelNew")
        self.assertEquals(4, self._updateCounter)

    def testSorting(self):
        db = viewdb.DB()
        db.add("fileA", "A", "labelA")
        db.add("fileC", "C", "labelC")
        db.add("fileB", "B", "labelB")
        l = db.getOrderedLastViewedList()
        self.assertEquals(("labelC","fileC","C"), l[0])
        self.assertEquals(("labelB","fileB","B"), l[1])
        self.assertEquals(("labelA","fileA","A"), l[2])
        
if __name__ == "__main__":
    unittest.main()
