'''
Created on May 13, 2016

@author: Shauryadeep Chaudhuri
'''
import json


class JsonLoader(object):
    '''
    classdocs
    '''

    def __call__(self, json_text):
        return self._byteify(
            json.loads(json_text, object_hook=self._byteify),
            ignore_dicts=True
        )

    def _checkType(self, typeString):
        if type(typeString) not in [dict, list, tuple]:
            typeDict = {str(typ): typ for typ in [str, int, long, float, bool]}
            if typeString in typeDict:
                typeString = typeDict[typeString]

        return typeString

    def _byteify(self, data, ignore_dicts=False):
        data = self._checkType(data)
        # if this is a unicode string, return its string representation
        if isinstance(data, unicode):
            return data.encode('utf-8')
        # if this is a list of values, return list of byteified values
        if isinstance(data, list):
            return [self._byteify(item, ignore_dicts=True) for item in data]
        # if this is a dictionary, return dictionary of byteified keys and values
        # but only if we haven't already byteified it
        if isinstance(data, dict) and not ignore_dicts:
            return {
                self._byteify(key, ignore_dicts=True): self._byteify(value, ignore_dicts=True)
                for key, value in data.iteritems()
            }
        # if it's anything else, return it in its original form
        return data
