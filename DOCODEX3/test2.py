#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob
import os.path
import xmltodict
import numpy as np

from shutil import copyfile
from textClass import TEXT

#VARIABLES GLOBALES
SOURCES_FOLDER_PATH = '/home/preyes/Proyectos/Memoria/pablo-reyes-memoria/Codigo/DOCODEX3/Sources/'
PARTS = ['part1/','part2/','part3/','part4/','part5/',
         'part6/','part7/','part8/','part9/','part10/',
         'part11/','part12/','part13/','part14/','part15/',
         'part16/','part17/','part18/','part19/','part20/',
         'part21/','part22/','part23/','part24/','part25/',
         'part26/','part27/','part28/','part29/','part30/',
         'part31/','part32/']
LMDA_N = 2.3
LMDA_NXS = 2.5

#-- --------------------------------------------------------------

def fileList(path, extension):
  return sorted(glob.glob(path+'*.'+extension))
  
#-- --------------------------------------------------------------
  
if __name__ == "__main__":
  file_n = open("UmbralesN.txt", "w")
  file_nxs = open("UmbralesNXS.txt", "w")
  for part in PARTS:
    file_list = fileList(SOURCES_FOLDER_PATH + part, 'txt')
    #Procesamos cada archivo de la lista
    for txt_file in file_list:
      print txt_file
      txt_filename = txt_file.split('/')[-1]
      xml_file = txt_file.replace('.txt','.xml')
      xml_filename = txt_filename.replace('.txt','.xml')

      if os.path.exists(xml_file):
        text = TEXT(txt_file, xml_file)

        docode_n = text.docode_normalizado(400)
        std_n = np.std(docode_n['differences'])
        file_n.write("%s\n" %(round(std_n*LMDA_N,3)))
        docode_nxs = text.docode_normalizado_segmento(400)        
        std_nxs = np.std(docode_nxs['differences'])
        file_nxs.write("%s\n"%(round(std_nxs*LMDA_NXS,3)))
  file_n.close()
  file_nxs.close()
        