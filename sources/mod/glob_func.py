'''
Trtamos las funciones globales o para reemplazar la carga de datos que antes eran globales.
'''

import mod.mdb as mdb
import mod.vars as mi_vars

# Se encarga de actualizar las listas globales de LINEA, TIPO, INTERIOR y LINEANUM. Tener en cuenta que se quitó la posibilidad de marcar que uno de esos concepto 
    # está desactivado
def Act_Listas_Globales():
    mi_vars.LINEA = []
    mi_vars.TIPO = []
    mi_vars.INTERIOR = []
    mi_vars.LINEANUM = []
    mi_vars.LINEAORDENADA = []

    # LISTA LINEA Y LINEANUM
    Datos = ['0']
    fila = mdb.Dev_Reg_Prod_Config('Tabla', 'Linea')
    for pos in fila:
        Datos[0] = pos[2]
    if Datos[0] != '0':
        mi_vars.LINEA.append("-")
        mi_vars.LINEANUM.append(0)
        Contador = 0
        while Contador < Datos[0]:
            Fila = mdb.Reg_Un_param(mi_vars.BaseDeDatos, 'Linea', "Orden", Contador + 1)
            for pos in Fila:
                mi_vars.LINEA.append(pos[3])
                mi_vars.LINEANUM.append(pos[0])
            Contador += 1

        # Cargamos una lista LISTAORDENADA de todas las líneas según su orden real en la base de datos, y no según su orden en función a su uso.
        Contador = 0
        mi_vars.LINEAORDENADA.append("-")
        while Contador < Datos[0]:
            Fila = mdb.Reg_Un_param(mi_vars.BaseDeDatos, 'Linea', "ID", Contador + 1)
            for pos in Fila:
                mi_vars.LINEAORDENADA.append(pos[3])
            Contador += 1

    # LISTA TIPO
    Datos = ['0']
    fila = mdb.Dev_Reg_Prod_Config('Tabla', 'Tipo')
    for pos in fila:
        Datos[0] = pos[2]
    if Datos[0] != '0':
        Tabla = mdb.Dev_Tabla(mi_vars.BaseDeDatos, 'Tipo')
        mi_vars.TIPO.append("-")
        for pos in Tabla:
            mi_vars.TIPO.append(pos[3])
    
    # LISTA INTERIOR
    Datos = ['0']
    fila = mdb.Dev_Reg_Prod_Config("Tabla", "Interior")
    for pos in fila:
        Datos[0] = pos[2]
    if Datos[0] != '0':
        Tabla = mdb.Dev_Tabla(mi_vars.BaseDeDatos, 'Interior')
        mi_vars.INTERIOR.append("-")
        for pos in Tabla:
            mi_vars.INTERIOR.append(pos[3])
    
    # LISTA LISTA_TIPOS_IMAGENES
    Tope = 0
    Registro = mdb.Reg_Un_param(mi_vars.BaseDeDatos, "Config", "Tabla", "Imagen_Tipo")
    for i in Registro:
        Tope = i[2]
    cont = 0
    if Tope > 0:
        mi_vars.LISTA_TIPOS_IMAGENES.append("Seleccione Tipo de imgen")
        while cont < Tope:
            Tabla = mdb.Dev_Tabla(mi_vars.BaseDeDatos, "Image_Tipo")
            for val in Tabla:
                if cont + 1 == val[1]:
                    mi_vars.LISTA_TIPOS_IMAGENES.append(val[2])
                    break
            cont += 1
    else:
        mi_vars.LISTA_TIPOS_IMAGENES.append("-")
