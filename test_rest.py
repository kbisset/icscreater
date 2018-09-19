#!/usr/bin/env python

import sys, os, re, shutil, json, urllib, urllib2, BaseHTTPServer

class MethodRequest(urllib2.Request):
    'See: https://gist.github.com/logic/2715756'
    def __init__(self, *args, **kwargs):
        if 'method' in kwargs:
            self._method = kwargs['method']
            del kwargs['method']
        else:
            self._method = None
        return urllib2.Request.__init__(self, *args, **kwargs)

    def get_method(self, *args, **kwargs):
        return self._method if self._method is not None else urllib2.Request.get_method(self, *args, **kwargs)

def rest_call_json(url, payload=None, with_payload_method='PUT'):
    'REST call with JSON decoding of the response and JSON payloads'
    if payload:
        if not isinstance(payload, basestring):
            payload = json.dumps(payload)
        # PUT or POST
        response = urllib2.urlopen(MethodRequest(url, payload, {'Content-Type': 'application/json'}, method=with_payload_method))
    else:
        # GET
        response = urllib2.urlopen(url)
    response = response.read().decode()
    return json.loads(response)

def main(argv):
    url = 'http://localhost:8080/record/1'
    data = {
        'name': 'Bob Smith',
        'age': 35,
        'pets': ['fido', 'fluffy']
    }
    result = rest_call_json(url, data, 'PUT')
    print 'Result ', result

if __name__ == '__main__':
    main(sys.argv[1:])
