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

import config as cf
from App import model
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________

def init():
    analyzer = model.newAnalyzer()
    return analyzer

# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________


def cabFileSelection(file):
    if file == '1':
        cabFile = 'taxi-trips-wrvz-psew-subset-small.csv'
    elif file == '2':
        cabFile = 'taxi-trips-wrvz-psew-subset-medium.csv'
    else:
        cabFile = 'taxi-trips-wrvz-psew-subset-large.csv'
    return cabFile


def loadData(analyzer, cabFile):
    cabFile = cf.data_dir + cabFile
    input_file = csv.DictReader(open(cabFile, encoding="utf-8"), delimiter=",")
    for trip in input_file:
        model.addCompanies(analyzer['companies'], trip)
    return analyzer

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________