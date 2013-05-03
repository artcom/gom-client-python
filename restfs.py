import http.client
import urllib.parse
import json
import logging
import xml.etree.ElementTree as ET

logging.basicConfig(level=logging.WARN,
                    format='%(asctime)s - %(levelname)s -  %(message)s')

DEFAULT_HEADER = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

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

# Actual RestFsClass
class RestFs(object):
    
    def __init__(self, theGomRoot):
        logging.info("RestFs.__init__ with gom_root: '{gom_root}'".format(gom_root=theGomRoot))
        self.gom_root = urllib.parse.urlparse(theGomRoot)
    
    # TODO add redirection support (with limit of course)
    def retrieve(self, thePath):
        logging.info("RestFs.retrieve with path: '{path}'".format(path=thePath))
        conn = http.client.HTTPConnection(self.gom_root.netloc)
        conn.request("GET", thePath, headers=DEFAULT_HEADER)
        response = conn.getresponse()
        raw_payload = response.read().decode('utf-8')
        conn.close()
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
            conn = http.client.HTTPConnection(self.gom_root.netloc)
            conn.request("PUT",
                         thePath,
                         urllib.parse.urlencode({'attribute': theValue,
                                                 "type": "string"}),
                         headers = {
                             "Accept": "text/plain",
                             "Content-Type": "application/x-www-form-urlencoded"
                         })
            response = conn.getresponse()
            payload = response.read().decode('utf-8')
            conn.close()
            return payload
        else:
            logging.info("    * node")
            if (type(theValue) != dict):
                raise RestFsBaseError("update attribute value must be a dict")
            conn = http.client.HTTPConnection(self.gom_root.netloc)
            conn.request("PUT",
                         thePath,
                         attributes_to_xml(theValue),
                         headers = {
                             "Accept": "application/json",
                             "Content-Type": "application/xml"
                         })
            response = conn.getresponse()
            if (response.status == 500):
                raise RestFsResponseError(response)
            raw_payload = response.read().decode('utf-8')
            conn.close()
            return json.loads(raw_payload)
    
    def create(self, thePath, theAttributes={}):
        logging.info("RestFs.create with path: '{path}' and attributes '{attributes}'".format(path=thePath, attributes=repr(theAttributes)))
        conn = http.client.HTTPConnection(self.gom_root.netloc)
        conn.request("POST",
                     thePath,
                     attributes_to_xml(theAttributes),
                     headers = {
                          "Content-Type": "application/xml"
                     })
        response = conn.getresponse()
        if (response.status == 500):
            raise RestFsResponseError(response)
        return response.getheader('Location')
    
    def delete(self, thePath):
        # TODO Safeguard the Path a little?
        conn = http.client.HTTPConnection(self.gom_root.netloc)
        conn.request("DELETE",
                     thePath)
        response = conn.getresponse()
        
        if (response.status == 500):
            raise RestFsResponseError(response)
        elif (response.status == 404):
            return None
        return True
        
    def register_observer(self):
        raise RestFsNotImplementedError
        
    def run_script(self):
        raise RestFsNotImplementedError

        