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
ANNOTATIONS_2_FOLDER_PATH = '/home/preyes/Proyectos/Memoria/pablo-reyes-memoria/Codigo/DOCODEX3/Annotations2/'
PARTS = ['part1/','part2/','part3/','part4/','part5/',
         'part6/','part7/','part8/','part9/','part10/',
         'part11/','part12/','part13/','part14/','part15/',
         'part16/','part17/','part18/','part19/','part20/',
         'part21/','part22/','part23/','part24/','part25/',
         'part26/','part27/','part28/','part29/','part30/',
         'part31/','part32/']

TAMANO_SEGMENTOS = 400

#-- --------------------------------------------------------------

def fileList(path, extension):
  return sorted(glob.glob(path+'*.'+extension))
  
#-- --------------------------------------------------------------

if __name__ == "__main__":
	for part in PARTS:
	  file_list = fileList(SOURCES_FOLDER_PATH + part, 'txt')
	  #Procesamos cada archivo de la lista
	  for txt_file in file_list:
	    print txt_file
	    txt_filename = txt_file.split('/')[-1]
	    xml_file = txt_file.replace('.txt','.xml')
	    xml_filename = txt_filename.replace('.txt','.xml')

	    if os.path.exists(xml_file):
	      #if not procesed_file(xml_filename):
	      text = TEXT(txt_file, xml_file)
	      
	      ns = int(text.total_words/TAMANO_SEGMENTOS)+1
	      #ANNOTATIONS 2
	      #Generamos XML
	      feature_tag = '\t<feature name="plagiarism" type="artificial" this_language="en" this_offset="%s" this_length="%s" />\n'
	      xml_annotation = open(ANNOTATIONS_2_FOLDER_PATH + part + xml_filename, 'w')
	      xml_annotation.write('<?xml version="1.0" encoding="UTF-8"?>\n<document reference="%s">\n' %(txt_filename))
	      for i in range(1,ns+1):
	        iw = (i - 1) * TAMANO_SEGMENTOS
	        fw = i * TAMANO_SEGMENTOS - 1 if i*TAMANO_SEGMENTOS - 1 < text.total_words else text.total_words
	        if 1 in text.pv[iw:fw]:
	          #print "Plagio desde %s hasta %s" %(iw, fw)
	          xml_annotation.write(feature_tag %(text.tti[iw-1], text.tti[fw-1] + len(text.tt[fw-1])-1 ))
	      xml_annotation.write('</document>')
	      xml_annotation.close()