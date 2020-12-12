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

def loadCompanies(map, trip):
    currentCompany = trip['company']
    if (currentCompany == ''):
        currentCompany = '"Independent Owner"'
    entry = mp.get(map, currentCompany)
    if (entry is None):
        mp.put(map, currentCompany, (valueForCompany(map, trip, currentCompany)))
    else:
        entry=me.getValue(entry)
        addNewInfo(entry, trip)
    return map


def valueForCompany(map, trip, company):
    serviceList = lt.newList(datastructure='ARRAY_LIST')
    taxiList = lt.newList(datastructure='ARRAY_LIST')
    service = trip['trip_id']
    taxi = trip['taxi_id']
    info_company = ((lt.addLast(serviceList,trip)),(lt.addLast(taxiList,taxi)))
    return info_company


def addNewInfo(entry, trip):
    lt.addLast(entry['services'], trip['trip_id'])
    if (lt.isPresent(entry['taxis'],trip['taxi_id'])):
        lt.addLast(entry['taxis'], trip['taxi_id'])
    return entry

# ==============================
#Compare functions
# ==============================


def compareCompanies(company1, company2):
    if (company1 == company2):
        return 0
    else:
        return 1
