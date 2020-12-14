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
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc as scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
import datetime

from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Graphs import dfs as dfs

from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import rbt 
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as m
from DISClib.DataStructures import edge as ed
import datetime
assert config
from math import radians, cos, sin, asin, sqrt


"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria

Se define la estructura de un catálogo de libros.
El catálogo tendrá  una lista para los libros.

Los autores, los tags y los años se guardaran en
tablas de simbolos.
"""

# -----------------------------------------------------
# API del TAD Catalogo de Libros
# -----------------------------------------------------


def newAnalyzer():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los crimenes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.

    """
    clasificacion = "fechas"
    
    analyzer = {'accidentes': None,
                clasificacion: None,
                'connections':None,
                'duracion':None,
                'rango':None,
                'promedios':None
                

                
                }

    analyzer['accidentes'] = lt.newList('SINGLE_LINKED', compareIds)
    analyzer[clasificacion] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    
    analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=1400,
                                              comparefunction=compareStopIds)
    analyzer["rango"]={}   
    analyzer["duracion"]={}  
    analyzer["promedios"]={}
    
    return analyzer


# Funciones para agregar informacion al catalogo


def addAccident(analyzer, trip):
    """
    """
    
    clasificacion = "fechas"
    lt.addLast(analyzer['accidentes'], trip)
    updateDateIndex(analyzer[clasificacion], trip)
    if trip['pickup_community_area']!=trip['dropoff_community_area'] :
        hora_inicio=getDateTimeTaxiTripHour(trip['trip_start_timestamp'])
        hora_final=getDateTimeTaxiTripHour(trip['trip_end_timestamp'])
        origen = trip['pickup_community_area']+"-"+hora_a_string(hora_inicio)
        
        destination = trip['dropoff_community_area']+"-"+hora_a_string(hora_final)
        addStation(analyzer, destination)
        
        duration = float(trip['trip_seconds'])
        addStation(analyzer, origen)
        
        
        if not(trip['pickup_community_area'] in analyzer["rango"].keys()):
            analyzer["rango"][trip['pickup_community_area']]={}
            analyzer["rango"][trip['pickup_community_area']][hora_inicio]=origen
        else:
            if not(hora_inicio in analyzer["rango"][trip['pickup_community_area']]):
                analyzer["rango"][trip['pickup_community_area']][hora_inicio]=origen
        
        if not(trip['dropoff_community_area'] in analyzer["rango"].keys()):
            analyzer["rango"][trip['dropoff_community_area']]={}
            analyzer["rango"][trip['dropoff_community_area']][hora_final]=destination
        else:
            if not(hora_final in analyzer["rango"][trip['dropoff_community_area']]):
                analyzer["rango"][trip['dropoff_community_area']][hora_final]=destination
        if not(trip['pickup_community_area'] in analyzer["duracion"].keys()):
            analyzer["duracion"][trip['pickup_community_area']]={}
            analyzer["duracion"][trip['pickup_community_area']][hora_inicio]=hora_a_segundos(hora_inicio)
        else:
            if not(hora_inicio in analyzer["duracion"][trip['pickup_community_area']]):
                analyzer["duracion"][trip['pickup_community_area']][hora_inicio]=hora_a_segundos(hora_inicio)
        
        if not(trip['dropoff_community_area'] in analyzer["duracion"].keys()):
            analyzer["duracion"][trip['dropoff_community_area']]={}
            analyzer["duracion"][trip['dropoff_community_area']][hora_final]=hora_a_segundos(hora_final)
        else:
            if not(hora_final in analyzer["duracion"][trip['dropoff_community_area']]):
                analyzer["duracion"][trip['dropoff_community_area']][hora_final]=hora_a_segundos(hora_final)
        if not(origen in analyzer["promedios"].keys()):
            analyzer["promedios"][origen]={}
            analyzer["promedios"][origen][trip['dropoff_community_area']]=[float(duration)]
        else:
            if not (trip['dropoff_community_area'] in analyzer["promedios"][origen]):
                analyzer["promedios"][origen][trip['dropoff_community_area']]=[float(duration)]
            else:
                analyzer["promedios"][origen][trip['dropoff_community_area']].append(float(duration))
            
    return(analyzer)
        
