#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# """
# Created on Thu Nov 11 16:00:15 2021
# Class to read any Xray log fille
# @author: chenghua shao
# """


# class LogXray:
#     """Class to read Log file based on process
#     """

#     def __init__(self):
#         self.process = ""
#         self.program = ""

#     def setProcess(self, process):
#         l_process = ["indexing_integration",
#                      "scaling",
#                      "phasing",
#                      "refinement"]
#         if process.lower() in l_process:
#             self.process = process.lower()

#     def setProgram(self, program):
#         d_program = {}
#         d_program["scaling"] = ["scalepack",
#                                 "hkl-2000",
#                                 "scala",
#                                 "xia2"]
#         if program.lower() in d_program[self.process]:
#             self.program = program.lower()

#     def readLog(self, filepath):
#         """
#         Read log file into list of lines

#         Parameters
#         ----------
#         filepath : str
#             Filepath of the log

#         Returns
#         -------
#         None.

#         self.l_file #list of each line in a file

#         """
#         try:
#             with open(filepath) as file:
#                 self.l_file = file.read().splitlines() #read file into a list
#         except IOError as msg:
#             print(msg)

#     def readTemplate(self, filepath_template):
#         """
#         Read template to create empty class dict

#         Parameters
#         ----------
#         filepath_template : str
#             local filename of the template

#         Returns
#         -------
#         None.

#         Outcomes
#         -------
#         self.d_[cat][item] #1st level dict of the cat, 2nd level dict of items

#         """
#         try:
#             file = open(filepath_template)
#         except IOError as msg:
#             print(msg)
#         else:
#             for line in file:
#                 item = line.strip().split()[0]
#                 if item.startswith('_'): #read cif item
#                     try:
#                         [cat, attr] = item.split('.') #split cat and item
#                         if cat not in self.d_:
#                             self.d_[cat] = {}
#                             self.d_[cat][item] = []
#                         else:
#                             self.d_[cat][item] = []
#                     except IndexError as msg:
#                         print(msg)
#         finally:
#             file.close()


# def main():
#     log = LogXray()
#     log.setProcess("scaling")
#     log.setProgram("scalepack")
#     print(log.process)
#     print(log.program)

# if __name__ == "__main__":
#     main()
