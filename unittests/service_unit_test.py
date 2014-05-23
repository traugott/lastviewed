'''
Created on 23.05.2014

@author: blicrain
'''

import unittest
import viewdb
import service_impl

class ServiceTestCase(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        viewdb.db.clear()
        service_impl.clear()
        self._time = 1;
        service_impl.setTimeGetter(lambda: self._time)
        
    def testUpdateDatabase(self):
        service_impl.doService(lambda : ("1", "2"))
        label, filename, lastviewed = viewdb.db.getOrderedLastViewedList()[0]
        self.assertEquals("1", filename)
        self.assertEquals("2", label)
        self.assertTrue(lastviewed > 0)

        self._time = self._time + 1
        service_impl.doService(lambda : ("1", "2"))
        _, _, lastviewed2 = viewdb.db.getOrderedLastViewedList()[0]
        self.assertEquals(lastviewed, lastviewed2)
        

    def testStartAndStop(self):
        service_impl.doService(lambda : ("1", "2"))
        label, filename, lastviewed = viewdb.db.getOrderedLastViewedList()[0]
        self.assertEquals("1", filename)
        self.assertEquals("2", label)
        self.assertTrue(lastviewed > 0)

        service_impl.doService(lambda : None)

        self._time = self._time + 1
        service_impl.doService(lambda : ("1", "2"))
        _, _, lastviewed2 = viewdb.db.getOrderedLastViewedList()[0]
        self.assertTrue(lastviewed < lastviewed2)
        
    def testEntryInDb(self):
        service_impl.doService(lambda : ("filename1", "label1"))
        self._time = self._time + 1
        service_impl.doService(lambda : ("filename2", "label2"))
        self._time = self._time + 1
        service_impl.doService(lambda : ("filename3", "label3"))
        elements = viewdb.db.getOrderedLastViewedList()
        self.assertEqual(("label3","filename3"), elements[0][0:2])
        self.assertEqual(("label2","filename2"), elements[1][0:2])
        self.assertEqual(("label1","filename1"), elements[2 ][0:2])

                
        