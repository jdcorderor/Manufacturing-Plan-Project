from Modulo1 import *
from Modulo2 import *

# Módulo 1:

mbacklogalum, mbacklogcob, mexistencia, vbacklogalum, vbacklogcob, vexistencia = ImportData()

vexistencia = SupRep(vexistencia)
vbacklogcob = SupRep(vbacklogcob)
vbacklogalum = SupRep(vbacklogalum)

mbacklogcob = CompMat1(vbacklogcob, mbacklogcob)
mbacklogalum = CompMat1(vbacklogalum, mbacklogalum)

mexistencia = CompMat2(vexistencia, mexistencia)

CupperPlan(mbacklogcob, vexistencia, mexistencia)

AluminiumPlan(mbacklogalum, vexistencia, mexistencia)

# Módulo 2:

filename = input("Inserte el nombre del archivo correspondiente al Ventas Today exportado por SQL Server (incluya la terminación del formato de texto .txt): ")
matrizventas, vectorcodigos = datatransfer(filename)

monthlydates = datelimits(matrizventas)

codigos = sup(vectorcodigos)

dataprocessing(codigos, matrizventas, monthlydates)

maxminps = parameters("Parámetros Sugeridos.txt")
maxminif = parameters("Items Flotantes.txt")  

averageps = average("Parámetros Sugeridos.txt")
averageif = average("Items Flotantes.txt") 

CupperPlanFinal("Plan de Necesidades - Cobre.txt", maxminps, averageps)
AluminiumPlanFinal("Plan de Necesidades - Aluminio.txt", maxminps, averageps)
AdditionalPlanFinal(maxminif, averageif, matrizventas, codigos)