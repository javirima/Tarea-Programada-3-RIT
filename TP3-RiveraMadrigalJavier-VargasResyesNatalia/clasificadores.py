
import json
import numpy as np

global clases
global totalDocuments
global bayesianosClases
global niBayesianos
totalDocuments = 0
clases = {}
bayesianosClases = {}  #Frecuencias de clases por termino
niBayesianos = {}      #Ni para Frecuencias de clases por termino
vectoresBayesianos = {}

#clase=[docsClase,centroide,[terminos]]

#-----------------------------------Inicio Bayesianos--------------------------------------#

def calQip(termino,clase):
    global bayesianosClases
    for listaTermino in  bayesianosClases[clase][1]:
        if listaTermino[0] == termino:
            #print((1+niBayesianos[termino]-listaTermino[1])/(2+totalDocuments-listaTermino[1]))
            return (1+niBayesianos[termino]-listaTermino[1])/(2+totalDocuments-listaTermino[1])

    return 0
    

def calPip(termino,clase):
    global bayesianosClases
    for listaTermino in  bayesianosClases[clase][1]:
        if listaTermino[0] == termino:
            #print((1+listaTermino[1]) / (2+bayesianosClases[clase][0]))
            return (1+listaTermino[1])/(2+bayesianosClases[clase][0])  #(1+nip)/(2+ni)
    return 0



def calVectorsPerClassBayesian():
    global bayesianosClases
    tempDicc = {} #Para guardar {"Clase": [ [termino1,#], [termino2,#] ]}
                  #Donde # es la formula (Pip/(1-Pip)) + log((1-qip)/qip)
    for clase in bayesianosClases:
        tempDicc[clase] = []
        for listaTermino in bayesianosClases[clase][1]:
            termino = listaTermino[0]
            pip = calPip(termino,clase)
            qip = calQip(termino,clase)
            formule = np.round(np.log2(pip/(1-pip))+ np.log2((1-qip)/qip), 3)
            tempDicc[clase].append([termino,formule])

    print(tempDicc)
            #print(formule)
            #listaTermino[1]

def searchInTerms(termino, postings):
    #Decir si un termino se encuentra en los terminos de alguna clase en bayesianosClases
    for post in postings:
        if (post[0]==termino):
            return True
    return False


def addFrecInClass(termino, postings):
    for post in postings:
        if (post[0]==termino):
            post[1]+=1
    return False

def getClassesInfomation(coleccion):
    global bayesianosClases
    global totalDocuments

    for doc in coleccion:

        clase = coleccion[doc]['CLASE']
        
        if (clase in bayesianosClases):  #Si la clase ya existe en el dicc
            bayesianosClases[clase][0] = bayesianosClases[clase][0]+1
        else:
            bayesianosClases[clase] = [1,[]]  #Agrega la clase con su frecuencia y lista de terminos
            
       
        
        for listaTermino in coleccion[doc]["POSTINGS"]:  #recorre lista de postings del doc actual
            
            if(searchInTerms(listaTermino[0],bayesianosClases[clase][1])): #Si el termino está en la lista de posting de la clase del doc actual
                
                addFrecInClass(listaTermino[0],bayesianosClases[clase][1]) #Agregar la frecuencia 
                
            else:
                bayesianosClases[clase][1].append([listaTermino[0],1])  #agrega una lista de termino y frecuencia en los postings de bayesianosClases


            if listaTermino[0] in niBayesianos:
                niBayesianos[listaTermino[0]] += 1
                
            else:
                niBayesianos[listaTermino[0]] = 1

        totalDocuments = totalDocuments+1  #Contar docs, total np



#----------------------------------Fin Bayesianos--------------------------------------------#



        
def getClasses(coleccion):
    global clases
    global totalDocuments
    index = 0

    for doc in coleccion:

        if (coleccion[doc]['CLASE'] in clases):
            clases[coleccion[doc]['CLASE']][0] = clases[coleccion[doc]['CLASE']][0]+1
        else:
            clases[coleccion[doc]['CLASE']] = [1,0,[]]

        index+=1
        totalDocuments = totalDocuments+1  #Contar docs

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
    print(clases)

    for i in clases:
        getTerminosClase(i,coleccion) #agrega los terminos de la clase en el dict clases
        print(clases)
        calcularVector(i,coleccion,0.75,0.25)
        #calculateCentroide(i,0.75,0.25)

    print(clases)

    

def main(dir):
    coleccion = json.load(open(dir+'/'+'coleccion.json','r'))
    getClassesInfomation(coleccion)
    #print(bayesianosClases)
    print()
    print("----------------------------------------------------------------------------------------------------------------------")
    print()
    #print(niBayesianos)
    calVectorsPerClassBayesian()


#dir='C:/Users/javir/Desktop/TEC Javi/RIT/TP3-RiveraMadrigalJavier-VargasResyesNatalia/Index'
dir='D:\\2 SEMESTRE 2021\\RIT\\PROYECTOS\\Proyecto 3\\Tarea-Programada-3-RIT\\TP3-RiveraMadrigalJavier-VargasResyesNatalia\\Index'

#rocchio(dir)

main(dir)






