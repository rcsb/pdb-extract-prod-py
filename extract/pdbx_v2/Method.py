##
# File:      Method.py
# Orignal:   Aug 12, 2013   Jdw
# 
# Updates:
#
##
"""
Utility classes for applying dictionary methods on PDBx/mmCIF data files.
"""

__docformat__ = "restructuredtext en"
__author__    = "John Westbrook"
__email__     = "jwest@rcsb.rutgers.edu"
__license__   = "Creative Commons Attribution 3.0 Unported"
__version__   = "V0.01"

import sys
#from pdbx_v2.reader.PdbxReader      import PdbxReader
#from pdbx_v2.writer.PdbxWriter      import PdbxWriter
#from pdbx_v2.reader.PdbxContainers    import *
#from pdbx_v2.reader.DataCategory      import DataCategory
#from pdbx_v2.dictionary.DictionaryApi import DictionaryApi

class MethodDefinition(object):
    def __init__(self,method_id,code='calculate',language='Python',inline=None):
        self.method_id=method_id
        self.language=language
        self.code=code
        self.inline=inline

    def getId(self):
        return self.method_id
    def getLanguage(self):
        return self.language
    def getInline(self):
        return self.inline
    
    def printIt(self,fh=sys.stdout):
        fh.write("------------- Method definition -------------\n")
        fh.write("Id:           %s\n" % self.method_id)
        fh.write("Code:         %s\n" % self.code)        
        fh.write("Language:     %s\n" % str(self.language))
        fh.write("Inline text:  %s\n" % str(self.inline))        


class MethodReference(object):
    def __init__(self,method_id,type='attribute',category=None,attribute=None):
        self.method_id=method_id
        self.type=type
        self.categoryName=category
        self.attributeName=attribute

    def getId(self):
        return self.method_id
    def getType(self):
        return self.type
    def getCategoryName(self):
        return self.categoryName
    def getAttributeName(self):
        return self.attributeName

    def printIt(self,fh=sys.stdout):
        fh.write("--------------- Method Reference -----------------\n")
        fh.write("Id:             %s\n" % self.method_id)
        fh.write("Type:           %s\n" % self.type)
        fh.write("Category name:  %s\n" % str(self.categoryName))
        fh.write("Attribute name: %s\n" % str(self.attributeName))
