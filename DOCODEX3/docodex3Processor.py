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
ANNOTATIONS_FOLDER_PATH = '/home/preyes/Proyectos/Memoria/pablo-reyes-memoria/Codigo/DOCODEX3/Annotations/'
DETECTIONS_FOLDER_PATH = '/home/preyes/Proyectos/Memoria/pablo-reyes-memoria/Codigo/DOCODEX3/Detections/'
SOURCE_FOLDER = 'part1/'

#-- --------------------------------------------------------------

def fileList(path, extension):
  return sorted(glob.glob(path+'*.'+extension))

#-- --------------------------------------------------------------

def procesed_file(xml_filename):
  if os.path.exists(DETECTIONS_FOLDER_PATH + SOURCE_FOLDER + "DOCODE_NORMALIZADO_SEGMENTO/lambda_30/" + xml_filename):
    return True
  return False
  
#-- --------------------------------------------------------------

if __name__ == "__main__":
  file_list = fileList(SOURCES_FOLDER_PATH + SOURCE_FOLDER, 'txt')
  #Procesamos cada archivo de la lista
  for txt_file in file_list:
    print txt_file
    txt_filename = txt_file.split('/')[-1]
    xml_file = txt_file.replace('.txt','.xml')
    xml_filename = txt_filename.replace('.txt','.xml')

    if os.path.exists(xml_file):
      if not procesed_file(xml_filename):
        text = TEXT(txt_file, xml_file)
        print "Palabras: %s" %(text.total_words)

        #DOCODE
        docode = text.docode(400)
        print "Segmentos: %s" %(len(docode['segments']))
        #Generamos XML Resultados
        feature_tag = '\t<feature name="detected-plagiarism" type="artificial" obfuscation="high" obfuscator_version="2009" this_language="en" this_offset="%s" this_length="%s" />\n'
        xml_docode = open(DETECTIONS_FOLDER_PATH + SOURCE_FOLDER + "DOCODE/" + xml_filename, 'w')
        xml_docode.write('<?xml version="1.0" encoding="UTF-8"?>\n<document reference="%s">\n' %(txt_filename))
        threshold = docode['style'] - 0.075
        for segment in docode['segments']:
          if segment['s_style'] < threshold:
            xml_docode.write(feature_tag %(text.tti[segment['initial_word']-1], text.tti[segment['final_word']-1] + len(text.tt[segment['final_word']-1])-1 ))
        xml_docode.write('</document>')
        xml_docode.close()
        #DOCODE NORMALIZADO y NORMALIZADO POR SEGMENTO
        lmdas = [ 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0,
                  1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0,
                  2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0 ]
        
        docode_n = text.docode_normalizado(400)
        docode_nxs = text.docode_normalizado_segmento(400)
        
        std_n = np.std(docode_n['differences'])
        std_nxs = np.std(docode_nxs['differences'])
        
        for lmda in lmdas:
          #Generamos XML Resultados - Normalizado
          xml_docode_n = open(DETECTIONS_FOLDER_PATH + SOURCE_FOLDER + "DOCODE_NORMALIZADO/lambda_" + str(int(lmda*10)) + "/" + xml_filename, 'w')
          xml_docode_n.write('<?xml version="1.0" encoding="UTF-8"?>\n<document reference="%s">\n' %(txt_filename))
          threshold = docode_n['style'] + lmda * std_n
          for segment in docode_n['segments']:
            if segment['s_style'] > threshold:
              xml_docode_n.write(feature_tag %(text.tti[segment['initial_word']-1], text.tti[segment['final_word']-1] + len(text.tt[segment['final_word']-1])-1 ))
          xml_docode_n.write('</document>')
          xml_docode_n.close()

          #Generamos XML Resultados - Normalizado por Segmento
          xml_docode_nxs = open(DETECTIONS_FOLDER_PATH + SOURCE_FOLDER + "DOCODE_NORMALIZADO_SEGMENTO/lambda_" + str(int(lmda*10)) + "/" + xml_filename, 'w')
          xml_docode_nxs.write('<?xml version="1.0" encoding="UTF-8"?>\n<document reference="%s">\n' %(txt_filename))
          threshold = docode_nxs['style'] + lmda * std_nxs
          for segment in docode_nxs['segments']:
            if segment['s_style'] > threshold:
              xml_docode_nxs.write(feature_tag %(text.tti[segment['initial_word']-1], text.tti[segment['final_word']-1] + len(text.tt[segment['final_word']-1])-1 ))
          xml_docode_nxs.write('</document>')
          xml_docode_nxs.close()
        print "-------------------------------------------------------------------------------"
    copyfile(xml_file, ANNOTATIONS_FOLDER_PATH + SOURCE_FOLDER + xml_filename)