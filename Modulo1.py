# Módulo 1: Análisis de Necesidades de Producción.

# Función 1. Transfiere los datos exportados de SQL Server a arreglos matemáticos.

def ImportData():
    backlogaluminio = open(input("Inserte el nombre del archivo correspondiente al Backlog Today (ALUMINIO) exportado por SQL Server (incluya la terminación del formato de texto .txt): "), "r")
    backlogcobre = open(input("Inserte el nombre del archivo correspondiente al Backlog Today (COBRE) exportado por SQL Server (incluya la terminación del formato de texto .txt): "), "r")
    existencia = open(input("Inserte el nombre del archivo correspondiente al Existencia Today exportado por SQL Server (incluya la terminación del formato de texto .txt): "), "r")
    regbacklogaluminio = len(backlogaluminio.readlines())
    backlogaluminio.seek(0)
    matbacklogaluminio = [[None] * 6 for i in range (regbacklogaluminio)]
    vecbacklogaluminio = [int for i in range (regbacklogaluminio)]
    regbacklogcobre = len(backlogcobre.readlines())
    backlogcobre.seek(0)
    matbacklogcobre = [[None] * 6 for i in range (regbacklogcobre)]
    vecbacklogcobre = [int for i in range (regbacklogcobre)]
    regexistencia = len(existencia.readlines())
    existencia.seek(0)
    matexistencia = [[None] * 5 for i in range (regexistencia)]
    vecexistencia = [int for i in range (regexistencia)]
    f = 0
    for registro in backlogaluminio:
        campos = registro.split(";")
        vecbacklogaluminio[f] = int(campos[0])
        matbacklogaluminio[f][0] = int(campos[0])
        matbacklogaluminio[f][1] = campos[1]
        matbacklogaluminio[f][2] = campos[4].replace("\n", "")
        matbacklogaluminio[f][3] = campos[2]
        matbacklogaluminio[f][4] = float(campos[3].replace(",", "."))
        matbacklogaluminio[f][5] = float(campos[5].replace(",", "."))
        f += 1
    f = 0
    for registro in backlogcobre:
        campos = registro.split(";")
        vecbacklogcobre[f] = int(campos[0])
        matbacklogcobre[f][0] = int(campos[0])
        matbacklogcobre[f][1] = campos[1]
        matbacklogcobre[f][2] = campos[4].replace("\n", "")
        matbacklogcobre[f][3] = campos[2]
        matbacklogcobre[f][4] = float(campos[3].replace(",", "."))
        matbacklogcobre[f][5] = float(campos[5].replace(",", "."))
        f += 1
    f = 0
    for registro in existencia:
        campos = registro.split(";")
        vecexistencia[f] = int(campos[0])
        matexistencia[f][0] = int(campos[0])
        matexistencia[f][1] = campos[1]
        matexistencia[f][2] = campos[2]
        matexistencia[f][3] = campos[3]
        matexistencia[f][4] = float(campos[4].replace(",", "."))
        f += 1
    backlogaluminio.close()
    backlogcobre.close()
    existencia.close()
    return matbacklogaluminio, matbacklogcobre, matexistencia, vecbacklogaluminio, vecbacklogcobre, vecexistencia

# Función 1.1: Comprime los datos y suprime repeticiones.

def SupRep(vector):
    lista = []
    for element in vector:
        if element not in lista:
            lista.append(element)
    return lista

# Función 1.2.1: Comprime las matrices de datos del Backlog.

def CompMat1(vector, matriz):
    matriz2 = [[None] * 6 for i in range (len(vector))]
    fila = 0
    for element in vector:
        codigotemporal = element
        matriz2[fila][0] = element
        pending = 0
        for f in range (len(matriz)):
            if matriz[f][0] == codigotemporal:
                matriz2[fila][1] = matriz[f][1]
                matriz2[fila][2] = matriz[f][2]
                matriz2[fila][5] = matriz[f][5]
                matriz2[fila][3] = "M"
                if matriz[f][3].upper() == "M":
                    pending += matriz[f][4]
                elif matriz[f][3].upper() == "KG":
                    pending += (matriz[f][4]/matriz[f][5])
            matriz2[fila][4] = pending
        fila += 1
    return matriz2

