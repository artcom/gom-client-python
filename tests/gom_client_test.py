import unittest
import gom_client

class GomClientTest(unittest.TestCase):
    
    def test_is_attribute(self):
        self.assertTrue(gom_client.is_attribute("/foo:bar"))
        self.assertFalse(gom_client.is_attribute("/foo/bar"))
