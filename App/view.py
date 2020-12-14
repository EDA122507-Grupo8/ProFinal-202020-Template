"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

import sys
import config
from App import controller
assert config
import model as mdl
import datetime
"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________


# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de accidentes")
    print("3- Consultar puntos de taxi en una fecha")
    print("4- Consultar puntos de taxi en el rango de fechas")
    print("8- consulta del mejor horario para desplazarse entre dos “Community Area” ")
    print("0- Salir")
    print("*******************************************")


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()
        
    elif int(inputs[0]) == 2:
        accidentfile="taxi-small.csv"
        print("\nCargando información de taxis ....")        
        controller.loadData(cont, accidentfile)
        
        print("si se necesita cargar mas archivos llame otra vez la funcion")
        print('Accidentes cargados: ' + str(controller.accidentSize(cont)))
        print('Altura del arbol: ' + str(controller.indexHeight(cont)))
        print('Elementos en el arbol: ' + str(controller.indexSize(cont)))
        print('Menor Llave: ' + str(controller.minKey(cont)))
        print('Mayor Llave: ' + str(controller.maxKey(cont)))

        print(cont["rango"])
        
    elif int(inputs[0]) == 3:
        limite=int(input("Inserte límite"))
        fecha=input("Inserte fecha")
        controller.parteb1(cont,limite,fecha)

    elif int(inputs[0]) == 4:
        dia1=int(input("Inserte dia fecha1 "))
        mes1=int(input("Inserte mes fecha1 "))
        año1=int(input("Inserte año fecha1 "))
        dia2=int(input("Inserte dia fecha2 "))
        mes2=int(input("Inserte mes fecha2 "))
        año2=int(input("Inserte año fecha2 "))
        limite=int(input("Inserte límite"))
        controller.parteb2(cont,limite,dia1,mes1,año1,dia2,mes2,año2)

    elif int(inputs[0])==8:
        auto=int(input("desea tiempos de espera? (si=1) o (no=0)\n"))
        estacion_i=input("inserte estacion origen\n")
        estacion_f=input("inserte estacion final\n")
        hora_i=input("inserte hora inicio\n")
        hora_f=input("inserte hora limite\n")
        print(controller.partec(cont,hora_i,hora_f,estacion_i,estacion_f,auto))


    else:
        sys.exit(0)
sys.exit(0)