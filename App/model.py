# ==============================
#Librerías
# ==============================


from DISClib.ADT import map as mp
from DISClib.DataStructures import mapstructure as ms
from DISClib.DataStructures import mapentry as me
from DISClib.DataStructures import listiterator as it
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
        serviceCont = [1]
        taxiList = lt.newList(datastructure='ARRAY_LIST',
                            cmpfunction=compareElements)
        lt.addLast(taxiList,trip['taxi_id'])
        value = (serviceCont, taxiList)
        mp.put(map, currentCompany, value)
    else:
        entry["value"][0][0] += 1
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
    listaRetorno = lt.newList('ARRAY_LIST', cmpfunction=compareElements)
    listaTuplas = ms.valueSet(map)
    taxisIterator = it.newIterator(listaTuplas)
    while it.hasNext(taxisIterator):
        valor = it.next(taxisIterator)
        listaId = valor[1]
        idsIterator = it.newIterator(listaId)
        while it.hasNext(idsIterator):
            taxiId = it.next(idsIterator)
            if (lt.isPresent(listaRetorno, taxiId) == 0):
                lt.addLast(listaRetorno, taxiId)
    return lt.size(listaRetorno)



def totalCompanies(map):
    """
    Número total de compañías con al menos 1 taxi afiliado.
    Se ignoran los taxis registrados como 'Independet Owner'
    """
    exc = mp.get(map, 'Independet Owner')
    if (exc is None):
        return int(mp.size(map))
    else:
        return (int(mp.size(map)) - 1)


def topCompaniesTaxis(map, topNumber):
    """
    Heap --> maxPQ de compañías por taxis afiliados
    """

    maxPQ = mpq.newMinPQ(cmpfunction=comparePQs)
    diccionario = {}
    listaComparativa = []
    contTop = 1
    listaTuplas = ms.valueSet(map)
    taxisIterator = it.newIterator(listaTuplas)


    while it.hasNext(taxisIterator):
        valor = it.next(taxisIterator)
        listaId = valor[1]
        valorCompany = lt.size(listaId)
        mpq.insert(maxPQ, valorCompany)


    while (contTop <= topNumber):
        contTop += 1
        maximo = mpq.min(maxPQ)
        mpq.delMin(maxPQ)
        listaComparativa.append(maximo)


    listaLlaves = mp.keySet(map)
    companiesIterator = it.newIterator(listaLlaves)
    tuplas = mp.valueSet(listaTuplas)
    valueIterator = it.newIterator(tuplas)


    contador = 0
    while it.hasNext(companiesIterator):
        llave = it.next(companiesIterator)
        tuplaLlave = it.next(valueIterator)
        listaTaxis = tuplaLlave[1]
        valorLlave = lt.size(listaTaxis)
        for elemento in listaComparativa:
            if (valorLlave == elemento) and (contador < topNumber):
                if (llave not in diccionario) and (llave is not "Independent Owner" ):
                    diccionario[valorLlave] = [llave]
                    contador += 1
                else:
                    diccionario[valorLlave].append(llave)
                    contador += 1

    return diccionario


def topCompaniesServices(map, topNumber):
    """
    Heap --> maxPQ de compañías por servicios prestados
    """

    maxPQ = mpq.newMinPQ(cmpfunction=comparePQs)
    diccionario = {}
    listaComparativa = []
    contTop = 1
    listaTuplas = ms.valueSet(map)
    taxisIterator = it.newIterator(listaTuplas)


    while it.hasNext(taxisIterator):
        valor = it.next(taxisIterator)
        valorCompany = valor[0]
        mpq.insert(maxPQ, valorCompany)


    while (contTop <= topNumber):
        contTop += 1
        maximo = mpq.min(maxPQ)
        mpq.delMin(maxPQ)
        listaComparativa.append(maximo)


    listaLlaves = mp.keySet(map)
    companiesIterator = it.newIterator(listaLlaves)
    tuplas = mp.valueSet(listaTuplas)
    valueIterator = it.newIterator(tuplas)


    contador = 0
    while it.hasNext(companiesIterator):
        llave = it.next(companiesIterator)
        tuplaLlave = it.next(valueIterator)
        valorLlave = tuplaLlave[0]

        for elemento in listaComparativa:
            if (valorLlave == elemento) and (contador < topNumber):
                if (llave not in diccionario) and (llave is not "Independent Owner" ):
                    diccionario[valorLlave] = [llave]
                    contador += 1
                else:
                    diccionario[valorLlave].append(llave)
                    contador += 1

    return diccionario
    

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


def comparePQs(pq1, pq2):
    if (pq1==pq2):
        return 0
    elif (pq1 < pq2):
        return 1
    else:
        return -1