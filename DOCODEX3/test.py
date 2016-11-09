#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob
import os.path
import xmltodict
import numpy as np
import subprocess
import pyexcel
from pyexcel_xls import save_data
from collections import OrderedDict

from shutil import copyfile
from textClass import TEXT

#VARIABLES GLOBALES
ANNOTATIONS_FOLDER_PATH = '/home/preyes/Proyectos/Memoria/pablo-reyes-memoria/Codigo/DOCODEX3/Annotations/'
DETECTIONS_FOLDER_PATH = '/home/preyes/Proyectos/Memoria/pablo-reyes-memoria/Codigo/DOCODEX3/Detections/'

A_FOLDER_PATH = '/home/preyes/Proyectos/Memoria/pablo-reyes-memoria/Codigo/DOCODEX3/test/A/'
D_FOLDER_PATH = '/home/preyes/Proyectos/Memoria/pablo-reyes-memoria/Codigo/DOCODEX3/test/D/'

PARTS = ['part1/','part2/','part3/','part4/','part5/',
         'part6/','part7/','part8/','part9/','part10/',
         'part11/','part12/','part13/','part14/','part15/',
         'part16/','part17/','part18/','part19/','part20/',
         'part21/','part22/','part23/','part24/','part25/',
         'part26/','part27/','part28/','part29/','part30/',
         'part31/','part32/']

LMDA_DN = 2.3
LMDA_DNXS = 2.5

#-- --------------------------------------------------------------

def f1(prec, rec):
  return round(float(2.0 * ((prec * rec) / (prec + rec))), 3) if prec + rec > 0.0 else 0.0

#-- --------------------------------------------------------------

def fileList(path, extension):
  return sorted(glob.glob(path+'*.'+extension))
  
#-- --------------------------------------------------------------

if __name__ == "__main__":
  xls_filename = 'Results/score.xls'
  xls_data = OrderedDict()
  xls_data.update({ "DOCODEX3 SCORE": [['File', 'DOCODE', 'NORMALIZADO', 'X SEGMENTO']] })
  save_data(xls_filename, xls_data)
  for part in PARTS:
    file_list = fileList(ANNOTATIONS_FOLDER_PATH + part, 'xml')
    #Procesamos cada archivo de la lista
    for xml_file in file_list:
      print xml_file
      xml_filename = xml_file.split('/')[-1]
      copyfile(xml_file, A_FOLDER_PATH + "file.xml")
      try:
        #DOCODE
        copyfile(DETECTIONS_FOLDER_PATH+part+'DOCODE/'+xml_filename, D_FOLDER_PATH + "file.xml")
        output = subprocess.check_output("python pan09-plagiarism-detection-performance-measures.py -p %s -d %s" %(A_FOLDER_PATH, D_FOLDER_PATH), shell=True)
        output = output.split('\n')
        d = [round(float(i), 3) for i in output[7].split('-')]
        d.append(f1(d[2],d[1]))
        #DOCODE NORMALIZADO
        copyfile(DETECTIONS_FOLDER_PATH+part+'DOCODE_NORMALIZADO/lambda_' + str(int(LMDA_DN*10)) + '/' + xml_filename, D_FOLDER_PATH + "file.xml")
        output = subprocess.check_output("python pan09-plagiarism-detection-performance-measures.py -p %s -d %s" %(A_FOLDER_PATH, D_FOLDER_PATH), shell=True)
        output = output.split('\n')
        dn = [round(float(i), 3) for i in output[7].split('-')]
        dn.append(f1(d[2],d[1]))
        #DOCODE NORMALIZADO X SEGMENTO
        copyfile(DETECTIONS_FOLDER_PATH+part+'DOCODE_NORMALIZADO_SEGMENTO/lambda_' + str(int(LMDA_DNXS*10)) + '/' + xml_filename, D_FOLDER_PATH + "file.xml")
        output = subprocess.check_output("python pan09-plagiarism-detection-performance-measures.py -p %s -d %s" %(A_FOLDER_PATH, D_FOLDER_PATH), shell=True)
        output = output.split('\n')
        dnxs = [round(float(i), 3) for i in output[7].split('-')]
        dnxs.append(f1(d[2],d[1]))

        sheet = pyexcel.get_sheet(file_name=xls_filename)
        sheet.row += [xml_file, d[0], dn[0], dnxs[0]]
        sheet.save_as(xls_filename)
      except:
        print "error"