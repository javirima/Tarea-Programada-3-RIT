
import pandas as pd
import json
import os


global coleccion



coleccion = {}

def saveIndex(rutaIndice,coleccion):
    if os.path.exists(rutaIndice):
        createIndex(rutaIndice,coleccion)

    else:
        os.makedirs(rutaIndice)
        createIndex(rutaIndice,coleccion)

def createIndex(rutaIndice,coleccion):
    with open(rutaIndice+'/'+'coleccion.json', 'w') as c:   
            json.dump(coleccion, c)
    

def getTerms(docTerms, index):
    terms = docTerms.split(' ')
    for term in terms:
        obj = term.split('/')
        coleccion[index]['POSTINGS'].append(obj)



    return 

def read_info(archivo,folder):
    csv = pd.read_csv(archivo, index_col=0)
    index = 0
    for doc in csv.index:
        
        items = doc.split('\t')
        print(items)
        coleccion[index] = dict({'DOCID':items[0],'CLASE':items[1], 'NTERMINOS':items[2], 'POSTINGS':[]})
    
        getTerms(items[3],index)
        index+=1
    
    saveIndex(folder, coleccion)
    return 


#archivo = "C:/Users/javir/Desktop/TEC Javi/RIT/TP3-RiveraMadrigalJavier-VargasResyesNatalia/test-set.csv"
#folder = 'C:/Users/javir/Desktop/TEC Javi/RIT/TP3-RiveraMadrigalJavier-VargasResyesNatalia/Index'
archivo = 'D:\\2 SEMESTRE 2021\\RIT\\PROYECTOS\\Proyecto 3\\Tarea-Programada-3-RIT\\TP3-RiveraMadrigalJavier-VargasResyesNatalia\\training-set.csv'
folder = 'D:\\2 SEMESTRE 2021\\RIT\\PROYECTOS\\Proyecto 3\\Tarea-Programada-3-RIT\\TP3-RiveraMadrigalJavier-VargasResyesNatalia\\Index'

read_info(archivo,folder)


#print(csv)

