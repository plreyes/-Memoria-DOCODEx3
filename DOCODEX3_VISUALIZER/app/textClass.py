#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import xmltodict
import numpy as np

from collections import Counter

class TEXT:
  r = re.compile(r"[^a-z]", re.IGNORECASE)

  def __init__(self, txt_path, xml_path):
    self.tt, self.tti, self.pv = [], [], []

    self.txt_path = txt_path
    self.xml_path = xml_path

    with open(self.xml_path,'r') as f:
      self.xml_file = f.read()
    self.xml_dict = xmltodict.parse(self.xml_file)
    
    with open(self.txt_path,'r') as f:
      self.text = f.read()
    self.lower_text = self.text.lower()
    self.re_text = self.r.sub(' ', self.lower_text)
    self.split_text = self.re_text.split(' ')

    i = 0
    for f in self.xml_dict['document']['feature'] :
      if f['@name'] == 'plagiarism':
        #No Plagio
        e = int(f['@this_offset'])
        self.preprocess_segment(self.r.sub(' ', self.lower_text[i:e]), self.tt, self.tti, self.pv, 0, i)
        #Plagio
        i = int(f['@this_offset']) + 1
        e = i + int(f['@this_length'])
        self.preprocess_segment(self.r.sub(' ',self.lower_text[i:e]), self.tt, self.tti, self.pv, 1, i)
        i = e + 1
    self.preprocess_segment(self.r.sub(' ',self.text[i:len(self.lower_text)]), self.tt, self.tti, self.pv, 0, i)
    #Expresamos texto como un conjunto de numeros.
    self.vocabulary = list(set(self.tt))
    self.vocabulary_dict = {value: key for key, value in enumerate(self.vocabulary)}
    self.ptt = [self.vocabulary_dict[w] for w in self.tt]

    self.total_words = len(self.ptt)
    self.frequency = Counter(self.ptt)
    self.frequency_vector = self.frequency.values()
    self.normalized_frequency_vector = [float(x)/self.total_words for x in self.frequency_vector]

  def preprocess_segment(self, segment, tt, tti, pv, plagio_state, index):
    aux_tt = []
    aux_tti = []
    st = segment.split(' ')
    for w in st:
      if w != '':
        aux_tt.append(w)
        aux_tti.append(index)
        index += len(w)+1 #+1 asume el corrimiento necesario para considerar el espacio eliminado por el split()
      else:
        index += 1
    pv += [plagio_state]*len(aux_tt)
    tt += aux_tt
    tti += aux_tti

  def segment_style(self, fulltext_vector, segment_vector, sl):
  	d = [np.abs(float(fulltext_vector[j] - segment_vector[j]))/np.abs(float(fulltext_vector[j] + segment_vector[j]))/sl for j in range(0, len(segment_vector)) ]
  	return sum(d), d

  def docode(self, m):
    style = 0.0
    segments = []
    differences = []
    ns = int(len(self.ptt)/m)+1
    
    for i in range(1,ns+1):
      #Obtenemos el segmento de texto c
      iw = (i-1)*m
      fw = i*m - 1 if i*m - 1 < self.total_words else self.total_words
      s  = self.ptt[iw:fw]
      s_frecuency = Counter(s)
      sv_keys = s_frecuency.keys()
      #Obtenemos las frecuencias de las palabras del segmento en el vector del texto completo
      s_ftv = [self.frequency_vector[j] for j in sv_keys ]
      
      #Algoritmo 1 - DOCODE NORMAL
      sv_values = [float(x) for x in s_frecuency.values()]
      #calculamos diferencias
      s_style, d = self.segment_style(s_ftv, sv_values, len(s))
      style += s_style
      differences.append(s_style)
      segments.append({"id": i, "initial_word": iw, "final_word": fw, "sv_keys": sv_keys, "sv_values": sv_values, "s_style": s_style, "s_ftv": s_ftv, "differences": d, "plagio": False})
    style = style/float(ns)
    return {'style': style, 'segments': segments, 'differences': differences}


  def docode_normalizado(self, m):
    style = 0.0
    segments = []
    differences = []
    ns = int(len(self.ptt)/m)+1
    
    for i in range(1,ns+1):
      #Obtenemos el segmento de texto c
      iw = (i-1)*m
      fw = i*m if i*m < self.total_words else self.total_words
      s  = self.ptt[iw:fw]
      s_frecuency = Counter(s)
      sv_keys = s_frecuency.keys()
      #Obtenemos las frecuencias de las palabras del segmento en el vector del texto completo
      s_ftv = [self.frequency_vector[j] for j in sv_keys ]

      N = float(len(s))
      sv_values = [float(x)/N for x in s_frecuency.values()]
      #calculamos diferencias
      s_style, d = self.segment_style(s_ftv, sv_values, len(s))
      style += s_style
      differences.append(s_style)
      segments.append({"id": i, "initial_word": iw, "final_word": fw, "sv_keys": sv_keys, "sv_values": sv_values, "s_style": s_style, "s_ftv": s_ftv, "differences": d, "plagio": False})
    style = style/float(ns)
    return {'style': style, 'segments': segments, 'differences': differences}


  def docode_normalizado_segmento(self, m):
    style = 0.0
    segments = []
    differences = []
    ns = int(len(self.ptt)/m)+1
    
    for i in range(1,ns+1):
      #Obtenemos el segmento de texto c
      iw = (i-1)*m
      fw = i*m if i*m < self.total_words else self.total_words
      s  = self.ptt[iw:fw]
      s_frecuency = Counter(s)
      sv_keys = s_frecuency.keys()
      #Obtenemos las frecuencias de las palabras del segmento en el vector del texto completo
      s_ftv = [self.frequency_vector[j] for j in sv_keys ]

      Ns = float(len(s))
      sv_values = [float(x)/Ns for x in s_frecuency.values()]
      #Normalizamos el vector generado anteriormente
      Nsftv = float(sum(s_ftv))
      ns_ftv = [float(x)/Nsftv for x in s_ftv ]
      #calculamos diferencias
      s_style, d = self.segment_style(ns_ftv, sv_values, len(s))
      style += s_style
      differences.append(s_style)
      segments.append({"id": i, "initial_word": iw, "final_word": fw, "sv_keys": sv_keys, "sv_values": sv_values, "s_style": s_style, "s_ftv": ns_ftv, "differences": d, "plagio": False})
    style = style/float(ns)
    return {'style': style, 'segments': segments, 'differences': differences}