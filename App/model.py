# ==============================
#Librerías
# ==============================


from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import list as lt
from DISClib.ADT import minpq as mpq

# -----------------------------------------------------
# API del TAD Catalogo de Libros
# -----------------------------------------------------

def newAnalyzer():
    analyzer={'companies':None
                }
    
    analyzer['companies'] = mp.newMap(numelements=1000,
                                        maptype='PROBING',
                                        comparefunction=compareCompanies
                                        )

    return analyzer


# Funciones para agregar informacion en analyzer

def addCompanies(map, trip):
    """
    Recibe analyzer['companies'] y carga al mapa:
        key = nombre de la compañía 
            ('Independent Owner' agrupa a los taxis que no están afiliados a una compañía) 
        value = tupla con la siguiente información:
            conteo alusivo a los servicios prestados
            lista con los id de los taxis afiliados a la misma
    """
    currentCompany = trip['company']
    if (currentCompany == ''):
        currentCompany = '"Independent Owner"'
    entry = mp.get(map, currentCompany)
    if (entry is None):
        serviceCont = 1
        taxiList = lt.newList(datastructure='ARRAY_LIST',
                            cmpfunction=compareElements)
        lt.addLast(taxiList,trip['taxi_id'])
        value = (serviceCont, taxiList)
        mp.put(map, currentCompany, value)
    else:
        tupla = entry["value"][0]
        tupla += 1
        lista = entry["value"][1]
        if ((lt.isPresent(lista,trip['taxi_id'])) == 0):
            lt.addLast(lista, trip['taxi_id'])
    return map


# -----------------------------------------------------
# Funciones de consulta
# -----------------------------------------------------


def totalTaxis(map):
    """
    Calcular total de taxis sin repetir id
    """
    listaRetorno = lt.newList('ARRAY_LIST')
    for company in mp.size(map):
        tupla = me.getValue(company)
        lista = tupla["value"][1]
        for taxi in lt.size(lista):
            taxiId = lt.getElement(lista, taxi)
            entry = lt.getElement(listaRetorno, taxiId)
            if (entry is None):
                lt.addLast(listaRetorno, taxiId)
    return lt.size(listaRetorno)


def totalCompanies(map):
    """
    Número total de compañías con al menos 1 taxi afiliado.
    Se ignoran los taxis registrados como 'Independet Owner'
    """
    exc = mp.get(map, 'Independet Owner')
    if (exc is None):
        return int(mp.size(map)
    else:
        return (int(mp.size(map)) - 1)


def topCompaniesTaxis(map):
    """
    Heap --> maxPQ de compañías por taxis afiliados
    """
    heap = mpq.newMinPQ(cmpfunction=compareCompanies)
    tupla = mp.get(map, company)
    lista = tupla["value"][1]
    valorCompany = lt.size(lista)
    mpq.insertWithValue(heap, me.getKey(map), valorCompany)
    return heap


def topCompaniesServices(map, top):
    """
    Heap --> maxPQ de compañías por servicios prestados
    """
    heap = mpq.newMinPQ(cmpfunction=compareCompanies)
    tupla = mp.get(map, company)
    valorCompany = tupla["value"][0]
    mpq.insertWithValue(heap, me.getKey(map), valorCompany)
    return heap
    

# ==============================
#Compare functions
# ==============================


def compareCompanies(company1, company2):
    companieKey = company2["key"]
    if (company1 == companieKey):
        return 0
    elif (company1 > companieKey):
        return 1
    else:
        return -1


def compareElements(element1, element2):
    if (element1 == element2):
        return 0
    elif (element1 > element2):
        return 1
    else:
        return -1