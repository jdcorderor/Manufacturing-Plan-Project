# Función 1: Genera el arreglo de datos brutos.

def datatransfer(ref):
    archivo = open(ref, "r")
    cant = len(archivo.readlines())
    archivo.seek(0)
    mv = [[None] * 7 for i in range (cant)]
    vc = [int for i in range (cant)]
    f = 0
    for registro in archivo:
        campos = registro.split(";")
        vc[f] = int(campos[0])
        mv[f][0] = int(campos[0]) #Code
        mv[f][1] = campos[1] #Description
        mv[f][2] = float(campos[2].replace(',', '.')) #Quantity
        mv[f][3] = campos[3] #UM
        mv[f][4] = int(campos[4]) #Date
        mv[f][5] = campos[5] #Warehouse
        mv[f][6] = float(campos[6].replace(",", ".")) #Metal
        f += 1
    archivo.close()
    return mv, vc

# Función 2: Determina las fechas límites.

def datelimits(mv):
    datemax = mv[0][4]
    datemin = mv[0][4]
    for f in range(len(mv)-1):
        if mv[f+1][4] > datemax:
            datemax = mv[f+1][4]
        elif mv[f+1][4] < datemin:
            datemin = mv[f+1][4]
    datemin = (datemin//100) * 100
    datemax = ((datemax//100) * 100 ) + 100
    lista = []
    date = datemin
    if (datemin//10000) == (datemax//10000):
        while date <= datemax:
            lista.append(date)
            date += 100
    elif (datemin//10000) != (datemax//10000):
        while date <= (((date//10000) * 10000) + 1200):
            lista.append(date)
            date += 100
        date = ((date//10000) * 10000) + 10100
        while date <= datemax:
            lista.append(date)
            date += 100
    return lista

# Función 3: Suprime las duplicaciones.

def sup(v):
    lista = []
    for element in v:
        if element not in lista:
            lista.append(element)
    return lista

# Función 4: Adiciona los contenidos de metal por metro.

def addmetalcontent(m):
    # Backlog Aluminio:
    archivo1 = open("Backlog Aluminio.txt", "r")
    cant1 = len(archivo1.readlines())
    archivo1.seek(0)
    m1 = [[None] * 2 for i in range (cant1)]
    v1 = [int for i in range (cant1)]
    f1 = 0
    for registro in archivo1:
        campos = registro.split(";")
        v1[f1] = int(campos[0])
        m1[f1][0] = int(campos[0])
        m1[f1][1] = float(campos[5].replace(",", "."))
        f1 += 1
    v1 = sup(v1)
    mf1 = [[None] * 2 for i in range (len(v1))]
    k1 = 0
    for element in v1:
        temp1 = element
        mf1[k1][0] = temp1
        for j1 in range (len(m1)):
            if m1[j1][0] == temp1:
                mf1[k1][1] = m1[j1][1]
        k1 += 1 
    archivo1.close()       
    # Backlog Cobre:   
    archivo2 = open("Backlog Cobre.txt", "r")
    cant2 = len(archivo2.readlines())
    archivo2.seek(0)
    m2 = [[None] * 2 for i in range (cant2)]
    v2 = [int for i in range (cant2)]
    f2 = 0
    for registro in archivo2:
        campos = registro.split(";")
        v2[f2] = int(campos[0])
        m2[f2][0] = int(campos[0])
        m2[f2][1] = float(campos[5].replace(",", "."))
        f2 += 1
    v2 = sup(v2)
    mf2 = [[None] * 2 for i in range (len(v2))]
    k2 = 0
    for element in v2:
        temp2 = element
        mf2[k2][0] = temp2
        for j2 in range (len(m2)):
            if m2[j2][0] == temp2:
                mf2[k2][1] = m2[j2][1]
        k2 += 1
        archivo2.close()
    # Totalizado:
    lista = []
    for fila in range (len(mf1)):
        lista.append(mf1[fila])
    for fila in range (len(mf2)):
        lista.append(mf2[fila])
    # Cruzar con la matriz filtrada:
    for p in range (len(m)):
        code = m[p][0]
        for w in range (len(lista)):
            if lista[w][0] == code:
                m[p].append(lista[w][1])
    return m   

# Función 5.1: Compila las matrices definitivas mensuales en un archivo de texto independiente (in Backlog).

def file2compiler(m, j):
    if j == 0:
        archivo = open("Parámetros Sugeridos.txt", "w")
        for f in range (len(m)):
            line = "{0:1d};{1:1};{2:1.2f};{3:1};{4:1};{5:1}\n".format(m[f][0], m[f][1], m[f][2], m[f][3], m[f][4], m[f][5])
            archivo.write(line)
        archivo.close()
    elif j > 0:
        archivo = open("Parámetros Sugeridos.txt", "a")
        for f in range (len(m)):
            line = "{0:1d};{1:1};{2:1.2f};{3:1};{4:1};{5:1}\n".format(m[f][0], m[f][1], m[f][2], m[f][3], m[f][4], m[f][5])
            archivo.write(line)
        archivo.close()
    return

# Función 5.2: Compila las matrices definitivas mensuales en un archivo de texto independiente (not in Backlog).

def file3compiler(m, j):
    if j == 0:
        archivo = open("Items Flotantes.txt", "w")
        for f in range (len(m)):
            line = "{0:1d};{1:1};{2:1.2f};{3:1};{4:1};{5:1}\n".format(m[f][0], m[f][1], m[f][2], m[f][3], m[f][4], m[f][5])
            archivo.write(line)
        archivo.close()
    elif j > 0:
        archivo = open("Items Flotantes.txt", "a")
        for f in range (len(m)):
            line = "{0:1d};{1:1};{2:1.2f};{3:1};{4:1};{5:1}\n".format(m[f][0], m[f][1], m[f][2], m[f][3], m[f][4], m[f][5])
            archivo.write(line)
        archivo.close()
    return

# Función 6: Acumula las ventas filtradas por código del producto y distribuidas mensualmente por fecha de facturación.

def dataprocessing(vc, mv, vf):
    a = 0
    while a < ((len(vf))-1):
        low = vf[a]
        high = vf[a+1]
        lista = [] #All Content
        lc = [] #Code
        for f in range (len(mv)):
            if (mv[f][4] > low) and (mv[f][4] < high):
                lista.append(mv[f])
                lc.append(mv[f][0])
        lista = addmetalcontent(lista)
        lc = sup(lc)
        contA = 0
        contB = 0
        lt = []
        for element in lc:
            for i in range (len(lista)):
                if lista[i][0] == element:
                    if len(lista[i]) == 8 and (lista[i][5] == "AC" or lista[i][5] == "AA") and lista[i][2] > 0:
                        if element not in lt:
                            lt.append(element)
                            contA += 1
            for i in range (len(lista)):
                if lista[i][0] == element:
                    if len(lista[i]) == 7 and (lista[i][5] == "AC" or lista[i][5] == "AA") and lista [i][2] > 0:
                        if element not in lt:
                            lt.append(element)
                            contB += 1
        md2 = [[None] * 6 for i in range (contA)]
        md3 = [[None] * 6 for i in range (contB)]
        if contA > 0:
            j2 = 0
            for element in lc:
                temp = element
                if j2 < contA:
                    md2[j2][2] = 0
                    for k in range (len(lista)):
                        if lista[k][0] == element:
                            if len(lista[k]) == 8:
                                if lista[k][2] > 0:
                                    if (lista[k][3].upper() == "M" or lista[k][3].upper() == "R1" or lista[k][3].upper() == "R2" or lista[k][3].upper() == "R5") and (lista[k][5] == "AC" or lista[k][5] == "AA"):
                                        md2[j2][0] = element #Code
                                        md2[j2][1] = lista[k][1] #Description
                                        md2[j2][3] = "M" #UM
                                        md2[j2][4] = str(low) + " to " + str(high) #Date
                                        md2[j2][5] = lista[k][5] #Warehouse
                                        md2[j2][2] += lista[k][2] #QuantityM
                                    elif lista[k][3].upper() == "KG" and (lista[k][5] == "AC" or lista[k][5] == "AA"):
                                        md2[j2][0] = element #Code
                                        md2[j2][1] = lista[k][1] #Description
                                        md2[j2][3] = "M" #UM
                                        md2[j2][4] = str(low) + " to " + str(high) #Date
                                        md2[j2][5] = lista[k][5] #Warehouse
                                        md2[j2][2] += (lista[k][2] / lista[k][6]) #QuantityKG
                    if j2 < contA:
                        if md2[j2][0] != None:
                            j2 += 1
        if contB > 0:
            j3 = 0
            for element in lc:
                temp = element
                if j3 < contB:
                    md3[j3][2] = 0
                    for k in range (len(lista)):
                        if lista[k][0] == element:
                            if len(lista[k]) == 7:
                                if (lista[k][3].upper() == "M" or lista[k][3].upper() == "R1" or lista[k][3].upper() == "R2" or lista[k][3].upper() == "R5") and (lista[k][5] == "AC" or lista[k][5] == "AA"):
                                    md3[j3][0] = element #Code
                                    md3[j3][1] = lista[k][1] #Description
                                    md3[j3][3] = "KG" #UM
                                    md3[j3][4] = str(low) + " to " + str(high) #Date
                                    md3[j3][5] = lista[k][5] #Warehouse
                                    md3[j3][2] += lista[k][6] #QuantityM
                                elif lista[k][3].upper() == "KG" and (lista[k][5] == "AC" or lista[k][5] == "AA"):
                                    md3[j3][0] = element #Code
                                    md3[j3][1] = lista[k][1] #Description
                                    md3[j3][3] = "KG" #UM
                                    md3[j3][4] = str(low) + " to " + str(high) #Date
                                    md3[j3][5] = lista[k][5] #Warehouse
                                    md3[j3][2] += lista[k][2] #QuantityKG
                    if j3 < contB:
                        if md3[j3][0] != None:
                            j3 += 1
        file2compiler(md2, a)
        file3compiler(md3, a)
        a += 1

# Función 7: Determina máximos y mínimos.

def parameters(ref):
    archivo = open(ref, "r")
    cant = len(archivo.readlines())
    m = [[None] * 6 for i in range (cant)]
    v = [int for i in range (cant)]
    archivo.seek(0)
    f = 0
    for registro in archivo:
        campos = registro.split(";")
        v[f] = int(campos[0])
        m[f][0] = int(campos[0])
        m[f][1] = campos[1]
        m[f][2] = float(campos[2])
        m[f][3] = campos[3]
        m[f][4] = campos[4]
        m[f][5] = campos[5]
        f += 1
    v = sup(v)
    mf = [[None] * 4 for i in range (len(v))]
    p = 0
    for element in v:
        band = 0
        j = 0
        while band == 0:
            if m[j][0] == element:
                max = m[j][2]
                min = m[j][2]
                unit = m[j][3]
                band = 1
            else:
                j +=1
        while band == 1:
            for k in range (len(m)):
                if m[k][0] == element:
                    if m[k][2] > max:
                        max = m[k][2]
                    elif m[k][2] < min:
                        min = m[k][2]
            band = 2
        mf[p][0] = element
        mf[p][1] = min
        mf[p][2] = max
        mf[p][3] = unit
        p += 1
    archivo.close()
    return mf
    
# Función 7: Determina promedios.

def average(ref):
    archivo = open(ref, "r")
    cant = len(archivo.readlines())
    m = [[None] * 6 for i in range (cant)]
    v = [int for i in range (cant)]
    archivo.seek(0)
    f = 0
    for registro in archivo:
        campos = registro.split(";")
        v[f] = int(campos[0])
        m[f][0] = int(campos[0])
        m[f][1] = campos[1]
        m[f][2] = float(campos[2])
        m[f][3] = campos[3]
        m[f][4] = campos[4]
        m[f][5] = campos[5]
        f += 1
    v = sup(v)
    mf = [[None] * 3 for i in range (len(v))]
    p = 0
    for element in v:
        cont = 0
        total = 0
        for j in range (len(m)):
            if m[j][0] == element:
                total += m[j][2]
                cont += 1
                unit = m[j][3]
        mf[p][0] = element
        mf[p][1] = total/cont
        mf[p][1] = round(mf[p][1], 2)
        mf[p][2] = unit
        p += 1
    archivo.close()
    return mf

# Función 8: Fusiona la data en el Plan de Necesidades de la Planta de Cobre:

def CupperPlanFinal(ref, maxmin, prom):
    archivo = open(ref, "r")
    cant = len(archivo.readlines())
    m = [[None] * 12 for i in range (cant)]
    archivo.seek(0)
    f = 0
    for registro in archivo:
        campos = registro.split(";")
        m[f][0] = int(campos[0]) #Code
        m[f][1] = campos[1] #Description
        m[f][2] = campos[2] #ContentPerMeter
        m[f][3] = campos[3] #Quantity
        m[f][4] = campos[4] #UM
        m[f][5] = campos[5].replace("\n", "") #TotalMetal
        f += 1
    archivo.close()
    plan = open("Plan de Necesidades - Cobre (Suggested).txt", "w")
    line = "Código BPCS;Descripción;Contenido de Metal;Cantidad;U/M;Total Metal;Mínimo Histórico;U/M;Promedio Histórico;U/M;Máximo Histórico;U/M\n"
    plan.write(line)
    for k in range (len(m)):
        temp = m[k][0]
        for j in range (len(maxmin)):
            if int(maxmin[j][0]) == temp:
                m[k][6] = maxmin[j][1]
                m[k][7] = maxmin[j][3]
                m[k][10] = maxmin[j][2]
                m[k][11] = maxmin[j][3]
        for p in range (len(prom)):
            if int(prom[p][0]) == temp:
                m[k][8] = prom[p][1]
                m[k][9] = prom[p][2]
    for h in range (len(m)):
        for c in range (12):
            if (c%2 == 0) and (m[h][c] == None):
                m[h][c] = 0
            elif (c%2 != 0) and (m[h][c] == None):
                m[h][c] = m[h][4]
    for l in range (len(m)):
        line = ("{0:1};{1:1};{2:1};{3:2};{4:1};{5:1};{6:1};{7:1};{8:1};{9:1};{10:1};{11:1}\n".format(m[l][0], m[l][1], m[l][2], m[l][3], m[l][4], m[l][5], str(m[l][6]).replace(".", ","), m[l][7], str(m[l][8]).replace(".", ","), m[l][9], str(m[l][10]).replace(".", ","), m[l][11]))
        plan.write(line)
    plan.close
    
# Función 9: Fusiona la data en el Plan de Necesidades de la Planta de Aluminio:

def AluminiumPlanFinal(ref, maxmin, prom):
    archivo = open(ref, "r")
    cant = len(archivo.readlines())
    m = [[None] * 12 for i in range (cant)]
    archivo.seek(0)
    f = 0
    for registro in archivo:
        campos = registro.split(";")
        m[f][0] = int(campos[0]) #Code
        m[f][1] = campos[1] #Description
        m[f][2] = campos[2] #ContentPerMeter
        m[f][3] = campos[3] #Quantity
        m[f][4] = campos[4] #UM
        m[f][5] = campos[5].replace("\n", "") #TotalMetal
        f += 1
    archivo.close()
    plan = open("Plan de Necesidades - Aluminio (Suggested).txt", "w")
    line = "Código BPCS;Descripción;Contenido de Metal;Cantidad;U/M;Total Metal;Mínimo Histórico;U/M;Promedio Histórico;U/M;Máximo Histórico;U/M\n"
    plan.write(line)
    for k in range (len(m)):
        temp = m[k][0]
        for j in range (len(maxmin)):
            if int(maxmin[j][0]) == temp:
                m[k][6] = maxmin[j][1]
                m[k][7] = maxmin[j][3]
                m[k][10] = maxmin[j][2]
                m[k][11] = maxmin[j][3]
        for p in range (len(prom)):
            if int(prom[p][0]) == temp:
                m[k][8] = prom[p][1]
                m[k][9] = prom[p][2]
    for h in range (len(m)):
        for c in range (12):
            if (c%2 == 0) and (m[h][c] == None):
                m[h][c] = 0
            elif (c%2 != 0) and (m[h][c] == None):
                m[h][c] = m[h][4]
    for l in range (len(m)):
        line = ("{0:1};{1:1};{2:1};{3:2};{4:1};{5:1};{6:1};{7:1};{8:1};{9:1};{10:1};{11:1}\n".format(m[l][0], m[l][1], m[l][2], m[l][3], m[l][4], m[l][5], str(m[l][6]).replace(".", ","), m[l][7], str(m[l][8]).replace(".", ","), m[l][9], str(m[l][10]).replace(".", ","), m[l][11]))
        plan.write(line)
    plan.close

# Función 10: Plan de Items Flotantes:

def AdditionalPlanFinal(maxmin, prom, mv, vc):
    md = [[None] * 2 for i in range (len(vc))]
    t = 0
    for element in vc:
        for f in range (len(mv)):
            if mv[f][0] == element:
                md[t][0] = element
                md[t][1] = mv[f][1]
        t += 1
    cant = len(prom)
    mf = [[None] * 8 for i in range (cant)]
    u = 0
    for r in range (len(prom)):
        mf[u][0] = prom[r][0]
        mf[u][2] = maxmin[r][1] #Min
        mf[u][3] = maxmin[r][3] #UM
        mf[u][4] = prom[r][1] #Average
        mf[u][5] = prom[r][2] #UM
        mf[u][6] = maxmin[r][2] #Max
        mf[u][7] = maxmin[r][3] #UM
        for y in range (len(md)):
            if md[y][0] == mf[r][0]:
                mf[u][1] = md[y][1]
        u += 1 
    plan = open("Plan de Necesidades - Items Flotantes (Suggested).txt", "w")
    line = "Código BPCS;Descripción;Mínimo Histórico;U/M;Promedio Histórico;U/M;Máximo Histórico;U/M\n"
    plan.write(line)
    for h in range (len(mf)):
        for c in range (8):
            if (c%2 == 0) and (mf[h][c] == None):
                mf[h][c] = 0
            elif (c%2 != 0) and (mf[h][c] == None):
                mf[h][c] = 0
    for l in range (len(mf)):
        line = ("{0:1};{1:1};{2:1};{3:2};{4:1};{5:1};{6:1};{7:1}\n".format(mf[l][0], mf[l][1], str(mf[l][2]).replace(".", ","), mf[l][3], str(mf[l][4]).replace(".", ","), mf[l][5], str(mf[l][6]).replace(".", ","), mf[l][7]))
        plan.write(line)
    plan.close