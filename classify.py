import pyexiv2
import requests
import json
import sys
import time
import threading
import math
from os import walk


# Classifica a imagem por tags enviando pelo tagbox e recebendo as tags
def classify_file(filename, file):
    response = requests.post('http://localhost:8080/tagbox/check', files={'file': (filename, file)})
    try:
        body = json.loads(response.content)
    except:
        print(filename)
        raise "ata"
    print(body["tags"])
    return body['success'], body['tags']

# Modifica o exif das imagens para incluir as tags
def modify_tags(filename, tags):
    with open(filename, 'rb+') as file:
        with pyexiv2.ImageData(file.read()) as img:
            metadata = img.read_xmp()
            img.modify_xmp({'Xmp.dc.subject': tags})
            file.seek(0)
            file.write(img.get_bytes())

def get_tags(file):
    with pyexiv2.ImageData(file.read()) as img:
        return img.read_xmp()['Xmp.dc.subject']

# Le arquivo e manda para classificação
def classify_and_modify(filename):
    with open(filename, 'rb+') as file:
        res, tags = classify_file(filename, file)
        cleaned_tags = [tag['tag'] for tag in tags]
        if len(cleaned_tags) > 2:
            cleaned_tags = cleaned_tags[0:2]
        if not res:
            return
        modify_tags(filename, cleaned_tags)

print("\n[ Tagger 0.1 ]\n")

dir_path = input("Digite o path onde estão as imagens: ")

# Le todos os arquivos da pasta que eu especifiquei
files = []
for (dirpath, dirnames, filenames) in walk(dir_path):
    files.extend(filenames)
    break

errored = []

if len(files) == 0:
    print("Pasta não encontrada!")
else:
    print("Foram encontrados", len(files), "arquivos na pasta\n")
    start_time = time.time()
    actual = 0 
    total = len(files)
    for filename in files:        
        actual += 1
        print("[" + str(actual) + " / " + str(total) + "] " + filename)
        
        if not filename.endswith(".jpg") and not filename.endswith(".jpeg"):
            continue

        classify_and_modify(dir_path + "\\" + filename)
        try:    
            classify_and_modify(dir_path + "\\" + filename)
        except:
            errored.append(filename)


