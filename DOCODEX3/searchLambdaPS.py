#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob
import os.path
import subprocess

def f1(prec, rec):
  return float(2.0 * ((prec * rec) / (prec + rec)))

#VARIABLES GLOBALES
#ANNOTATIONS_FOLDER_PATH = '/home/preyes/Proyectos/Memoria/pablo-reyes-memoria/Codigo/DOCODEX3/Annotations/'
ANNOTATIONS_FOLDER_PATH = '/home/preyes/Proyectos/Memoria/pablo-reyes-memoria/Codigo/DOCODEX3/Annotations2/'
DETECTIONS_FOLDER_PATH = '/home/preyes/Proyectos/Memoria/pablo-reyes-memoria/Codigo/DOCODEX3/Detections/'
SOURCE_FOLDERS = ['part1/','part2/','part3/','part4/','part5/',
                'part6/','part7/','part8/','part9/','part10/',
                'part11/','part12/','part13/','part14/','part15/',
                'part16/','part17/','part18/','part19/','part20/',
                'part21/','part22/','part23/','part24/','part25/',
                'part26/','part27/','part28/','part29/','part30/',
                'part31/','part32/','poco/','medio/','mucho/']
lmdas = [ 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0,
          1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0,
          2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0 ]

for SOURCE_FOLDER in SOURCE_FOLDERS:
  #DOCODE
  print "DOCODE"
  output = subprocess.check_output("python pan09-plagiarism-detection-performance-measures.py -p %s -d %s" %(ANNOTATIONS_FOLDER_PATH+SOURCE_FOLDER, DETECTIONS_FOLDER_PATH+SOURCE_FOLDER+'DOCODE'), shell=True)
  output = output.split('\n')
  d = [round(float(i), 3) for i in output[7].split('-')]
  d.append(round(f1(d[2],d[1]), 3))

  score_dn, score_dnxs = 0.0, 0.0
  dn, dnxs = [0.0], [0.0]
  for lmda in lmdas:
    print "lambda %s" %(lmda)
    #DOCODE NORMALIZADO
    try:
      output = subprocess.check_output("python pan09-plagiarism-detection-performance-measures.py -p %s -d %s" %(ANNOTATIONS_FOLDER_PATH+SOURCE_FOLDER, DETECTIONS_FOLDER_PATH+SOURCE_FOLDER+"DOCODE_NORMALIZADO/lambda_" + str(int(lmda*10)) ), shell=True)
      output = output.split('\n')
      aux = [round(float(i), 3) for i in output[7].split('-')]
      if aux[0] > dn[0]:
        dn = aux
        dn.append(round(f1(dn[2],dn[1]) ,3))
        dn.append(lmda)
    except:
      print "Error lambda %s" %(lmda)
    #DOCODE NORMALIZADO POR SEGMENTO
    try:
      output = subprocess.check_output("python pan09-plagiarism-detection-performance-measures.py -p %s -d %s" %(ANNOTATIONS_FOLDER_PATH+SOURCE_FOLDER, DETECTIONS_FOLDER_PATH+SOURCE_FOLDER+"DOCODE_NORMALIZADO_SEGMENTO/lambda_" + str(int(lmda*10)) ), shell=True)
      output = output.split('\n')
      aux = [round(float(i), 3) for i in output[7].split('-')]
      if aux[0] > dnxs[0]:
        dnxs = aux
        dnxs.append(round(f1(dnxs[2],dnxs[1]) ,3))
        dnxs.append(lmda)
    except:
      print "Error lambda %s" %(lmda)
  print SOURCE_FOLDER
  print "-----------------------------------"
  print "\tALGORITMO :\tSCORE\tRECALL\tPREC\tGRAN\tF_1\tLMDA"
  print "\tDOCODE    :\t%s\t%s\t%s\t%s\t%s\t----" %(d[0],d[1],d[2],d[3],d[4])
  print "\tDOCODE_N  :\t%s\t%s\t%s\t%s\t%s\t%s" %(dn[0],dn[1],dn[2],dn[3],dn[4],dn[5])
  print "\tDOCODE_NXS:\t%s\t%s\t%s\t%s\t%s\t%s" %(dnxs[0],dnxs[1],dnxs[2],dnxs[3],dnxs[4],dnxs[5])