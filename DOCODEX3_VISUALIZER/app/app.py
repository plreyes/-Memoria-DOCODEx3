#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

from collections import Counter
from textClass import TEXT
from time import time

import numpy as np
import xmltodict
import nltk
import glob
import re

app = Flask(__name__)
cors = CORS(app)

SOURCES_FOLDER_PATH = '/home/preyes/Proyectos/Memoria/pablo-reyes-memoria/Codigo/Ipython_DocodeX3/textos/'

#-- ----------------------------------------------------------------

@app.route('/')
def index():
  files = get_files()
  return render_template("layout.html", files = files)

#-- ----------------------------------------------------------------

@app.route('/docodex3', methods = ['POST'])
def docodex3():
  form =  request.form
  txt_file = form.get('docode-file', 'default.txt')
  xml_file = txt_file.replace('.txt', '.xml')
  algorithm = int(form.get('docode-algorithm', 1))
  m = int(form.get('docode-m', 400))
  
  #Get files
  files = get_files()

  #Preprocesamos texto
  text = TEXT(txt_file, xml_file)
  #Ejecutamos algoritmo solicitado
  if algorithm == 1:
    docode = text.docode(m)
    threshold = docode["style"] - 0.075
  elif algorithm == 2:
    docode = text.docode_normalizado(m)
    threshold = docode["style"] + 2.3 * np.std(docode["differences"])
  elif algorithm == 3:
    docode = text.docode_normalizado_segmento(m)
    threshold = docode["style"] + 2.5 * np.std(docode["differences"])
  else:
    docode = text.docode(m)
    threshold = 0.0


  return render_template("docodex3.html", files = files, current_file = txt_file,\
                                          algorithm = algorithm, m = m,  text = text,\
                                          docode = docode, threshold = threshold)

#-- ----------------------------------------------------------------

def fileList(path, extension):
  return glob.glob(path+'*.'+extension)

def get_files():
  return fileList(SOURCES_FOLDER_PATH, 'txt')

#-- ----------------------------------------------------------------

if __name__ == '__main__':
  app.run(debug = True, port = 5000, threaded=True)