import unittest
import gom_client

# TODO setup and tearDown
# TODO use created node for these integration tests to isolate
# TODO mock real http access

class GomClientTest(unittest.TestCase):
    
    def test_is_attribute(self):
        self.assertTrue(gom_client.is_attribute("/foo:bar"))
        self.assertFalse(gom_client.is_attribute("/foo/bar"))

    def test_attributes_to_xml(self):
        self.assertEqual('<node><attribute name="temperature">50 °C</attribute></node>',
                         gom_client.attributes_to_xml({"temperature":"50 °C"}))
        self.assertEqual('<node />',
                         gom_client.attributes_to_xml({}))

    def test_gom_client_initialize(self):
        self.assertEqual("gom:8020", gom_client.GomClient("http://gom:8020").gom_root.netloc)
    
    # requires gom at 192.168.56.101:3080 for now.
    # Mocking can be done if library get used
    def test_gom_client_operations(self):
        myGom = gom_client.GomClient("http://192.168.56.101:3080")

        # simple retrieve
        result = myGom.retrieve("/")
        self.assertEqual(len(result['node']['entries']), 8)
        
        #update attr
        self.assertEqual(myGom.update("/test/gaga:bar", "hhhhh"),
                         myGom.retrieve("/test/gaga:bar")['attribute']['value'])
        
        # update node
        self.assertEqual(201, myGom.update("/test/tokio", {"hey":"fufu"})['status'])
        
        # create
        myNodePath = myGom.create("/test")
        self.assertEqual(myNodePath, myGom.retrieve(myNodePath)['node']['uri'])
        
        # delete
        self.assertTrue(myGom.delete(myNodePath))
        self.assertEqual(None, myGom.retrieve(myNodePath))
        myGom.delete("/test/tokio")
        myGom.delete("/test/gaga")
