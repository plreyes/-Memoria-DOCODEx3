#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob
import os.path
import subprocess

def f1(prec, rec):
	return float(2.0 * ((prec * rec) / (prec + rec)))

#VARIABLES GLOBALES
ANNOTATIONS_FOLDER_PATH = '/home/preyes/Proyectos/Memoria/pablo-reyes-memoria/Codigo/DOCODEX3/Annotations2/'
DETECTIONS_FOLDER_PATH = '/home/preyes/Proyectos/Memoria/pablo-reyes-memoria/Codigo/DOCODEX3/Detections/'
#SOURCE_FOLDERS = ['part1/','part2/','part3/','part4/','part5/',
#                  'part6/','part7/','part8/','part9/','part10/',
#                  'part11/','part12/','part13/','part14/','part15/',
#                  'part16/','part17/','part18/','part19/','part20/',
#                  'part21/','part22/','part23/','part24/','part25/',
#                  'part26/','part27/','part28/','part29/','part30/',
#                  'part31/','part32/']
SOURCE_FOLDERS = ['poco/','medio/','mucho/']

LMDA_DN = 2.3     #DOCODE Normalizado
LMDA_DNXS = 2.5   #DOCODE Normalizado por Segmento

for SOURCE_FOLDER in SOURCE_FOLDERS:
	#DOCODE
	print "DOCODE"
	output = subprocess.check_output("python pan09-plagiarism-detection-performance-measures.py -p %s -d %s" %(ANNOTATIONS_FOLDER_PATH+SOURCE_FOLDER, DETECTIONS_FOLDER_PATH+SOURCE_FOLDER+'DOCODE'), shell=True)
	output = output.split('\n')
	d = [round(float(i), 3) for i in output[7].split('-')]
	d.append(round(f1(d[2],d[1]), 3))

	score_dn, score_dnxs = 0.0, 0.0
	dn, dnxs = [0.0, 0.0, 0.0, 0.0, -1.0], [0.0, 0.0, 0.0, 0.0, -1.0]
	#DOCODE NORMALIZADO
	LMDA_DN = 2.3
	try:
		output = subprocess.check_output("python pan09-plagiarism-detection-performance-measures.py -p %s -d %s" %(ANNOTATIONS_FOLDER_PATH+SOURCE_FOLDER, DETECTIONS_FOLDER_PATH+SOURCE_FOLDER+"DOCODE_NORMALIZADO/lambda_" + str(int(LMDA_DN*10)) ), shell=True)
		output = output.split('\n')
		aux = [round(float(i), 3) for i in output[7].split('-')]
		f1_dn = round(f1(aux[2],aux[1]) ,3)
		if f1_dn > dn[4]:
			dn = aux
			dn.append(f1_dn)
			dn.append(LMDA_DN)
	except:
		print "Error lambda %s" %(lmda)
	#DOCODE NORMALIZADO POR SEGMENTO
	LMDA_DNXS = 2.5
	try:
		output = subprocess.check_output("python pan09-plagiarism-detection-performance-measures.py -p %s -d %s" %(ANNOTATIONS_FOLDER_PATH+SOURCE_FOLDER, DETECTIONS_FOLDER_PATH+SOURCE_FOLDER+"DOCODE_NORMALIZADO_SEGMENTO/lambda_" + str(int(LMDA_DNXS*10)) ), shell=True)
		output = output.split('\n')
		aux = [round(float(i), 3) for i in output[7].split('-')]
		f1_dnxs = round(f1(aux[2],aux[1]) ,3)
		if f1_dnxs > dnxs[4]:
			dnxs = aux
			dnxs.append(f1_dnxs)
			dnxs.append(LMDA_DNXS)
	except:
		print "Error lambda %s" %(LMDA_DNXS)
	print SOURCE_FOLDER
	print "-----------------------------------"
	print "\tALGORITMO :\tSCORE\tRECALL\tPREC\tGRAN\tF_1\tLMDA"
	print "\tDOCODE    :\t%s\t%s\t%s\t%s\t%s\t----" %(d[0],d[1],d[2],d[3],d[4])
	print "\tDOCODE_N  :\t%s\t%s\t%s\t%s\t%s\t%s" %(dn[0],dn[1],dn[2],dn[3],dn[4],dn[5])
	print "\tDOCODE_NXS:\t%s\t%s\t%s\t%s\t%s\t%s" %(dnxs[0],dnxs[1],dnxs[2],dnxs[3],dnxs[4],dnxs[5])
