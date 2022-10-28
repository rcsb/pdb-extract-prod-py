##
#
# File:     DataCategoryFormatted.py
# Original: 02-Feb-2009   jdw
#
# Update:
#   14-Nov-2012   jdw refactoring
#   17-Nov-2012   jdw self._rowList becomes data -
#   17-Dec-2012   jdw add quoting preference as constructor option.
##
"""

A subclass of DataCategory including additional formatting methods.

"""

__docformat__ = "restructuredtext en"
__author__    = "John Westbrook"
__email__     = "jwest@rcsb.rutgers.edu"
__license__   = "Creative Commons Attribution 3.0 Unported"
__version__   = "V0.01"

import re,sys,traceback
from extract.pdbx_v2.DataCategory  import DataCategory

class DataCategoryFormatted(DataCategory):
    """  A subclass of DataCategory including additional formatting methods.
    """
#    def __init__(self,name,attributeNameList=None,rowList=None):
#        super(DataCategory,self).__init__(name,attributeNameList,rowList)
    def __init__(self,dataCategoryObj,preferDoubleQuotes=True):
        self.__dcObj=dataCategoryObj
        super(DataCategory,self).__init__(self.__dcObj._name,self.__dcObj._attributeNameList,self.__dcObj.data)        
        #
        self.__lfh = sys.stdout
        
        self._currentRowIndex=0
        self._currentAttribute=None
        #
        self.__avoidEmbeddedQuoting=False
        self.__preferDoubleQuotes=preferDoubleQuotes
        #
        # --------------------------------------------------------------------
        # any whitespace 
        self.__wsRe=re.compile(r"\s")
        #self.__wsAndQuotesRe=re.compile(r"[\s'\"]")
        self.__wsAndQuotesRe=re.compile(r"[\s'\"#]")        
        # any newline or carriage control
        self.__nlRe=re.compile(r"[\n\r]")
        #
        # single quote 
        self.__sqRe=re.compile(r"[']")
        #
        self.__sqWsRe=re.compile(r"('\s)|(\s')")
        
        # double quote 
        self.__dqRe=re.compile(r'["]')
        self.__dqWsRe=re.compile(r'("\s)|(\s")')
        #
        self.__intRe=re.compile(r'^[0-9]+$')
        self.__floatRe=re.compile(r'^-?(([0-9]+)[.]?|([0-9]*[.][0-9]+))([(][0-9]+[)])?([eE][+-]?[0-9]+)?$')
        #
        self.__dataTypeList=['DT_NULL_VALUE','DT_INTEGER','DT_FLOAT','DT_UNQUOTED_STRING','DT_ITEM_NAME',
                             'DT_DOUBLE_QUOTED_STRING','DT_SINGLE_QUOTED_STRING','DT_MULTI_LINE_STRING']
        self.__formatTypeList=['FT_NULL_VALUE','FT_NUMBER','FT_NUMBER','FT_UNQUOTED_STRING',
                               'FT_QUOTED_STRING','FT_QUOTED_STRING','FT_QUOTED_STRING','FT_MULTI_LINE_STRING']
        #


    def __formatPdbx(self, inp):
        """ Format input data following PDBx quoting rules - 
        """
        try:
            if (inp is None):
                return ("?",'DT_NULL_VALUE')

            # pure numerical values are returned as unquoted strings
            if (isinstance(inp,int) or self.__intRe.search(str(inp))):
                return ( [str(inp)],'DT_INTEGER')

            if (isinstance(inp,float) or self.__floatRe.search(str(inp))):
                return ([str(inp)],'DT_FLOAT')

            # null value handling -

            if (inp == "." or inp == "?"):
                return ([inp],'DT_NULL_VALUE')

            if (inp == ""):
                return (["."],'DT_NULL_VALUE')

            # Contains white space or quotes ?
            if not self.__wsAndQuotesRe.search(inp):
                #if inp.startswith("_"):
                if inp[0] in ['_']:
                    return (self.__doubleQuotedList(inp),'DT_ITEM_NAME')
                elif inp[0] in ['[',']','$','#',';']:
                    return (self.__doubleQuotedList(inp),'DT_DOUBLE_QUOTED_STRING')
                elif inp[:5] in ['data_','loop_','save_']:
                    return (self.__doubleQuotedList(inp),'DT_DOUBLE_QUOTED_STRING')
                else:
                    return ([str(inp)],'DT_UNQUOTED_STRING')
            else:
                if self.__nlRe.search(inp):
                    return (self.__semiColonQuotedList(inp),'DT_MULTI_LINE_STRING')
                else:
                    if (self.__preferDoubleQuotes):
                        if (self.__avoidEmbeddedQuoting):                    
                            # change priority to choose double quoting where possible.
                            if not self.__dqRe.search(inp) and not self.__sqWsRe.search(inp):
                                return (self.__doubleQuotedList(inp),'DT_DOUBLE_QUOTED_STRING')                                        
                            elif not self.__sqRe.search(inp) and not self.__dqWsRe.search(inp):
                                return (self.__singleQuotedList(inp),'DT_SINGLE_QUOTED_STRING')                                        
                            else:
                                return (self.__semiColonQuotedList(inp),'DT_MULTI_LINE_STRING')
                        else:
                            # change priority to choose double quoting where possible.
                            if not self.__dqRe.search(inp):
                                return (self.__doubleQuotedList(inp),'DT_DOUBLE_QUOTED_STRING')                                        
                            elif not self.__sqRe.search(inp):
                                return (self.__singleQuotedList(inp),'DT_SINGLE_QUOTED_STRING')                                        
                            else:
                                return (self.__semiColonQuotedList(inp),'DT_MULTI_LINE_STRING')
                    else:
                        if (self.__avoidEmbeddedQuoting):                    
                            # change priority to choose double quoting where possible.
                            if not self.__sqRe.search(inp) and not self.__dqWsRe.search(inp):
                                return (self.__singleQuotedList(inp),'DT_SINGLE_QUOTED_STRING')
                            elif not self.__dqRe.search(inp) and not self.__sqWsRe.search(inp):
                                return (self.__doubleQuotedList(inp),'DT_DOUBLE_QUOTED_STRING')
                            else:
                                return (self.__semiColonQuotedList(inp),'DT_MULTI_LINE_STRING')
                        else:
                            # change priority to choose double quoting where possible.
                            if not self.__sqRe.search(inp):
                                return (self.__singleQuotedList(inp),'DT_SINGLE_QUOTED_STRING')
                            elif not self.__dqRe.search(inp):
                                return (self.__doubleQuotedList(inp),'DT_DOUBLE_QUOTED_STRING')
                            else:
                                return (self.__semiColonQuotedList(inp),'DT_MULTI_LINE_STRING')
        except:
            traceback.print_exc(file=self.__lfh)                            

    def __dataTypePdbx(self, inp):
        """ Detect the PDBx data type - 
        """
        if (inp is None):
            return ('DT_NULL_VALUE')
        
        # pure numerical values are returned as unquoted strings
        if isinstance(inp,int) or self.__intRe.search(str(inp)):
            return ('DT_INTEGER')

        if isinstance(inp,float) or self.__floatRe.search(str(inp)):
            return ('DT_FLOAT')

        # null value handling -

        if (inp == "." or inp == "?"):
            return ('DT_NULL_VALUE')

        if (inp == ""):
            return ('DT_NULL_VALUE')

        # Contains white space or quotes ?
        if not self.__wsAndQuotesRe.search(inp):
            if inp.startswith("_"):
                return ('DT_ITEM_NAME')
            else:
                return ('DT_UNQUOTED_STRING')
        else:
            if self.__nlRe.search(inp):
                return ('DT_MULTI_LINE_STRING')
            else:
                if (self.__avoidEmbeddedQuoting):
                    if not self.__sqRe.search(inp) and not self.__dqWsRe.search(inp):
                        return ('DT_DOUBLE_QUOTED_STRING')                                        
                    elif not self.__dqRe.search(inp) and not self.__sqWsRe.search(inp):
                        return ('DT_SINGLE_QUOTED_STRING')                                        
                    else:
                        return ('DT_MULTI_LINE_STRING')
                else:
                    if not self.__sqRe.search(inp):
                        return ('DT_DOUBLE_QUOTED_STRING')                                        
                    elif not self.__dqRe.search(inp):
                        return ('DT_SINGLE_QUOTED_STRING')                                        
                    else:
                        return ('DT_MULTI_LINE_STRING')                    

    def __singleQuotedList(self,inp):
        l=[]
        l.append("'")
        l.append(inp)
        l.append("'")        
        return(l)

    def __doubleQuotedList(self,inp):
        l=[]
        l.append('"')
        l.append(inp)
        l.append('"')        
        return(l)
    
    def __semiColonQuotedList(self,inp):
        l=[]
        l.append("\n")            
        if inp[-1] == '\n':
            l.append(";")
            l.append(inp)
            l.append(";")
            l.append("\n")                        
        else:
            l.append(";")
            l.append(inp)
            l.append("\n")                        
            l.append(";")
            l.append("\n")                                    

        return(l)

    def getValueFormatted(self,attributeName=None,rowIndex=None):
        if attributeName is None:
            attribute=self._currentAttribute
        else:
            attribute=attributeName

        if rowIndex is None:
            rowI = self._currentRowIndex
        else:
            rowI = rowIndex
            
        if isinstance(attribute, str) and isinstance(rowI,int):
            try:
                list,type=self.__formatPdbx(self.data[rowI][self._attributeNameList.index(attribute)])
                return "".join(list)
            except (IndexError):
                self.__lfh.write("attributeName %s rowI %r rowdata %r\n" % (attributeName,rowI,self.data[rowI]))
                raise IndexError        
        raise TypeError(attribute)
        

    def getValueFormattedByIndex(self,attributeIndex,rowIndex):
        try:
            list,type=self.__formatPdbx(self.data[rowIndex][attributeIndex])
            return "".join(list)
        except (IndexError):
            raise IndexError        

    def getAttributeValueMaxLengthList(self,steps=1):
        mList=[0 for i in range(len(self._attributeNameList))]
        for row in self.data[::steps]:
            for indx in range(len(self._attributeNameList)):
                val=row[indx]                
                mList[indx] = max(mList[indx],len(str(val)))
        return mList

    def getFormatTypeList(self,steps=1):
        try:
            curDataTypeList=['DT_NULL_VALUE' for i in range(len(self._attributeNameList))]
            for row in self.data[::steps]:
                for indx in range(len(self._attributeNameList)):
                    val=row[indx]
                    # print "index ",indx," val ",val
                    dType=self.__dataTypePdbx(val)
                    dIndx=self.__dataTypeList.index(dType)
                    # print "d type", dType, " d type index ",dIndx
                
                    cType=curDataTypeList[indx]
                    cIndx=self.__dataTypeList.index(cType)           
                    cIndx= max(cIndx,dIndx)
                    curDataTypeList[indx]=self.__dataTypeList[cIndx]

            # Map the format types to the data types
            curFormatTypeList=[]
            for dt in curDataTypeList:
                ii=self.__dataTypeList.index(dt)
                curFormatTypeList.append(self.__formatTypeList[ii])
        except:
            self.__lfh.write("PdbxDataCategory(getFormatTypeList) ++Index error at index %d in row %r\n" % (indx,row))

        return curFormatTypeList,curDataTypeList

    def getFormatTypeListX(self):
        curDataTypeList=['DT_NULL_VALUE' for i in range(len(self._attributeNameList))]
        for row in self.data:
            for indx in range(len(self._attributeNameList)):
                val=row[indx]
                #print "index ",indx," val ",val
                dType=self.__dataTypePdbx(val)
                dIndx=self.__dataTypeList.index(dType)
                #print "d type", dType, " d type index ",dIndx
                
                cType=curDataTypeList[indx]
                cIndx=self.__dataTypeList.index(cType)           
                cIndx= max(cIndx,dIndx)
                curDataTypeList[indx]=self.__dataTypeList[cIndx]

        # Map the format types to the data types
        curFormatTypeList=[]
        for dt in curDataTypeList:
            ii=self.__dataTypeList.index(dt)
            curFormatTypeList.append(self.__formatTypeList[ii])
        return curFormatTypeList,curDataTypeList
    

