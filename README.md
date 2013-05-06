#Python Gom Client

##Requirements

* Python 3.2

##Usage

### Setup and initialization

```python
import gom_client
GOM = gom_client.GomClient(<Gom-URI>)
```

Where the gom-uri is of format `"http://<ip/name>:<port>"`.

All further operations are then performed via the initialized object (in this example `GOM`)

###RESTful operations

Assuming gom is at `"http://192.168.56.101:3080"`

* GET/retrieve

  * Attribute retrieval:

    ```python
    >>> import gom_client
    >>> from pprint import pprint
    >>> GOM = gom_client.GomClient("http://192.168.56.101:3080")
    >>> myAttribute = GOM.retrieve("/test:myAttr")
    >>> pprint(myAttribute)
    {'attribute': {'ctime': '2012-10-12T08:46:48+02:00',
               'mtime': '2012-10-12T08:46:48+02:00',
               'name': 'myAttr',
               'node': '/test',
               'type': 'string',
               'value': 'test'}}
    >>> print(myAttribute['attribute']['value']
    test
    ```

  * Node retrieval:

    ```python
    >>> import gom_client
    >>> from pprint import pprint
    >>> GOM = gom_client.GomClient("http://192.168.56.101:3080")
    >>> myNode = GOM.retrieve("/areas")
    >>> pprint(myNode)
    {'node': {'ctime': '2012-09-20T04:51:56+02:00',
          'entries': [{'ctime': '2012-07-30T16:13:02+02:00',
                       'mtime': '2012-07-30T16:13:02+02:00',
                       'node': '/areas/home'},
                      {'ctime': '2012-09-29T17:51:47+02:00',
                       'mtime': '2012-09-29T17:51:47+02:00',
                       'node': '/areas/life'},
                      {'ctime': '2012-06-26T21:13:35+02:00',
                       'mtime': '2012-06-26T21:13:35+02:00',
                       'node': '/areas/mobile'},
                      {'ctime': '2012-10-10T18:30:50+02:00',
                       'mtime': '2012-10-10T18:30:50+02:00',
                       'node': '/areas/move'},
                      {'ctime': '2012-09-20T02:19:30+02:00',
                       'mtime': '2012-09-20T02:19:30+02:00',
                       'node': '/areas/pre-show'},
                      {'ctime': '2012-07-30T14:03:57+02:00',
                       'mtime': '2012-07-30T14:03:57+02:00',
                       'node': '/areas/welcome'},
                      {'attribute': {'ctime': '2012-10-11T07:02:18+02:00',
                                     'mtime': '2012-10-11T07:02:18+02:00',
                                     'name': 'operational_mode',
                                     'node': '/areas',
                                     'type': 'string',
                                     'value': 'idle'}}],
          'mtime': '2012-09-20T04:51:56+02:00',
          'uri': '/areas'}}
    >>> pprint(list(map(lambda x: x['node'], filter(lambda x: "node" in x, myNode['node']['entries']))))
    ['/areas/home',
     '/areas/life',
     '/areas/mobile',
     '/areas/move',
     '/areas/pre-show',
     '/areas/welcome']
    ```

  * Retrieval of non-existent Node/Attribute:

    ```python
    >>> import gom_client
    >>> from pprint import pprint
    >>> GOM = gom_client.GomClient("http://192.168.56.101:3080")
    >>> pprint(GOM.retrieve("/test/does-not-exist"))
    None
    >>> pprint(GOM.retrieve("/test:does-not-exist"))
    None
    ```

* PUT/update

  * Attribute update

    ```python
    >>> import gom_client
    >>> GOM = gom_client.GomClient("http://192.168.56.101:3080")
    >>> GOM.update("/test:temperature", "50 °C")
    '50 °C'
    ```
   
  * Node update

    ```python
    >>> import gom_client
    >>> GOM = gom_client.GomClient("http://192.168.56.101:3080")
    >>> GOM.update("/test/weather", {"temperature": "50 °C", "wind_velocity": "3 km/h", "wind_direction": "NNW"})
    {'status': 201}
    ```

* DELETE/delete

  * Delete existing node
  
    ```python
    >>> import gom_client
    >>> GOM = gom_client.GomClient("http://192.168.56.101:3080")
    >>> GOM.delete("/test/c18bf546-e577-414a-92d2-2ebdfb69b4f6")
    True
    ```

  * Delete non-existing node
  
    ```python
    >>> import gom_client
    >>> GOM = gom_client.GomClient("http://192.168.56.101:3080")
    >>> print(GOM.delete("/test/does-not-exist"))
    None
    ```
  
Attributes are deleted accordingly

* POST/create
  
  * Create empty node
  
   ```python
   >>> import gom_client
   >>> GOM = gom_client.GomClient("http://192.168.56.101:3080")
   >>> GOM.create("/test")
   '/test/c18bf546-e577-414a-92d2-2ebdfb69b4f6'
   ```
  
  * Create node with attributes
  
    ```python
    >>> import gom_client
    >>> from pprint import pprint
    >>> GOM = gom_client.GomClient("http://192.168.56.101:3080")
    >>> GOM.create("/test", {"name":"Hans", "profession": "Lumberjack"})
    '/test/419e9db0-2800-43ed-9053-edaafd4f60b3'
    >>> pprint(GOM.retrieve("/test/419e9db0-2800-43ed-9053-edaafd4f60b3"))
    {'node': {'ctime': '2012-10-12T10:43:25+02:00',
              'entries': [{'attribute': {'ctime': '2012-10-12T10:43:25+02:00',
                                         'mtime': '2012-10-12T10:43:25+02:00',
                                         'name': 'name',
                                         'node': '/test/419e9db0-2800-43ed-9053-edaafd4f60b3',
                                         'type': 'string',
                                         'value': 'Hans'}},
                          {'attribute': {'ctime': '2012-10-12T10:43:25+02:00',
                                         'mtime': '2012-10-12T10:43:25+02:00',
                                         'name': 'profession',
                                         'node': '/test/419e9db0-2800-43ed-9053-edaafd4f60b3',
                                         'type': 'string',
                                         'value': 'Lumberjack'}}],
              'mtime': '2012-10-12T10:43:25+02:00',
              'uri': '/test/419e9db0-2800-43ed-9053-edaafd4f60b3'}}
    ```

##Packaging

The module gom_client can be moved around freely in your project and has no further dependencies.

If required though a package can be built and installed system wide by executing

```bash
easy_install-3.2 .
```

in the checkout directory. `easy_install-3.2`'s specific name can vary depending your system setup.

##TODO

* Support script runner (maybe)
* Support gom observer creation (probably)
