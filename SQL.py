import mysql.connector as sql
import msvcrt
import time
from Ruta import *
import colorama
from tabulate import tabulate
ruta = rutaCiudad()
dia = time.strftime("%d")
mes = time.strftime("%m")
ano = time.strftime("%Y")
ruta.crear_carpetas(dia=dia, mes=mes)
colorama.init()

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
print (colorama.Fore.YELLOW+"\n",fecha)


print(colorama.Fore.RESET+"-"*37)
print(colorama.Fore.CYAN+"\tGENERADOR SQL")
cursor1 = conexion1.cursor()
cursor1.execute(f"select * from z04_estado WHERE fecha_ingreso = '{fecha}' AND sincronizado = 0")
consultasBD  = [item for item in cursor1.fetchall()]
if len(consultasBD) == 0:
    print(colorama.Fore.YELLOW+"\nNo hay procesos insertados")

else:
        id_z04 = []
        consultatxt = []
        updateRemotaInsert = []
        updateRemotaUpdate = []
        updateRemotaInsert.append("INSERT INTO z04_estado (z01_radicacion_juzgado, z01_radicacion_z01_radicacion, demandante, demandado, notificacion, fecha_notificacion, clase_proceso, folio, cuaderno, ciudad) VALUES ")
        updateRemotaUpdate.append("UPDATE z01_radicacion_has_z02_abogado, z02_abogado SET z01_radicacion_has_z02_abogado.leido = 1 WHERE ")
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
            updateRemotaUpdate.append(f"(z01_radicacion_has_z02_abogado.z01_radicacion_z01_radicacion = '{radicacion}' AND z01_radicacion_has_z02_abogado.ciudad='{ciudad}' AND z01_radicacion_has_z02_abogado.z01_radicacion_juzgado = '{juzgado}' AND z01_radicacion_has_z02_abogado.z02_abogado_idcedula_z02=z02_abogado.idcedula_z02 AND z02_abogado.estado=1) OR ")      
        with open(f'.\\{ruta.dife_fecha()}\\{dia}\\{fechaSegundos}.txt','w') as temp_file:
            for item in consultatxt:
                temp_file.write("%s\n" % item)
        file = open(f'.\\{ruta.dife_fecha()}\\{dia}\\{fechaSegundos}.txt', 'r')
            
        id_z04 =tuple(id_z04)
        print(colorama.Fore.RESET+"-"*37)
        print(colorama.Fore.GREEN+"Lineas Consultadas: ",len(id_z04))
        print(colorama.Fore.RESET+"-"*37)


        cursor1.execute(f"UPDATE z04_estado SET sincronizado = 1 WHERE id_z04_estado  IN {id_z04}")
        cursor1.close()



        print(colorama.Fore.CYAN+"\tSINCRONIZANDO")
        print(colorama.Fore.RESET+"-"*37)
        print(colorama.Fore.GREEN+"Insertando Lineas:")
        print(colorama.Fore.RESET+"-"*37)

        cursor2 = conexion2.cursor()
        updateRemotaInsert = "".join(updateRemotaInsert)
        updateRemotaInsert = updateRemotaInsert[:-1]

        updateRemotaUpdate = "".join(updateRemotaUpdate)
        updateRemotaUpdate = updateRemotaUpdate[:-3]

        cursor2.execute(updateRemotaInsert)

        print(colorama.Fore.YELLOW+"¡Lineas Insertadas!")
        print(colorama.Fore.RESET+"-"*37)
        print(colorama.Fore.GREEN+"Ejecutando UPDATE:")
        print(colorama.Fore.RESET+"-"*37)
        cursor2.execute(updateRemotaUpdate)
        print(colorama.Fore.YELLOW+"¡Tablas Actualizadas!")
        print(colorama.Fore.RESET+"-"*37)




        print(colorama.Fore.GREEN+"Sincronización hecha correctamente",colorama.Fore.YELLOW+" \2")
        print(colorama.Fore.RESET+"-"*37)

print(colorama.Fore.GREEN+"\nEjecutando Diferencia BD's:")

cursor1 = conexion1.cursor()
cursor1.execute(f"SELECT COUNT(id_z04_estado) FROM z04_estado WHERE fecha_notificacion = CURDATE()")
totalLocal  = [item for item in cursor1.fetchall()]
cursor1.close()

cursor2 = conexion2.cursor()
cursor2.execute(f"SELECT COUNT(id_z04_estado) FROM z04_estado WHERE fecha_notificacion = CURDATE()")
totalRemota  = [item for item in cursor2.fetchall()]
cursor2.close()

diferencia = int(totalLocal[0][0]) - (totalRemota[0][0])

dif = [[totalRemota[0][0],totalLocal[0][0],diferencia]]
header = ["TotalRemota","TotalLocal","Diferencia"]
print(colorama.Fore.YELLOW+"\n",tabulate(dif,header,tablefmt='fancy_grid'))


print(colorama.Fore.CYAN+"Presione una tecla para cerrar")
msvcrt.getch()