# Función 1.2.2: Comprime las matrices de datos de Existencia.

def CompMat2(vector, matriz):
    matriz2 = [[None] * 5 for i in range (len(vector))]
    fila = 0
    for element in vector:
        codigotemporal = element
        matriz2[fila][0] = element
        noasign = 0
        for f in range (len(matriz)):
            if matriz[f][0] == codigotemporal:
                noasign += matriz[f][4]
                matriz2[fila][1] = matriz[f][1]
                matriz2[fila][2] = matriz[f][2]
                matriz2[fila][3] = matriz[f][3]
            matriz2[fila][4] = noasign
        fila += 1
    return matriz2
                
# Función 2: Genera el Plan de Necesidades de la Planta de Cobre.

def CupperPlan(matbacklogcobre, vecexistencia, matexistencia):
    archivocobre = open("Plan de Necesidades - Cobre.txt", "w")
    for f1 in range (len(matbacklogcobre)):
        codigotemporal = matbacklogcobre[f1][0]
        if codigotemporal not in vecexistencia:
            line = ("{0:1};{1:1};{2:1};{3:2};{4:1};{5:1}\n".format(matbacklogcobre[f1][0], matbacklogcobre[f1][1], str(matbacklogcobre[f1][5]).replace(".", ","), str(matbacklogcobre[f1][4]).replace(".", ","), matbacklogcobre[f1][3], str(round(matbacklogcobre[f1][5]*matbacklogcobre[f1][4], 2)).replace(".", ",")))
            archivocobre.write(line)
        else:
            for f2 in range (len(matexistencia)):
                if matexistencia[f2][0] == codigotemporal:
                    target = matbacklogcobre[f1][4] - matexistencia[f2][4]
                    if target < 0:
                        target = 0
                    line = ("{0:1};{1:1};{2:1};{3:2};{4:1};{5:1}\n".format(matbacklogcobre[f1][0], matbacklogcobre[f1][1], str(matbacklogcobre[f1][5]).replace(".", ","), str(target).replace(".", ","), matbacklogcobre[f1][3], str(round(matbacklogcobre[f1][5]*target, 2)).replace(".", ",")))
                    archivocobre.write(line)
    archivocobre.close()

# Función 3: Genera el Plan de Necesidades de la Planta de Aluminio.

def AluminiumPlan(matbacklogaluminio, vecexistencia, matexistencia):
    archivoaluminio = open("Plan de Necesidades - Aluminio.txt", "w")
    for f1 in range (len(matbacklogaluminio)):
        codigotemporal = matbacklogaluminio[f1][0]
        if codigotemporal not in vecexistencia:
            line = ("{0:1};{1:1};{2:1};{3:2};{4:1};{5:1}\n".format(matbacklogaluminio[f1][0], matbacklogaluminio[f1][1], str(matbacklogaluminio[f1][5]).replace(".", ","), str(matbacklogaluminio[f1][4]).replace(".", ","), matbacklogaluminio[f1][3], str(round(matbacklogaluminio[f1][5]*matbacklogaluminio[f1][4], 2)).replace(".", ",")))
            archivoaluminio.write(line)
        else:
            for f2 in range (len(matexistencia)):
                if matexistencia[f2][0] == codigotemporal:
                    target = matbacklogaluminio[f1][4] - matexistencia[f2][4]
                    if target < 0:
                        target = 0
                    line = ("{0:1};{1:1};{2:1};{3:2};{4:1};{5:1}\n".format(matbacklogaluminio[f1][0], matbacklogaluminio[f1][1], str(matbacklogaluminio[f1][5]).replace(".", ","), str(target).replace(".", ","), matbacklogaluminio[f1][3], str(round(matbacklogaluminio[f1][5]*target, 2)).replace(".", ",")))
                    archivoaluminio.write(line)
    archivoaluminio.close()