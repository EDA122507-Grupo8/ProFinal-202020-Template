# ==============================
#Librerías
# ==============================


from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import list as lt

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
    currentCompany = trip['company']
    if (currentCompany == ''):
        currentCompany = '"Independent Owner"'
    entry = mp.get(map, currentCompany)
    if (entry is None):
        
        mp.put(map, currentCompany, (valueForCompany(map, trip)))
    else:
        entry = me.getValue(entry)
        addNewInfo(entry, trip)
    return map


def valueForCompany(map, trip):
    serviceCont = 1
    taxiList = lt.newList(datastructure='ARRAY_LIST',
                            cmpfunction=compareElements)
    lt.addLast(taxiList,trip['taxi_id'])
    return (serviceCont, taxiList)


def addNewInfo(entry, trip):
    entry[0] += 1
    if ((lt.isPresent(entry[1],trip['taxi_id'])) == 0):
        lt.addLast(entry[1], trip['taxi_id'])
    return entry

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