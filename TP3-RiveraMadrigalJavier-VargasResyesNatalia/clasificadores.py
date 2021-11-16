
import json

global clases
global totalDocuments
totalDocuments = 0
clases = {}
#clase=[docsClase,centroide,[terminos]]
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
            clases[coleccion[doc]['CLASE']] = [1,0,[]]

        index+=1

def sumarCantidad(clase,term):
    for terms in clases[clase][2]:
        if term == terms[0]:
            print(term[1])
            term[1] = terms[1]+1
    return 

def getTerminosClase(clase,coleccion):
    for doc in coleccion:
        if coleccion[doc]['CLASE']==clase:
            for term in coleccion[doc]['POSTINGS']:
                #termAppend = [termino, cantTermino, vector]
                termAppend = [term[0],0]
                if termAppend not in clases[clase][2]:
                    clases[clase][2].append(termAppend)
               # else:
                #    sumarCantidad(clase,term[0])
    return

def sumarPromedio(promedio,term,terminosDoc):
    for terminoDoc in terminosDoc:
        if terminoDoc[0] ==  term:
            promedio += float(terminoDoc[1])
            break
    return promedio        

def calcularVector(clase,coleccion,b,g):
    #Termino, qc
   
    for term in clases[clase][2]:
        promC = 0
        promNotC = 0
        for doc in coleccion:
            if coleccion[doc]['CLASE']== clase:
                promC = sumarPromedio(promC,term[0],coleccion[doc]['POSTINGS'])
            else:
                promNotC = sumarPromedio(promNotC,term[0],coleccion[doc]['POSTINGS'])
        
        term[1] = round((promC/clases[clase][0])*b - (promNotC/(totalDocuments-clases[clase][0]))*g,6 )



    
    return 

def calculateCentroide(key,b,y):
    #clases[key][0] = documentos que estan en la clase p
    centroide = ((b/clases[key][0])*clases[key][0])-(y/(totalDocuments-clases[key][0])*(clases[key][0]-totalDocuments))
    clases[key][1] = centroide
    return

def rocchio(dir):
    coleccion = json.load(open(dir+'/'+'coleccion.json','r'))
    getClasses(coleccion)
    getTotalDocuments(coleccion)

    for i in clases:
        getTerminosClase(i,coleccion) #agrega los terminos de la clase en el dict clases
        calcularVector(i,coleccion,0.75,0.25)
        #calculateCentroide(i,0.75,0.25)

    print(clases)

    

   

dir='C:/Users/javir/Desktop/TEC Javi/RIT/TP3-RiveraMadrigalJavier-VargasResyesNatalia/Index'

rocchio(dir)