from PdbxReader import PdbxReader
from PdbxWriter import PdbxWriter


class Reader(PdbxReader):
    def __init__(self):
        # define 3-level objects:
        # top level: "l_block" for list of data blocks each in a PdbxContainer
        # 2nd level: "block" for current data block in a PdbxContainer
        # 3rd level: "cat" for current data category in a DataCategory
        self.l_block = []  # must set as empty list, not None
        self.block_index = None
        self.block = None
        self.cat = None

    def parse(self, filepath):
        with open(filepath) as file:
            super(Reader, self).__init__(file)
            self.read(self.l_block)

    def printBlocks(self):
        for i in range(len(self.l_block)):
            blockname = self.l_block[i].getName()
            print("index %s: name %s" % (i, blockname))

    def selectBlock(self, selector, selector_type="index"):
        if selector_type == "index":
            self.block_index = selector
        elif selector_type == "name":
            for i in range(len(self.l_block)):
                blockname = self.l_block[i].getName()
                if blockname == selector:
                    self.block_index = i
                    break
        else:
            self.block_index = None
        self.block = self.l_block[self.block_index]
        # self.l_block[self.block_index] = self.block

    def selectCat(self, cat_name):
        self.cat = self.block.getObj(cat_name)
        # self.block.replace(self.cat)
        # self.l_block[self.block_index] = self.block


# class Block(DataContainer):
#     def __init__(self, container):
#         super(Block, self).__init__(name=container.getName())
#         for cat_name in container.getObjNameList():
#             obj = container.getObj(cat_name)
#             self.append(obj)

#     def printBlock(self):
#         print("Block name: %s" % self.getName())
#         print("List of data categories:")
#         for cat_name in self.getObjNameList():
#             print(cat_name)

#     def insert(self, obj, index=0):
#         """ Insert the input object to the current object catalog before index.
#         An existing object of the same name will be overwritten.
#         """
#         if obj.getName() is not None:
#             if obj.getName() not in self.getObjNameList():
#                 # self.__objNameList is keeping track of object order here --
#                 self.__objNameList.insert(obj.getName(), index)
#             self.__objCatalog[obj.getName()] = obj


# class Cat(DataCategory):
#     def __init__(self, cat):
#         super(Cat, self).__init__(name=cat.getName(),
#                                   attributeNameList=cat.getAttributeList(),
#                                   rowList=cat.getRowList())

#     def printCat(self):
#         print("Category name: %s" % self.getName())
#         print("List of attributes:")
#         for attr in self.getAttributeList():
#             print(attr)
#         print("Number of rows: %s" % self.getRowCount())
#         for i in range(min(10, self.getRowCount())):
#             row = self.data[i]
#             print(row)


class Writer(PdbxWriter):
    def __init__(self, filepath):
        self.file = open(filepath, 'w')
        super(Writer, self).__init__(ofh=self.file)

    def close(self):
        self.file.close()


class CopyCat:
    def __init__(self):
        self.filepath_from = None
        self.block_index_from = None
        self.cat_name = None
        self.filepath_to = None
        self.l_block_index_to = None
        self.filepath_combined = None

    def setFrom(self, filepath, cat_name, block_index=0):
        self.filepath_from = filepath
        self.block_index_from = block_index
        self.cat_name = cat_name

    def setTo(self, filepath, l_block_index=[0]):
        self.filepath_to = filepath
        self.l_block_index_to = l_block_index

    def copyCat(self, filepath, tf_replace=True):
        self.filepath_combined = filepath
        reader_from = Reader()
        reader_from.parse(self.filepath_from)
        reader_from.selectBlock(self.block_index_from)
        reader_from.selectCat(self.cat_name)

        reader_to = Reader()
        reader_to.parse(self.filepath_to)
        for i in self.l_block_index_to:
            reader_to.selectBlock(i)
            reader_to.block.insert(reader_from.cat)

        writer = Writer(self.filepath_combined)
        writer.write(reader_to.l_block)
        writer.close()


def testReport(filepath, block_index, cat_name):
    reader = Reader()
    reader.parse(filepath)
    reader.printBlocks()
    reader.selectBlock(0)
    reader.block.printBlock()
    reader.selectCat("database_PDB_rev")
    reader.cat.printCat()


def main():
    filepath = "test.cif"
    block_index = 0
    cat_name = "database_PDB_rev"
    testReport(filepath, block_index, cat_name)

    filepath_from = "test2.cif"
    filepath_to = "test.cif"
    cat_name = "audit_author"
    filepath_combined = "test_copy.cif"
    copycat = CopyCat()
    copycat.setFrom(filepath_from, cat_name)
    copycat.setTo(filepath_to, [0, 1])
    copycat.copyCat(filepath_combined)

    # print(dc0.getObjNameList())
    # cat1 = dc0.getObj('database_2')
    # print(cat1.getAttributeList())
    # print(cat1.getRowCount())
    # print(cat1.getItemNameList())
    # print(cat1.getRowList())
    # print(cat1.getValue("database_id",0))
    # print(cat1.data)
    # print(cat1.getValue("database_id"))
    # print(cat1.getRowItemDict(0))


if __name__ == '__main__':
    main()
