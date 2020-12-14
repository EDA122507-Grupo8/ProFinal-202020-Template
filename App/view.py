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
 * Contribución de:
 *
 * Dario Correal
 *
 """


import sys
import config
from App import controller
from App import model
from DISClib.ADT import stack
import timeit
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________


# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1. Inicializar Analizador")
    print("2. Cargar información de taxis")
    print("3. Mostrar reporte")
    print("4. Sistema de puntos y premios")
    print("5. Consultar mejor horario para una ruta")
    print("0. Salir")
    print("*******************************************")

"""
Menu principal
"""

while True:
    printMenu()
    eleccion = input('Digite la opción que desea: ')

    if int(eleccion[0]) == 1:
        print("\nInicializando...")
        cont = controller.init()
    
    elif int(eleccion[0]) == 2:
        print("Indique el tamaño del archivo: \n")
        print("1. Small")
        print("2. Medium")
        print("3. Large\n")
        tamanio = input()
        tripFile = controller.cabFileSelection(tamanio)
        print("\nCargando información de viajes...")
        controller.loadData(cont, tripFile)
    
    elif int(eleccion[0]) == 3:
        print("Ingrese el número de tops que desea conocer: \n")
        tops = int(input())
        print("El total de taxis encontrados ene l archivos ed de: " + str(controller.callTotalTaxis(cont)))
        print("El total de compañías con al menos un taxi afiliado es de: " + str(controller.callTotalCompanies(cont)))
        print("EL Top de compañías por taxis afiliados es: \n")
        print(controller.calltopTaxis(cont, tops))
        print("EL Top de compañías por servicios prestados es: \n")
        print(controller.callTopServices(cont, tops))

    elif int(eleccion[0]) == 4:
        None
    elif int(eleccion[0]) == 5:
        None
    else:
        sys.exit(0)
