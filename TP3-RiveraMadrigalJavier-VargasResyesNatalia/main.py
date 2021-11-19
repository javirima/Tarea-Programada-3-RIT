import lectura
import clasificadores

def menu():
    while True:
        print('**MENU**')
        print('1. Leer datos')
        print('2. Clasificador Rocchio')
        print('3. Clasificador Bayesianos')
        print('4. Salir')

        opcion = input('Ingrese la opcion: ')
        
        if opcion == '1':
            print('holi')
            lectura.start()
        elif opcion == '2':
            dir = input('Ingrese el directorio donde se encuentra test y training: ')
            clasificadores.rocchio(dir,0.75,0.25)
            #clasificadores.rocchio(dir,0.85,0.15)
            #clasificadores.rocchio(dir,0.95,0.05)

        elif opcion == '3':
            dir = input('Ingrese el directorio donde se encuentra test y training: ')
            clasificadores.bayesianos(dir)
            return
        else: 
            break

menu()


#D:\\2 SEMESTRE 2021\\RIT\\PROYECTOS\\Proyecto 3\\Tarea-Programada-3-RIT\\TP3-RiveraMadrigalJavier-VargasResyesNatalia\\Index
#C:/Users/javir/Desktop/TEC Javi/RIT/TP3-RiveraMadrigalJavier-VargasResyesNatalia/Index
