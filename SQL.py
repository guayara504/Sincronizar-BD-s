import mysql.connector as sql
import msvcrt
import time
from Ruta import *

ruta = rutaCiudad()
dia = time.strftime("%d")
mes = time.strftime("%m")
ano = time.strftime("%Y")
ruta.crear_carpetas(dia=dia, mes=mes)


conexion1 = sql.connect(
            host = "192.168.0.19", 
            user = "rpino40", 
            passwd = "Z0rt3kw3b#",
            database = "zortekv3")
conexion2 = sql.connect(
                    host = "92.204.136.43", 
                    user = "aluna", 
                    passwd = "R3djud1c1al!!",
                    database = "redjudicial")

fecha = time.strftime("%Y-%m-%d")
fechaSegundos = time.strftime("%d-%m-%Y-(%H-%M-%S)")
print (fecha)


print("-"*15)
print("GENERADOR SQL")
cursor1 = conexion1.cursor()
cursor1.execute(f"select * from z04_estado WHERE fecha_ingreso = '{fecha}' AND sincronizado = 0")
consultasBD  = [item for item in cursor1.fetchall()]
if len(consultasBD) == 0:
    print("No hay procesos")
else:
    id_z04 = []
    consultatxt = []
    updateRemotaInsert = []
    updateRemotaUpdate = []
    updateRemotaInsert.append("INSERT INTO z04_estado (z01_radicacion_juzgado, z01_radicacion_z01_radicacion, demandante, demandado, notificacion, fecha_notificacion, clase_proceso, folio, cuaderno, ciudad) VALUES ")
    for consultaBD in consultasBD:  
      id_z04.append(consultaBD[0])
      juzgado = consultaBD[1]
      radicacion = consultaBD[2]
      demandante = consultaBD[3] 
      demandado = consultaBD[4]
      notificacion = consultaBD[5]
      fecha_notificacion = consultaBD[6]
      clase_proceso = consultaBD[7]
      folio = consultaBD[8]
      cuaderno = consultaBD[9]
      ciudad = consultaBD[13]
      
      consultatxt.append(f"""INSERT INTO z04_estado (z01_radicacion_juzgado, z01_radicacion_z01_radicacion, demandante, demandado, notificacion, fecha_notificacion, clase_proceso, folio, cuaderno, ciudad) VALUES ('{juzgado}','{radicacion}', '{demandante}', '{demandado}', '{notificacion}','{fecha_notificacion}','{clase_proceso}','{folio}','{cuaderno}','{ciudad}')
UPDATE z01_radicacion_has_z02_abogado, z02_abogado SET z01_radicacion_has_z02_abogado.leido = 1 WHERE z01_radicacion_has_z02_abogado.z01_radicacion_z01_radicacion = '{radicacion}' AND z01_radicacion_has_z02_abogado.ciudad='{ciudad}' AND z01_radicacion_has_z02_abogado.z01_radicacion_juzgado = '{juzgado}' AND z01_radicacion_has_z02_abogado.z02_abogado_idcedula_z02=z02_abogado.idcedula_z02 AND z02_abogado.estado=1""")


      updateRemotaInsert.append(f"('{juzgado}','{radicacion}', '{demandante}', '{demandado}', '{notificacion}','{fecha_notificacion}','{clase_proceso}','{folio}','{cuaderno}','{ciudad}'),")
      updateRemotaUpdate.append(f"UPDATE z01_radicacion_has_z02_abogado, z02_abogado SET z01_radicacion_has_z02_abogado.leido = 1 WHERE z01_radicacion_has_z02_abogado.z01_radicacion_z01_radicacion = '{radicacion}' AND z01_radicacion_has_z02_abogado.ciudad='{ciudad}' AND z01_radicacion_has_z02_abogado.z01_radicacion_juzgado = '{juzgado}' AND z01_radicacion_has_z02_abogado.z02_abogado_idcedula_z02=z02_abogado.idcedula_z02 AND z02_abogado.estado=1")      
with open(f'.\\{ruta.dife_fecha()}\\{dia}\\{fechaSegundos}.txt','w') as temp_file:
    for item in consultatxt:
        temp_file.write("%s\n" % item)
file = open(f'.\\{ruta.dife_fecha()}\\{dia}\\{fechaSegundos}.txt', 'r')
print(file.read())
       
id_z04 =tuple(id_z04)
print("-"*15)
print(id_z04,"---",len(id_z04))


cursor1.execute(f"UPDATE z04_estado SET sincronizado = 1 WHERE id_z04_estado  IN {id_z04}")
cursor1.close()



print("\nSubiendo\n----------------")
print("Insertando Lineas...")

cursor2 = conexion2.cursor()
updateRemotaInsert = "".join(updateRemotaInsert)
updateRemotaInsert = updateRemotaInsert[:-1]
cursor2.execute(updateRemotaInsert)
print("¡Lineas Insertadas!")
n=0
print("Ejecutando UPDATE")
for consulta in updateRemotaUpdate:
    n+=1
    print("Proceso: ",n)
    cursor2.execute(consulta)
print("UPDATE Ejecutado\n-----------------\n")




print("--Consulta hecha con exito--")
print("-"*15)
print("--Presione una tecla para cerrar--")
msvcrt.getch()
