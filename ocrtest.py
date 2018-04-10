#! /usr/bin/env python3
# -*- coding: utf-8 -*-

### Importamos las librerías
from wand.image import Image as WImg
from PIL import Image as PI
import pyocr
import pyocr.builders
import os
import io
import sys


from wand.image import Image
from PIL import Image as PI
import pyocr
import pyocr.builders
import io
import sys

def show_config():
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("Herramienta OCR o encontrada.")
        sys.exit(1)
    print("* Herramientas OCR disponibles:")
    for tool in tools:
        print('  - %s' % tool)
        langs = tool.get_available_languages()
        print("    - Lenguajes disponibles en %s: %s" % (tool.get_name(), ", ".join(langs)))

#show_config()

tool = pyocr.get_available_tools()[0]
lang = 'spa'

### Cargamos el fichero PDF y convertimos cada una de sus páginas en una imagen JPEG (objeto blob)
image_pdf = Image(filename="jpegfile.pdf", resolution=300)
image_jpeg = image_pdf.convert('jpeg')

### Guardamos todas las imágenes en un array
page_jpeg_list = []
for img in image_jpeg.sequence:
    img_page = Image(image=img)
    page_jpeg_list.append(img_page.make_blob('jpeg'))

### Recorremos el array de imágenes y extraemos el texto de cada una de ellas aplicando OCR
page_text_list = []
for img in page_jpeg_list: 
    text = tool.image_to_string(PI.open(io.BytesIO(img)), lang=lang, builder=pyocr.builders.TextBuilder())
    page_text_list.append(text)
    print('- Página %2s: %5s caracteres' % (len(page_text_list), len(text)))

### Guardamos el texto en un fichero:    
fp = open('textfile.txt', 'w')
fp.write('\n\n'.join(page_text_list))
fp.close()

