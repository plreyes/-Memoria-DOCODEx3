# Memoria-DOCODEx3

Este repositorio contiene los algoritmos desarrollados en el marco del trabajo de memoria realizado para optar al título de Ingeniero Civil en Informática de la Universidad Técnica Federico Santa María.

## Corpus Prueba

El corpus de prueba utilizado en los experimentos realizados es **PAN Plagiarism Corpus 2010**, puesto a dispoción por la competencia PAN el año 2010-2011. El corpus consta de 2 carpetas principales: _source-documents_ compuesta sólo de documetos originales  y _suspicious-documents_ compuesto de documentos con plagio artificial.

En este proyecto se utilizó sólo la carpeta _suspicious-documents_ del corpus, debido a que se trabaja en la modalidad de detección intrínseca de plagio.

El corpus se encuentra disponible online y  puede ser descargado desde el siguiente link:
    
    http://www.uni-weimar.de/en/media/chairs/webis/corpora/corpus-pan-pc-10/
 


## DOCODEX3

* **Source**

    Directorio que contiene las carpetas y archivos del grupo _suspicious-documents_ del corpus PAN 2010

* **Annotations**

    Directorio donde se almacena una copia de los archivos XML originales que indican los segmentos plagiados de los documentos del grupo _suspicious-documents} del corpus PAN 2010, agrupado en carpetas _part1, part2, ..., part32_  tal como se presenta en el corpus y además agrupados por nivel de plagio en las carpetas _poco, medio, mucho_.

* **Annotations2**

    Directorio donde se almacena los archivos XML modificados que indican los segmentos plagiados de los documentos del grupo _suspicious-documents_ del corpus PAN 2010, agrupado en carpetas _part1/, part2/, ..., part32/_  tal como se presenta en el corpus y además agrupados por nivel de plagio en las carpetas _poco/, medio/, mucho/_.

* **Detections**

    Directorio donde se almacena los archivos XML con el detalle de las detecciones de plagio realizadas.

* **Results**

    Directorio que contiene los archivos TXT con los resultados de los experimentos realizados.

* **createDirectories**

    Script que crea todos los directorios y subdirectorios necesarios y requeridos por los otros scripts desarrollados. Se debe especificar la ruta raíz del directorio donde se encuentra **DOCODEX3**.

* **generateAnnotations2**

    Script que crea archivos XML modificados  a partir de los archivos XML originales del corpus PAN 2010, pero indicando segmentos plagiados según tamaño de segmentos definido por el usuario.

* **clasificador**

    Script que clasifica los archivos XML originales y modificados del grupo  _suspicious-documents} del corpus PAN 2010 según nivel de plagio.

* **docodex3Processor**

    Script que procesa los documentos de texto de la sub-carpeta del directorio **Sources/** indicada por el usuario utilizando los algoritmos _DOCODE_, _DOCODE Normalizado_ y _DOCODE Normalizado por Segmento_ para distintos valores de lambda en el rango $[0.1 - 3.0]$, generando XML de detecciones y guardando dichos XML en el directorio **Detections/**.

* **searchLambdaF1**

    Script que determina el valor de $\lambda_{F_{1}\,optimo}$ que obtiene mejor $F_1$ a partir de las detecciones registradas en los archivos XML del directorio **Detections** y los XML originales o modificados que indican donde existía el plagio realmente (**Annotations/** o **Annotations2/** según indique el usuario). Entrega las métricas _Puntaje Total_, _Recall_, _Precision_, $F_1$ y $\lambda_{F_{1}\,optimo}$ para los algoritmos _DOCODE_, _DOCODE Normalizado_ y _DOCODE Normalizado por Segmento_.

* **searchLambdaPS**

    Script que determina el valor de $\lambda_{PT\,optimo}$ que obtiene mejor _Puntaje Total_ a partir de las detecciones registradas en los archivos XML del directorio **Detections/** y los XML originales o modificados que indican donde existía el plagio realmente (**Annotations/** o **Annotations2/* según indique el usuario). Entrega las métricas _Puntaje Total_, _Recall_, _Precision_, $F_1$ y $\lambda_{PT\,optimo}$ para los algoritmos _DOCODE_, _DOCODE Normalizado_ y _DOCODE Normalizado por Segmento_.

* **resultsBestLambdaF1**

    Script que entrega las métricas _Puntaje Total_, _Recall_, _Precision_, $F_1$ y $\lambda_{F_{1}\,optimo}$ para los algoritmos _DOCODE_, _DOCODE Normalizado_ y _DOCODE Normalizado por Segmento_ utilizando los valores de $\lambda_{F_{1}\,optimo}$ indicados por el usuario.

* **resultsBestLambdaPS**

    Script que entrega las métricas _Puntaje Total_, _Recall_, _Precision_, $F_1$ y $\lambda_{PT\,optimo}$ para los algoritmos _DOCODE_, _DOCODE Normalizado_ y _DOCODE Normalizado por Segmento_ utilizando los valores de $\lambda_{PT\,optimo}$ indicados por el usuario.

* **textClass**

    Clase que realiza el preprocesamiento al texto a analizar y contiene los métodos _docode_, _docode\_normalizado_ y _docode\_normalizado\_segmento_.
    
Es posible replicar los experimentos simplemente ejecutando cada uno de los scripts descritos en el orden en que aparecen en el listado.

## DOCODEX3 Visualizer

Aplicación Flask desarrollada para visualizar el procesamiento de los algoritmos _DOCODE_, _DOCODE Normalizado_ y DOCODE Normalizado por Segmento_.

Los textos a ser procesador deben ser guardados en el directorio _textos/_ junto al archivo XML del mismo nombre que indica los segmentos plagiados siguiendo el formato de los archivos XML presentes el el corpus de prueba **PAN Plagiarism Corpus 2010**

