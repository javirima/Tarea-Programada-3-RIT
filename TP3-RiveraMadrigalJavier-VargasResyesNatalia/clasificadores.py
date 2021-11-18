
import json
import numpy as np
import operator
import lectura
import math

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
def printDicc(dicc):
    for key in dicc:
        print(key,": ",dicc[key])

        
def getHighKey(totalPerClass):
    '''
    Da la llave con valor más alto, para un diccionario con formato {"class1":#,"class2":#}
    '''
    max_key = max(totalPerClass, key = totalPerClass.get)
    return max_key


def getValueTermPerClass(termino, postings):
    '''
    Suma en cada clase los valores asociados a la formula  log2(pip/(1-pip))+ log2((1-qip)/qip)
    para cada termino, para clase.
    En este caso, según los terminos que tenga un documento, se van sumando a la cada clase
    según los valores que posee, para luego determinar el valor más alto.
    Nota: post[0] es el termino, post[1] es el valor calculado con la formula
    '''
    for post in postings:
        if (post[0]==termino):
            return post[1]
    return False



def originalClassPerDoc(testSet):
    '''
    Da los Id de cada documento y su clase original
    Nota: El formato de originalClassPerDoc es {"doc":"class"}
    '''
    
    originalClassPerDoc = {}
    
    for doc in testSet:
        docId = testSet[doc]["DOCID"]
        clase = testSet[doc]["CLASE"]
        originalClassPerDoc[docId] = clase
            
    return originalClassPerDoc


def calClassPerDoc(testSet,vectorsPerClassBayesian):
    '''
    Para cada documento del testSet, se recorren los postings para extraer cada termino
    luego para cada clase existente en vectorsPerClassBayesian, si la clase tiene el
    termino del doc, se suma. Al finalizar, la clase con el valor más alto, es la
    clase que define al documento.
    Nota: El formato de estimatedClassPerDoc es {"doc":"class"}
    '''
    
    estimatedClassPerDoc = {}
    totalPerClass = {}
    
    for doc in testSet:
        postings = testSet[doc]["POSTINGS"]  # formato [[termino1,#],[termino2,#]]
        docId = testSet[doc]["DOCID"]
        for listaTermino in postings:  #recorre lista de postings del doc actual
            termino = listaTermino[0]

            for clase in vectorsPerClassBayesian:
                if (searchInTerms(termino,vectorsPerClassBayesian[clase])):  #verifica que el termino se encuentre en los posting de esa clase
                    totalPerClass[clase] += getValueTermPerClass(termino,vectorsPerClassBayesian[clase])
                else:
                    totalPerClass[clase] = 0   

            highKey = getHighKey(totalPerClass)
            #print(totalPerClass,totalPerClass[highKey])  #Puede ser que también guardar para cada doc,todos los valores por clase
            #getHigh(totalPerClass)
            estimatedClassPerDoc[docId] = [highKey,totalPerClass[highKey]] #Guardar el valor que le quedó
            
    return estimatedClassPerDoc
                    

                
    
def calQip(termino,clase):
    '''
    Calcular el qip que es P('ki|Ci), es decir la probabilidad de que sea cualquier otro término
    aparte de Ki, dado que es de la clase Ci
    Notas: termino[0] es el termino y termino[1] es la frecuencia del termino por clase
    Se calcula (1+(ni-nip))/(2+(Nt-np))
    '''
    global bayesianosClases
    for listaTermino in  bayesianosClases[clase][1]:
        if listaTermino[0] == termino:
            #print((1+niBayesianos[termino]-listaTermino[1])/(2+totalDocuments-listaTermino[1]))
            return (1+(niBayesianos[termino]-listaTermino[1]))/(2+(totalDocuments-bayesianosClases[clase][0])) 

    return 0
    

def calPip(termino,clase):
    '''
    Calcular el qip que es P(ki|Ci), es decir la probabilidad de que sea el término Ki
    dado que es de la clase Ci
    Notas: termino[0] es el termino y termino[1] es la frecuencia del termino por clase
    Se calcula (1+nip)/(2+np)
    '''
    global bayesianosClases
    for listaTermino in  bayesianosClases[clase][1]:
        if listaTermino[0] == termino:
            #print((1+listaTermino[1]) / (2+bayesianosClases[clase][0]))
            return (1+listaTermino[1])/(2+bayesianosClases[clase][0])   
    return 0



def calVectorsPerClassBayesian():
    '''
    Similitudes por clase.
    Retorna un diccionario con las clases y sus terminos una vez calculados los pip y qip para
    realizar la formula log2(pip/(1-pip))+ log2((1-qip)/qip)
    Nota: tempDicc tiene el siguiente formato {"Clase": [ [termino1,#], [termino2,#] ]}
    '''
    global bayesianosClases
    tempDicc = {} 

    for clase in bayesianosClases:
        tempDicc[clase] = []
        for listaTermino in bayesianosClases[clase][1]:
            termino = listaTermino[0]
            pip = calPip(termino,clase)
            qip = calQip(termino,clase)
            formule = np.round(np.log2(pip/(1-pip))+ np.log2((1-qip)/qip), 3)
            tempDicc[clase].append([termino,formule])  

    return tempDicc
    


def searchInTerms(termino, postings):
    '''
    Decir si un termino se encuentra en los terminos de alguna clase en bayesianosClases
    '''

    for post in postings:
        if (post[0]==termino):
            return True
    return False


