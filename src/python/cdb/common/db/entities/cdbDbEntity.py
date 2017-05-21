#!/usr/bin/env python

"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.
"""


import copy
import types
from cdb.common.exceptions.dbError import DbError
from cdb.common.utility.loggingManager import LoggingManager

class CdbDbEntity(object):
    """ Base Cdb DB entity class. """
    columns = []
    mappedColumnDict = {}
    removeKeyList = [ '_sa_instance_state', 'logger' ]
    cdbObjectClass = None

    def __init__(self, **kwargs):
        self.logger = LoggingManager.getInstance().getLogger(self.__class__.__name__)
        for col, value in list(kwargs.items()):
            if col not in self.columns:
                raise DbError('Column %s not found in table %s' % (col, self.__class__.__name__))
            else:
                setattr(self, col, value)

    def getLogger(self):
        return self.logger

    def mapColumn(self, dbName, objectName):
        if dbName in self.__dict__:
            self.__dict__[objectName] = self.__dict__.get(dbName)

    def mapColumns(self):
        for (dbName, objectName) in list(self.mappedColumnDict.items()):
            self.mapColumn(dbName, objectName)
    
    def toCdbObject(self):
        scrubbedDict = copy.copy(self.__dict__)
        for (dbName, objectName) in list(self.mappedColumnDict.items()):
            if dbName in scrubbedDict:
                scrubbedDict[objectName] = scrubbedDict.get(dbName)
                del scrubbedDict[dbName]
        for key in self.removeKeyList:
            if key in scrubbedDict:
                del scrubbedDict[key]
        for (key,value) in list(scrubbedDict.items()):
            if isinstance(value, CdbDbEntity):
                scrubbedDict[key] = value.toCdbObject()
            elif type(value) == list:
                scrubbedList = []
                for item in value:
                    if isinstance(item, CdbDbEntity):
                        scrubbedList.append(item.toCdbObject())
                    else:
                        scrubbedList.append(item)
                scrubbedDict[key] = scrubbedList

        if self.cdbObjectClass is not None:
            return self.cdbObjectClass(scrubbedDict)
        else:
            return scrubbedDict
         
    def __repr__(self):
        s = '%s(' % self.__class__.__name__
        addComma = False
        for col in self.columns:
            colName = col.__str__().split('.')[-1]
            if not addComma:
                addComma = True
            else:
                s += ','
            exec('value = self.%s' % colName)
            if value is not None:
                s += '%s=%s' % (colName, value)
            s += ')'
        return s

    def loadRelationships(self):
        """ Load all relations object knows about. """
        pass

    def getCdbObject(self):
        """ Convert the raw database object into a CDB object. """
        return self.toCdbObject()

