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
        
        if opcion == 1:
            lectura.start()
        elif opcion == 2:
            dir = input('Ingrese el directorio donde se encuentra test y training')
            clasificadores.rocchio(dir)

        elif opcion == 3:
            return
        else: 
            break

            