def addFrecInClass(termino, postings):
    '''
    Suma una unidad a las frecuencias de un término dado y una lista de posting dados
    la lista de postings tiene el formato postings = [[post1,#],[post2,#]]
    '''
    for post in postings:
        if (post[0]==termino):
            post[1]+=1
    return False


def getClassesInfomation(coleccion):
    '''
    Para la coleccion dada recorre por documentos para separarlos en clases  y guaradarlos
    en bayesianosClases, para cada termino de los posting del documento revisa si existen en la
    clase actual del diccionario de bayesianosClases, si no está agrega el termino, si sí está
    agrega 1 a la frecuencia. Y finalmente por cada termino existente se va contabilizando en
    cuantos documentos estaba y se guarda en el diccionario niBayesianos.
    '''
    global bayesianosClases
    global totalDocuments

    for doc in coleccion:

        clase = coleccion[doc]['CLASE']
        
        if (clase in bayesianosClases):  #Si la clase ya existe en el dicc
            bayesianosClases[clase][0] = bayesianosClases[clase][0]+1
        else:
            bayesianosClases[clase] = [1,[]]  #Agrega la clase con su frecuencia y lista de terminos
            
       
        
        for listaTermino in coleccion[doc]["POSTINGS"]:  #recorre lista de postings del doc actual
            
            termino = listaTermino[0]
            if(searchInTerms(termino,bayesianosClases[clase][1])): #Si el termino está en la lista de posting de la clase del doc actual
                
                addFrecInClass(termino,bayesianosClases[clase][1]) #Agregar la frecuencia 
                
            else:
                bayesianosClases[clase][1].append([termino,1])  #agrega una lista de termino y frecuencia en los postings de bayesianosClases


            if termino in niBayesianos:
                niBayesianos[termino] += 1
                
            else:
                niBayesianos[termino] = 1

        totalDocuments = totalDocuments+1  #Contar docs, total np



#----------------------------------Fin Bayesianos--------------------------------------------#



        
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
        res = (promC/clases[clase][0])*b - (promNotC/(totalDocuments-clases[clase][0]))*g
        res = round(math.sqrt(res**2),6)
        term[1] = res

    return 


def revisarTermino(clase,term):
    encontrado = False
    for termClase in clases[clase][2]:
        if termClase[0] == term:
            encontrado = True
            break
    if encontrado == False:
        clases[clase][2].append([term,0])


'''
def agregarTerminosCentroide(coleccion):
    for clase in clases:
        for post in coleccion:
            for term in coleccion[post]['POSTINGS']:
                revisarTermino(clase,term)
    return
'''
def simDocCentroide(docPost,centroidPost):
    multTerms = [] 
    for term in docPost:
        if term in centroidPost.keys():
            multTerms.append(float(docPost[term])*float(centroidPost[term]))
    res = 0
    for mult in multTerms:
        res = res + mult

    return round(res,6)


def rocchio(dir):
    coleccion = json.load(open(dir+'/'+'training.json','r'))
    prueba =  json.load(open(dir+'/'+'test.json','r'))
    getClasses(coleccion)
    getTotalDocuments(coleccion)

    for i in clases:
        getTerminosClase(i,coleccion) #agrega los terminos de la clase en el dict clases
        calcularVector(i,coleccion,0.75,0.25)
        #agregarTerminosCentroide(coleccion)

    for doc in prueba:
        postDoc = dict(prueba[doc]['POSTINGS'])
        sim = ['',-10]
        escalafonDoc = []
        for clase in clases:
            postClass = dict(clases[clase][2])
            simCentroid =simDocCentroide(postDoc,postClass)
            escalafonDoc.append([clase,simCentroid])

            if simCentroid > sim[1]:
                sim[0] = clase
                sim[1] = simCentroid

        if sim[0] != prueba[doc]['CLASE']:
            print(prueba[doc]['DOCID']+': '+prueba[doc]['CLASE'] , sim,'diff')
        else:
            print(prueba[doc]['DOCID']+': '+prueba[doc]['CLASE'] , sim)

        print('Escalafon :', escalafonDoc)
        print('\n\n')
        
    lectura.saveIndex(dir,clases,'centroides')

    
    
def main(dir):
    trainingSet = json.load(open(dir+'/'+'training.json','r'))
    testSet = json.load(open(dir+'/'+'test.json','r'))
    getClassesInfomation(trainingSet)
    #print(bayesianosClases)
    print()
    print("----------------------------------------------------------------------------------------------------------------------")
    print()
    #print(niBayesianos)
    vectorsPerClassBayesian = calVectorsPerClassBayesian()
    #print(vectorsPerClassBayesian)
    estimatedClassPerDoc = calClassPerDoc(testSet,vectorsPerClassBayesian)
    originalClasses = originalClassPerDoc(testSet)
    #xd = originalClassPerDoc(trainingSet)

    printDicc(estimatedClassPerDoc)
    print("-----------------------------------------------------------------------------------------------------------------------")
    printDicc(originalClasses)
    #print("-----------------------------------------------------------------------------------------------------------------------")
    #printDicc(xd)
    


#dir='C:/Users/javir/Desktop/TEC Javi/RIT/TP3-RiveraMadrigalJavier-VargasResyesNatalia/Index'
#dir='D:\\2 SEMESTRE 2021\\RIT\\PROYECTOS\\Proyecto 3\\Tarea-Programada-3-RIT\\TP3-RiveraMadrigalJavier-VargasResyesNatalia\\Index'

#rocchio(dir)

#main(dir)






