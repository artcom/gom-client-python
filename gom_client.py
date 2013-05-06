import http.client
import urllib.parse
import json
import logging
import xml.etree.ElementTree as ET

logging.basicConfig(level=logging.WARN,
                    format='%(asctime)s - %(levelname)s -  %(message)s')

def addDefaultHeaders(theRequest):
    for key,value in DEFAULT_HEADER.items():
        theRequest.add_header(key, value)
    return True

def is_attribute(thePath):
    return (thePath.count(":") > 0)

def attributes_to_xml(theDict):
    node = ET.Element('node')
    for key, value in theDict.items():
        attr = ET.SubElement(node, "attribute")
        attr.attrib['name'] = key
        attr.text = value
    return ET.tostring(node, encoding="unicode")

# Custom exceptions
class RestFsBaseError(Exception):
    pass

class RestFsNotImplementedError(RestFsBaseError):
    def __str__(self):
        return "Not yet implemented!"

class RestFsResponseError(RestFsBaseError):
    def __init__(self, response):
        self.response = response
    
    def __str__(self):
        return str(self.response.status) + "-" + self.response.reason# + "(" + repr(response) + ")"

class GomClient(object):
    
    def __init__(self, theGomRoot):
        logging.info("RestFs.__init__ with gom_root: '{gom_root}'".format(gom_root=theGomRoot))
        self.gom_root = urllib.parse.urlparse(theGomRoot)
    
    def _perform_request(self, thePath, theMethod, theHeaders, thePayload= None):
        conn = http.client.HTTPConnection(self.gom_root.netloc)
        conn.request(theMethod, thePath, thePayload, theHeaders)
        response = conn.getresponse()
        raw_payload = response.read().decode('utf-8')
        conn.close()
        return (response, raw_payload)
    
    # TODO add redirection support (with limit of course)
    def retrieve(self, thePath):
        logging.info("RestFs.retrieve with path: '{path}'".format(path=thePath))
        response, raw_payload = self._perform_request(thePath, "GET", {
            "Accept": "application/json",
            "Content-Type": "application/json"
        })
        if (response.status == 500):
            raise RestFsResponseError(response)
        elif (response.status == 200):
            return json.loads(raw_payload)
        elif (response.status == 404):
            return None
        else:
            if (response):
                raise RestFsResponseError(response)
        
    def update(self, thePath, theValue):
        logging.info("RestFs.update with path: '{path}' and value '{value}'".format(path=thePath, value=repr(theValue)))
        if (is_attribute(thePath)):
            logging.info("    * attribute")
            if (theValue == None):
                raise RestFsBaseError("update attribute call must include value")
            if (type(theValue) != str):
                raise RestFsBaseError("update attribute value must be a string")
            response, raw_payload = self._perform_request(thePath, "PUT", {
                    "Accept": "text/plain",
                    "Content-Type": "application/x-www-form-urlencoded"
                 },
                 urllib.parse.urlencode({'attribute': theValue,
                                         "type": "string"}))
            if (response.status == 500):
                raise RestFsResponseError(response)
            return raw_payload
        else:
            logging.info("    * node")
            if (type(theValue) != dict):
                raise RestFsBaseError("update attribute value must be a dict")
            response, raw_payload = self._perform_request(thePath, "PUT", {
                    "Accept": "application/json",
                    "Content-Type": "application/"
                },
                 attributes_to_xml(theValue))
            if (response.status == 500):
                raise RestFsResponseError(response)
            return json.loads(raw_payload)
    
    def create(self, thePath, theAttributes={}):
        logging.info("RestFs.create with path: '{path}' and attributes '{attributes}'".format(path=thePath, attributes=repr(theAttributes)))
        
        response, raw_payload = self._perform_request(thePath, "POST", {
                "Content-Type": "application/xml"
            },
            attributes_to_xml(theAttributes))
        if (response.status == 500):
            raise RestFsResponseError(response)
        return response.getheader('Location')
    
    def delete(self, thePath):
        # TODO Safeguard the Path a little?
        conn = http.client.HTTPConnection(self.gom_root.netloc)
        conn.request("DELETE",
                     thePath)
        response = conn.getresponse()
        conn.close()
        
        if (response.status == 500):
            raise RestFsResponseError(response)
        elif (response.status == 404):
            return None
        return True
        
    def register_observer(self):
        raise RestFsNotImplementedError
        
    def run_script(self):
        raise RestFsNotImplementedError
       