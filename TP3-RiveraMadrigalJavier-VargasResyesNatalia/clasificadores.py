
import json

global clases
global totalDocuments
totalDocuments = 0
clases = {}

def getTotalDocuments(coleccion):
    global totalDocuments
    for doc in coleccion:
        totalDocuments = totalDocuments+1


def getClasses(coleccion):
    index = 0

    for doc in coleccion:

        if (coleccion[doc]['CLASE'] in clases):
            clases[coleccion[doc]['CLASE']][0] = clases[coleccion[doc]['CLASE']][0]+1
        else:
            clases[coleccion[doc]['CLASE']] = [1,0]

        index+=1


    

def calculateCentroide(key,b,y):
    centroide = ((b/clases[key][0])*clases[key][0])-(y/(totalDocuments-clases[key][0])*(clases[key][0]-totalDocuments))
    clases[key][1] = centroide
    return

def rocchio(dir):
    coleccion = json.load(open(dir+'/'+'coleccion.json','r'))
    getClasses(coleccion)
    getTotalDocuments(coleccion)

    for i in clases:
        calculateCentroide(i,0.75,0.25)

    print(clases)

    

   

dir='C:/Users/javir/Desktop/TEC Javi/RIT/TP3-RiveraMadrigalJavier-VargasResyesNatalia/Index'

rocchio(dir)