def grafo(analyzer):
    for estacion_inicio in analyzer["rango"].keys():
        for hora in analyzer["rango"][estacion_inicio].keys():
            llave=analyzer["rango"][estacion_inicio][hora]
            
            if llave in analyzer["promedios"].keys():
                for estacion_f in analyzer["promedios"][llave].keys():
                    cantidad=0
                    tiempo=0
                    for duracion in analyzer["promedios"][llave][estacion_f]:
                        cantidad+=1
                        tiempo+=duracion
                    promedio=tiempo/cantidad
                    segundos_inicial=analyzer["duracion"][estacion_inicio][hora]
                    segundos=segundos_inicial+promedio
                    horas=segundos//3600
                    minutos=(segundos%3600)//900                       
                    minutos=minutos*15
                    if horas>23:
                        horas=horas-24
                    if minutos>45:
                        minutos=minutos-60
                    formato=str(int(horas))+":"+str(int(minutos))
                    segundos_duracion=(horas*3600)+(minutos*15)
                    destination = estacion_f+"-"+formato
                    addStation(analyzer, destination)
                    if not(estacion_f in analyzer["duracion"].keys()):
                        analyzer["duracion"][estacion_f]={}
                        analyzer["duracion"][estacion_f][datetime.datetime.strptime(formato,"%H:%M")]=segundos_duracion
                    else:
                        if not(datetime.datetime.strptime(formato,"%H:%M") in analyzer["duracion"][estacion_f]):
                            analyzer["duracion"][estacion_f][datetime.datetime.strptime(formato,"%H:%M")]=segundos_duracion
                    if not(estacion_f in analyzer["rango"].keys()):
                        analyzer["rango"][estacion_f]={}
                        analyzer["rango"][estacion_f][datetime.datetime.strptime(formato,"%H:%M")]=destination
                    else:
                        if not(datetime.datetime.strptime(formato,"%H:%M") in analyzer["rango"][estacion_f]):
                            analyzer["rango"][estacion_f][datetime.datetime.strptime(formato,"%H:%M")]=destination
                    addConnection(analyzer,analyzer["rango"][estacion_inicio][hora],destination,promedio)
    return (analyzer)




            


            


        
        
        


    
    
   
def compareStopIds(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1


def compareroutes(route1, route2):
    """
    Compara dos rutas
    """
    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1


def totalStops(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['connections'])


def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['connections'])
    
    return analyzer




def updateDateIndex(map, accidente):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """
    occurreddate = accidente['trip_start_timestamp']
    accidentdate = datetime.datetime.strptime(occurreddate, '%Y-%m-%dT%H:%M:%S.%f')
    entry = om.get(map, accidentdate.date())
    
    if entry is None:
        datentry = newDataEntry(accidente)
        om.put(map, accidentdate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, accidente)
    return map


def addDateIndex(datentry, accidente):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lstaccidents']
    lt.addLast(lst, accidente)
    offenseIndex = datentry['offenseIndex']
    offentry = m.get(offenseIndex, accidente['trip_id'])
    if (offentry is None):
        entry = newOffenseEntry(accidente['trip_id'], accidente)
        lt.addLast(entry['lstoffenses'], accidente)
        m.put(offenseIndex, accidente['trip_id'], entry)
    else:
        entry = me.getValue(offentry)
        lt.addLast(entry['lstoffenses'], accidente)
    return datentry


def newDataEntry(accidente):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'offenseIndex': None, 'lstaccidents': None}
    entry['offenseIndex'] = m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareOffenses)
    entry['lstaccidents'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry


def newOffenseEntry(offensegrp, crime):
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    ofentry = {'offense': None, 'lstoffenses': None}
    ofentry['offense'] = offensegrp
    ofentry['lstoffenses'] = lt.newList('SINGLELINKED', compareOffenses)
    return ofentry


# ==============================
# Funciones de consulta
# ==============================


def accidentSize(analyzer):
    """
    Número de crimenes
    """
    return lt.size(analyzer['accidentes'])


def indexHeight(analyzer):
    """
    Altura del arbol
    """
    
    respuesta=om.height(analyzer['fechas'])
    return (respuesta)


def indexSize(analyzer):
    """
    Numero de elementos en el indice
    """
    
    respuesta=om.size(analyzer['fechas'])
    
    return (respuesta)
    


def minKey(analyzer):
    """
    Llave mas pequena
    """
    
    respuesta=om.minKey(analyzer['fechas'])
    
    return (respuesta)
    
    


def maxKey(analyzer):
    """
    Llave mas grande
    """
    
    respuesta=om.maxKey(analyzer['fechas'])
    
    return (respuesta)
    
    
def porcentaje(total,porcion):
    respuesta=(100/total)*porcion
    return(respuesta)


def getAccidentsByRange(analyzer, initialDate, finalDate):
    """
    Retorna el numero de crimenes en un rago de fechas.
    """
    lst = om.values(analyzer['fechas'], initialDate, finalDate)
    lstiterator = it.newIterator(lst)
    totcrimes=0
    while (it.hasNext(lstiterator)):
        lstdate = it.next(lstiterator)
        totcrimes += lt.size(lstdate['accidentes'])
    return totcrimes


def compareIds(id1, id2):
    """
    Compara dos crimenes
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1


