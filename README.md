#Python Gom RestFs Client


##Requirements


* Python 3.2


##Usage

### Setup and initialization

```python
import restfs
REST_FS = restfs.RestFs(<Gom-URI>)
```

Where the gom-uri is of format `"http://<ip/name>:<port>"`.

All further operations are then performed via the initialized object (in this example `REST_FS`)

###RESTful operations

Assuming gom is at `"http://192.168.56.101:3080"`

* GET/retrieve

  * Attribute retrieval:

    ```python
    >>> import restfs
    >>> from pprint import pprint
    >>> REST_FS = restfs.RestFs("http://192.168.56.101:3080")
    >>> myAttribute = REST_FS.retrieve("/test:myAttr")
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

  * Attribute retrieval:

    ```python
    >>> import restfs
    >>> from pprint import pprint
    >>> REST_FS = restfs.RestFs("http://192.168.56.101:3080")
    >>> myNode = REST_FS.retrieve("/areas")
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

* PUT/update
* DELETE/delete
  Tbd
* CREATE/create
  Tbd

TODO
---

* Support script runner (maybe)
* Support gom observer creation (probably)
