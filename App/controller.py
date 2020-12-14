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

import config as cf
from App import model
import datetime
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
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
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



def callTotalTaxis(cont):
    return model.totalTaxis(cont['companies'])

def callTotalCompanies(cont):
    return model.totalCompanies(cont['companies'])

def callTopServices(cont, tops):
    return model.topCompaniesServices(cont['companies'], tops)

def calltopTaxis(cont, tops):
    return model.topCompaniesTaxis(cont['companies'], tops)

def accidentSize(analyzer):
    """
    Numero de crimenes leidos
    """
    return model.accidentSize(analyzer)


def indexHeight(analyzer):
    """
    Altura del indice (arbol)
    """
    return model.indexHeight(analyzer)


def indexSize(analyzer):
    """
    Numero de nodos en el arbol
    """
    return model.indexSize(analyzer)


def minKey(analyzer):
    """
    La menor llave del arbol
    """
    return model.minKey(analyzer)


def maxKey(analyzer):
    """
    La mayor llave del arbol
    """
    return model.maxKey(analyzer)


def getAccidentsNumberByRange(analyzer, initialDate, finalDate):
    initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
    finalDate = datetime.datetime.strptime(finalDate, '%Y-%m-%d')
    return model.getAccidentsNumberByRange(analyzer, initialDate.date(), finalDate.date())


def getAccidentsSeverityByRange(analyzer, initialDate, finalDate):
    initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
    finalDate = datetime.datetime.strptime(finalDate, '%Y-%m-%d')
    return model.getAccidentsSeverityByRange(analyzer, initialDate.date(), finalDate.date())
    

def getAccidentsByRange(analyzer, initialDate, finalDate):
    """
    Retorna el total de crimenes en un rango de fechas
    """
    initialDate = datetime.datetime.strptime(initialDate, "%H:%M")
    finalDate = datetime.datetime.strptime(finalDate, '%H:%M')
    initialDate=model.conversion(initialDate)
    finalDate=model.conversion(finalDate)
    return model.getAccidentsByRange(analyzer, initialDate,
                                  finalDate)
    

def getAccidentsBydate(analyzer, date):
    fecha=datetime.datetime.strptime(date,"%Y-%m-%d")
    retorno=model.getAccidentsbydate(analyzer,fecha.date(),1)
    return retorno

def parteb1(analyzer,limite,fecha):
    model.parteb1(analyzer,limite,fecha)

def parteb2(analyzer,limite,dia1,mes1,año1,dia2,mes2,año2):
    model.parteb2(analyzer,limite,dia1,mes1,año1,dia2,mes2,año2)

def partec(analyzer,hora_i,hora_f,estacion_i,estacion_f,auto):
    analyzer=model.grafo(analyzer)
    if auto==1:
        analyzer=model.tiempo_espera(analyzer)
    initialhour = datetime.datetime.strptime(hora_i, "%H:%M")
    finalhour = datetime.datetime.strptime(hora_f, '%H:%M')
    respuesta=model.hora_adecuada(analyzer,initialhour,finalhour,estacion_i,estacion_f)
    return(respuesta)

   