def compareDates(date1, date2):
    """
    Compara dos fechas
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1


def compareOffenses(offense1, offense2):
    """
    Compara dos tipos de crimenes
    """
    offense = me.getKey(offense2)
    if (offense1 == offense):
        return 0
    elif (offense1 > offense):
        return 1
    else:
        return -1


def compare_accidents(accident1,accident2):
    offense = me.getKey(accident2)
    if (accident1 == offense):
        return 0
    elif (accident1 > offense):
        return 1
    else:
        return -1

def addStation(citibike, stationid):
    """
    Adiciona una estación como un vertice del grafo
    """
    if not gr.containsVertex(citibike ['connections'], stationid):
            gr.insertVertex(citibike ['connections'], stationid)

    return citibike


def addConnection(citibike, origin, destination, duration):
    """
    Adiciona un arco entre dos estaciones. Si el arci existe se actualiza su peso con el promedio
    """
    edge = gr.getEdge(citibike['connections'], origin, destination)
    if edge is None:
        gr.addEdge(citibike['connections'], origin, destination, duration)
    else:

        ed.updateAverageWeight(edge,duration)

    return citibike

  


def updateDateIndex2(map, accidente):
    occurreddate = accidente['trip_start_timestamp']
   
    accidentdate = datetime.datetime.strptime(occurreddate, '%Y-%m-%dT%H:%M:%S.%f')
    entry = om.get(map, conversion(accidentdate))
    
    
    if entry is None:
        datentry = newDataEntry(accidente)
        om.put(map, conversion(accidentdate), datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, accidente)
    return map

def conversion(accidente):
    if accidente.minute<= 15:
        accidente=datetime.time(accidente.hour,0)
    elif accidente.minute<= 45:
        accidente=datetime.time(accidente.hour,30)
    else:
        if accidente.hour < 23:
            accidente=datetime.time((accidente.hour)+1,0)
        else:
            accidente=datetime.time(23,59)
    return accidente
        

def parteb1(analyzer,limite,fecha):
    lista=[]
    a=0
    'limite=3'
    'fecha="2019-10-31"'
    for key in analyzer["fechas"]:
        if key != "cmpfunction" and key != "type":
            fecha_actual=str(analyzer["fechas"][key]["key"])
            if fecha==fecha_actual:
                actual=analyzer["fechas"][key]["value"]["offenseIndex"]["table"]["elements"]
                while a<limite:
                    maximo=0
                    for key2 in actual:
                        if key2["value"]!= None:
                            info_taxi=key2["value"]["lstoffenses"]["first"]["info"]
                            distancia=float(info_taxi["trip_miles"])
                            tarifa=float(info_taxi["fare"])
                            if distancia>0 and tarifa>0:
                                puntaje=float(info_taxi["trip_total"])
                                if puntaje>maximo and info_taxi["taxi_id"] not in lista:
                                    maximo=puntaje
                                    mayor=info_taxi["taxi_id"]
                    a+=1
                    lista.append(mayor)
                    lista.append(maximo)
    return print("El top "+ str(limite) +" de taxis con más puntos en la fecha "+ fecha+" ", lista)

def parteb2(analyzer,limite,dia1,mes1,año1,dia2,mes2,año2):
    lista=[]
    a=0
    'limite=3'
    fecha1=datetime.date(año1,mes1,dia1)
    fecha2=datetime.date(año2,mes2,dia2)
    print(fecha1)
    arbol=rbt.values(analyzer["fechas"],fecha1,fecha2)
    actual=arbol["first"]["info"]["offenseIndex"]["table"]["elements"]
    while a<limite:
        maximo=0
        for element in actual:
            if element["value"]!=None:
                distancia=element["value"]["lstoffenses"]["first"]["info"]["trip_miles"]
                tiempo=element["value"]["lstoffenses"]["first"]["info"]["fare"]
                if distancia != "" and tiempo != "":
                    distancia=float(distancia)
                    tiempo=float(tiempo)
                    if tiempo>0 and distancia>0:
                        puntaje=float(element["value"]["lstoffenses"]["first"]["info"]["trip_total"])
                        if puntaje>maximo and element["value"]["lstoffenses"]["first"]["info"]["taxi_id"] not in lista:
                            maximo=puntaje
                            mayor=element["value"]["lstoffenses"]["first"]["info"]["taxi_id"]
        lista.append(mayor)
        lista.append(maximo)
        a+=1
    return print("El top "+ str(limite) +" de taxis con más puntos entre las fechas "+ str(fecha1)+" y "+str(fecha2)+" ", lista)


def getDateTimeTaxiTripHour(tripstartdate):
    taxitripdatetime = datetime.datetime.strptime(tripstartdate, '%Y-%m-%dT%H:%M:%S.%f')
    return(taxitripdatetime.time())
def hora_a_string(hora):
    devolver=str(hora.hour)+":"+str(hora.minute)
    return(devolver)

def hora_a_segundos(hora):
    h_segundos=hora.hour*3600
    m_seguntos=hora.minute*60
    segundos=h_segundos+m_seguntos
    return(segundos)

def tiempo_espera(analyzer):
    for a in analyzer["duracion"].keys():
        print(a)

        for b in  analyzer["duracion"][a].keys():
            for c in analyzer["duracion"][a].keys():
                if b != c:
                    if analyzer["duracion"][a][c]<analyzer["duracion"][a][b]:
                        duration_menor=analyzer["duracion"][a][b]-analyzer["duracion"][a][c]
                        duration_mayor=(24*3600)-duration_menor
                        addConnection(analyzer,analyzer["rango"][a][c],analyzer["rango"][a][b], duration_menor)
                        addConnection(analyzer,analyzer["rango"][a][b],analyzer["rango"][a][c], duration_mayor)
                    else:
                        duration_menor=analyzer["duracion"][a][c]-analyzer["duracion"][a][b]
                        duration_mayor=(24*3600)-duration_menor
                        addConnection(analyzer,analyzer["rango"][a][b],analyzer["rango"][a][c], duration_menor)
                        addConnection(analyzer,analyzer["rango"][a][c],analyzer["rango"][a][b], duration_mayor)
    return(analyzer)

def hora_adecuada(analyzer,hora_i,hora_f,estacion_i,estacion_f):
    mayor=365*24*3600
    mejor=None
    ruta=None
    for a in analyzer["rango"][estacion_i].keys():
        hora=str(a.hour)
        minute=str(a.minute)
        comprar=hora+":"+minute
        tiempo=datetime.datetime.strptime(comprar, '%H:%M')
        print(tiempo)
        print(hora_i)
        print(hora_f)
        if tiempo>=hora_i and tiempo<=hora_f:
            grafo=djk.Dijkstra(analyzer["connections"],analyzer["rango"][estacion_i][a])
            for b in analyzer["rango"][estacion_f].keys():
                if djk.hasPathTo(grafo,analyzer["rango"][estacion_f][b]):
                    if mayor > djk.distTo(grafo,analyzer["rango"][estacion_f][b]):
                        mayor= djk.distTo(grafo,analyzer["rango"][estacion_f][b])
                        ruta= djk.pathTo(grafo,analyzer["rango"][estacion_f][b])
                        mejor=analyzer["rango"][estacion_i][a]
    return({"mejor hora: ":mejor,"ruta: ":ruta,"duracion: ":mayor})


















