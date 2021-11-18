
import pandas as pd
import json
import os


global coleccion



coleccion = {}

def saveIndex(rutaIndice,coleccion,ruta):
    if os.path.exists(rutaIndice):
        createIndex(rutaIndice,coleccion,ruta)

    else:
        os.makedirs(rutaIndice)
        createIndex(rutaIndice,coleccion,ruta)

def createIndex(rutaIndice,coleccion,ruta):
    with open(rutaIndice+'/'+ruta+'.json', 'w') as c:
            json.dump(coleccion, c)
    

def getTerms(docTerms, index):
    terms = docTerms.split(' ')
    for term in terms:
        obj = term.split('/')
        coleccion[index]['POSTINGS'].append(obj)



    return 

def read_info(training,test,folder):
    csv = pd.read_csv(training, index_col=0)
    index = 0
    for doc in csv.index:
        
        items = doc.split('\t')
        coleccion[index] = dict({'DOCID':items[0],'CLASE':items[1], 'NTERMINOS':items[2], 'POSTINGS':[]})
    
        getTerms(items[3],index)
        index+=1

    saveIndex(folder, coleccion,'training')

    csv = pd.read_csv(test, index_col=0)
    for doc in csv.index:
        
        items = doc.split('\t')
        coleccion[index] = dict({'DOCID':items[0],'CLASE':items[1], 'NTERMINOS':items[2], 'POSTINGS':[]})
    
        getTerms(items[3],index)
        index+=1

    saveIndex(folder, coleccion,'test')
    return 

def start():
    archivoTraining = input('Ingrese la ruta del archivo de entrenamiento: ')
    archivoTest = input ('Ingrese la ruta del archivo de prueba: ')
    folder = input('ingrese la ruta donde quiere guardar los json: ')
    read_info(archivoTraining,archivoTest,folder)

#print(csv)

