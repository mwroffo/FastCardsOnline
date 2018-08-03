"""
Test suite for FastCardsOnline.
mwroffo 2018-08-01
"""
import unittest
import os
import tempfile

from app import app

class BasicTestCase(unittest.TestCase):
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200,
                        msg="status code should be 200")

    def test_database(self):
        tester = os.path.exists("/Users/_mexus/Documents/code/FastCardsOnline/mwroffo.db")
        self.assertTrue(tester, "db connection should exist")

class FastCardsTestCase(unittest.TestCase):
    def testSecretKeyExists(self):
        pass

if __name__ == '__main__':
    unittest.main()
