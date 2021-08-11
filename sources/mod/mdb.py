'''
FUNCIONES PARA EL MANEJO DE LA BASE DE DATOS EN ESSEN
Estas funciones abarcan todo lo necesario para obtener un registro de una base de datos, varios registros, borrar, editar o agregar un registro.

Toda función que comienza con "Dev" indica que devuelve algo. "Act" que actualiza algún valor. "Add" que agrega algún valor. "Eli" que elimina algún valor.
De todas maneras, no queremos eliminar ningún valor practicamente en las base de datos de productos, porque todo lo que afecta a los registros totales no serán eliminados.


ESTRUCTURA DE LA BASE DE DATOS Prod.db
    * Recordar que las imagenes pueden llegar a eliminarse para siempre, por ende, no usamos autoincremental ni nada de eso en la bd.
    Separada en 4 tablas contienen lo siguiente:

    TABLA: Cbo_page1
    8 Columnas
    1  > ID:        Integer Autoincremental
    2  > Activo:    Integer 0= Combo normal, sin novedades.
                            1= Combo que contiene algún producto que no está disponible en para pedidos pero sí tenemos en stock.
                            2= Combo desactivado porque no se consigue algún producto.
    3  > Nro_Ident: Integer Es un número que identifica a la imagen en el montón de imagenes, para una fácil identificación. No podemos guiarnos por el número de ID debido a que
                            ése número no va a tener un orden entre sus imagenes, pudiendo quedar entremezcladas con individuales, etc. Por ende, utilizamos éste valor en
                            conjunción con "Tipo_Cbo", así todos pueden arrancar desde el 1 en adelante.
    4  > Tipo_Cbo:  Integer 1= Combo normal.
                            2= Individuales.
                            3= Publicidad sin precios.
    5  > FechaAct:  Integer Fecha de la última actualización del combo, importante a tener en cuenta para evitar que se envíen combos de promoción con precios desactualizados.
                            La fecha en formato de números indica que el valor 1 = 01/01/2020, y desde ahí en adelante.
    6  > Tipo_Prod: Integer 0= Indica que es un combinación de piezas de distintas líneas.
                            1= Predomina la línea del 1er producto.
                            2= Repuestos. 
                            3= Bazar. 
                            4= Ayuda Ventas.
                            5= Pedidos especiales.
                            6= Refugio Canino.
    7  > PcioLista: Real    Es el precio de lista ya que por lo general se realizan los cálculos de las cuotas en base a éste valor. Tener en cuenta que la intención primordial
                            es publicar los valores de las cuotas mas populares como por ej actualmente Ahora12 y Ahora18 y no precios de costo, pspv u otros.
    8  > Valor_Inte.Integer Es el ID que identifica de donde se toman los precios. Por ejemplo en éstos momentos, dentro de la ventana de Combos, tenemos hasta 5 listas de precios para probar, es decir que podemos cargar una cierta cantidad de cuotas e intereses y dejarlos almacenados. Los precios que se van a tomar para la actualización de los combos, se indican según el ID de esa lista de Intereses. Cabe destacar que por ejemplo por el momento, estamos sólo cargando el Ahora12 y Ahora18, por ende, sólo hay 2 cantidades de cuotas con su interés cada una, las imagenes deben tener entonces, 2 precios a cargar. Cuando no coincidan las cantidades entonces el combo no será actualizado.
    
    TABLA: Cbo_page2
    11 Columnas
    1  > ID:        Integer Autoincremental
    Prod1 al 10:    Integer Es el id de cada producto que contiene el combo o la imagen, pudiendo cargar hasta 10 productos en una misma imagen.

    TABLA: Cbo_page3
    11 Columnas
    1  > ID:        Integer Autoincremental
    Costo1 al 10:    Real   Es el porcentaje de descuento que le figura al combo. Por ejemplo, 0 indica que se cobra entero el producto y 100 es cuando viene de regalo.
    
    TABLA: Cbo_page4
    Tabla que indica cómo y donde se deben pegar las imágenes que contienen los números (para los precios de las cuotas) dentro de los combos. Es decir, que se indica por ejemplo en el combo 1, dónde se coloca el precio de la cuota del Ahora 12, indicando con coordenadas cartesianas la ubicación de la primer imagen y luego las demás se alinean con la primera. También se indica la orientación de los números, debido a que por ejemplo los números puede que tengan la necesidad de estar uno arriba de otro o ambos en una posición horizontal. En éste último caso hay una complicación adicional debido a que si tenemos 2 precios juntos (ej: "$ 1.598 $ 989"), el de valor 989 no nos genera problema porque indicamos la esquina superior izquierda de la imagen que representa el signo pesos y de ahí hacia la derecha vamos colocando el resto de imágenes. En cambio, en el caso de 1.598 no podemos indicar el primer píxel de la esquina superior izquierda porque no sabemos si siempre van a ser cuotas de 4 dígitos o más, entonces lo que hacemos es lo contrario, indicamos la esquina superior derecha del número 8 y de ahí vamos colocando hacia la izquierda las otras imágenes. Para ello es la "ORIENTACIÓN", para determinar si el pixel indicado va hacia la izquierda o derecha.
    Luego tenemos el valor en grados para girar los precios, por si su ubicación no es horizontal como es habitual sinó con algún grado de inclinación.
    13 Columnas
    1  > ID:        Integer Autoincremental
    Orientacion:    Integer 1= De izquierda a derecha, siendo el píxel de la parte superior.
                            2= De izquierda a derecha, siendo el píxel de la parte inferior.
                            3= De derecha a izquierda, siendo el píxel de la parte superior.
                            4= De derecha a izquierda, siendo el píxel de la parte inferior.
                            5= Es el píxel que indica el centro de todas las imagenes, por si el valor es uno sólo, se indica el centro. Píxel de la parte superior.
                            6= Es el píxel que indica el centro de las imagenes, perteneciendo a la parte inferior.
    Alineación:     Integer 0 - 360. Grados de inclinación de las imágenes.
    X1 al X5:       Integer Valor del eje X para el píxel que indica dónde comienza una imagen.
    Y2 al Y5:       Integer Idem anterior con eje Y.

'''

#Biblioteca para conectarse a base de datos SQLite
import sqlite3
import sources.mod.vars as mi_vars
#import vars as mi_vars

'''########################################################################################################################################
###########################################################################################################################################
                                                    BD: Prod.db >>> GENERALES                                                           '''

# Devuelve la tabla Cuotas de la base de datos de Prod.db
def Dev_Tabla_Prod(Tabla):
    return Dev_Tabla("./db\\prod.db", Tabla)

'''########################################################################################################################################
###########################################################################################################################################
                                                    BD: Prod.db >>> TABLA: Combos                                                       '''

# Busca según se ingrese un ID o el número del combo y devuelve una lista con los datos. Si no se encuentra devuelve "False" en la posición Lista[0]
def Dev_Reg_Combo(ID = 0, Nro = 0):
    Lista = []
    if ID > 0:
        query = "SELECT * FROM Combos WHERE ID = {}" .format(ID)
        Resultado = ""
        Resultado = Realiza_consulta(".db\\prod.db", query)
        if Resultado != "":
            for i in Resultado:
                return Lista.append(i)
    elif Nro > 0:
        query = "SELECT * FROM Combos WHERE Nro = {}" .format(Nro)
        Resultado = ""
        Resultado = Realiza_consulta(".db\\prod.db", query)
        if Resultado != "":
            for i in Resultado:
                return Lista.append(i)
    return Lista.append(False)

# Agrega un nuevo Registro
def Add_Combo(Activo, Nro, FechaAct, Tipo, Prod1, Prod2, Prod3, Prod4, Prod5, Prod6, Prod7, Prod8, Prod9, Prod10, Costo1, Costo2, Costo3, Costo4, Costo5, Costo6, Costo7, Costo8, Costo9, Costo10):
    sql = 'INSERT INTO Combos VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    parametros = (Activo, Nro, FechaAct, Tipo, Prod1, Prod2, Prod3, Prod4, Prod5, Prod6, Prod7, Prod8, Prod9, Prod10, Costo1, Costo2, Costo3, Costo4, Costo5, Costo6, Costo7, Costo8, Costo9, Costo10)
    Realiza_consulta("./db\\prod.db", sql, parametros)

'''########################################################################################################################################
###########################################################################################################################################
                                                    BD: Prod.db >>> TABLA: Config                                                       '''

# DEVUELVE UN REGISTRO BUSCADO SEGÚN UN DATO EN PARTICULAR DE LA TABLA CONFIG
def Dev_Reg_Prod_Config(Columna, DatoCoincide):
    sql = "SELECT * FROM Config WHERE {} = '{}'" .format( Columna, DatoCoincide)
    Resultado = Realiza_consulta("./db\\prod.db",sql)
    return Resultado

def Act_Regalo_Porcentaje(Valor):
    ID = 5
    query = 'UPDATE Config SET Registros = ? WHERE ID = ?'
    parameters = (Valor, ID)
    Realiza_consulta("./db\\prod.db", query, parameters)

def Act_Regalo_Margen(Valor):
    ID = 5
    query = 'UPDATE Config SET Activos = ? WHERE ID = ?'
    parameters = (Valor, ID)
    Realiza_consulta("./db\\prod.db", query, parameters)

'''########################################################################################################################################
###########################################################################################################################################
                                                            BD: clie.db                                                                '''

# Devuelve el registro de una tabla en particular
def Dev_Reg_Segun_Tabla(Tabla, Columna, DatoCoincide):
    reg = Reg_Un_param_Int(mi_vars.DB_CLIENTES, Tabla, Columna, DatoCoincide)
    return reg

# Devuelve 2 variables, la tabla completa que se haya solicitado y el total de registros que tiene
def Dev_Tabla_Clie_Total(Tabla):
    Total = 0
    _Tabla = Dev_Tabla(mi_vars.DB_CLIENTES, Tabla)
    Registro = Reg_Un_param(mi_vars.DB_CLIENTES, "sqlite_sequence", "name", Tabla)
    for reg in Registro:
        Total = reg[1]
    return _Tabla, Total

# Devuelve la tabla solicitada de la base de datos de clientes
def Dev_Tabla_Clie(Tabla):
    return Dev_Tabla(mi_vars.DB_CLIENTES, Tabla)

# Devuelve el total de registros de la tabla solicitada de la base de datos de clientes
def Dev_Total_Tabla_Clie(Tabla):
    reg = Reg_Un_param(mi_vars.DB_CLIENTES, "sqlite_sequence", "name", Tabla)
    valor = 0
    for i in reg:
        valor = i[1]
    return valor

def Dev_ID_ClienteTexto(Tabla, ColumnaCompara, DatoTexto):
    sql = "SELECT ID FROM {} WHERE {} = '{}'" .format(Tabla, ColumnaCompara, DatoTexto)
    Resultado = Realiza_consulta(mi_vars.DB_CLIENTES,sql)
    aux = -1
    for res in Resultado:
        aux = res[0] 
    return aux

def Dev_ID_ClienteInt(Tabla, ColumnaCompara, DatoEntero):
    sql = "SELECT ID FROM {} WHERE {} = {}" .format(Tabla, ColumnaCompara, DatoEntero)
    Resultado = Realiza_consulta(mi_vars.DB_CLIENTES,sql)
    aux = 0
    for res in Resultado:
        aux = res[0] 
    return aux

# Llega un ID y devuelve 3 listas, una con los datos de la tabla "Contacto", "DatosPersonales" y "SusProductos"
# Nota: El ID debe ser un dato existente
def Dev_Datos_Cliente(ID):
    lista1 = []
    lista2 = []
    lista3 = []
    reg = Reg_Un_param_Int(mi_vars.DB_CLIENTES, "Contacto","ID", ID)
    for i in reg:
        for n in range(14):
            lista1.append(i[n])
    reg = Reg_Un_param_Int(mi_vars.DB_CLIENTES, "DatosPersonales","ID", ID)
    for i in reg:
        for n in range(9):
            lista2.append(i[n])
    reg = Reg_Un_param_Int(mi_vars.DB_CLIENTES, "SusProductos","ID", ID)
    for i in reg:
        for n in range(6):
            lista3.append(i[n])
    return lista1, lista2, lista3

# A continuación, se agrega un cliente nuevo con 5 funciones. Desde donde corresponda se llama a la primera que desgloza los datos de una lista y los envía a las funciones
    # encargadas de crear un nuevo registro en cada una de las 4 tablas que tenemos con datos de los clientes.
def Add_Cliente_Nuevo(Lista):
    Add_Cliente_Nuevo_DatosPers(Lista[0], Lista[1], Lista[2], Lista[3], Lista[4], Lista[5], Lista[6], Lista[7])
    Add_Cliente_Nuevo_Formas_Pago(Lista[8], Lista[9], Lista[10], Lista[11], Lista[12])
    Add_Cliente_Nuevo_Sus_Prod(Lista[13], Lista[14], Lista[15], Lista[16], Lista[17])
    Add_Cliente_Nuevo_Contacto(Lista[18], Lista[19], Lista[20], Lista[21], Lista[22], Lista[23], Lista[24], Lista[25], Lista[26], Lista[27], Lista[28], Lista[29], Lista[30])
    Add_Cliente_Nuevo_WspVinculado( 1, 0, 0, 0, "")
# TABLA: DATOS PERSONALES
def Add_Cliente_Nuevo_DatosPers(Apellido1, Apellido2, Nombre1, Nombre2, Nombre3, Dni, Clasificacion, Comentario):
    sql = "INSERT INTO DatosPersonales VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?)"
    parametros = (Apellido1, Apellido2, Nombre1, Nombre2, Nombre3, Dni, Clasificacion, Comentario)
    Realiza_consulta(mi_vars.DB_CLIENTES, sql, parametros)
# TABLA: FORMAS DE PAGO
def Add_Cliente_Nuevo_Formas_Pago(Met1, Met2, Met3, Met4, Met5):
    sql = "INSERT INTO FormasDePago VALUES(NULL, ?, ?, ?, ?, ?)"
    parametros = (Met1, Met2, Met3, Met4, Met5)
    Realiza_consulta(mi_vars.DB_CLIENTES, sql, parametros)
# TABLA: SUS PRODUCTOS
def Add_Cliente_Nuevo_Sus_Prod(Adquirido, EnProceso, Deseos, Fecha, Recordatorios):
    sql = "INSERT INTO SusProductos VALUES(NULL, ?, ?, ?, ?, ?)"
    parametros = (Adquirido, EnProceso, Deseos, Fecha, Recordatorios)
    Realiza_consulta(mi_vars.DB_CLIENTES, sql, parametros)
# TABLA: CONTACTO
def Add_Cliente_Nuevo_Contacto(Agendado_Cel, TelFijo, Celular, Localidad, Direccion, Facebook, Instagram, email1, email2, Contacto1, Contacto2, Contacto3, Conocimiento):
    sql = "INSERT INTO Contacto VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    parametros = (Agendado_Cel, TelFijo, Celular, Localidad, Direccion, Facebook, Instagram, email1, email2, Contacto1, Contacto2, Contacto3, Conocimiento)
    Realiza_consulta(mi_vars.DB_CLIENTES, sql, parametros)
def Add_Cliente_Nuevo_WspVinculado( Trato, Difusion1, Difusion2, Difusion3, MsjProgramado):
    sql = "INSERT INTO WspVinculado VALUES(NULL, ?, ?, ?, ?, ?)"
    parametros = ( Trato, Difusion1, Difusion2, Difusion3, MsjProgramado)
    Realiza_consulta(mi_vars.DB_CLIENTES, sql, parametros)

# Actualiza los datos de un cliente previamente agendado
# Nota: 2 funciones que trabajan como una, que tuve que diseñar debido a un mal diseño de la función anterior, de crear nuevos clientes con el botón de guardar
def Act_Cliente(ID, Lista):
    Lista1 = [Lista[0], Lista[1], Lista[2], Lista[3], Lista[4], Lista[5], Lista[6], Lista[7]]
    Lista2 = [Lista[8], Lista[9], Lista[10], Lista[11], Lista[12]]
    Lista3 = [Lista[13], Lista[14], Lista[15], Lista[16], Lista[17]]
    Lista4 = [Lista[18], Lista[19], Lista[20], Lista[21], Lista[22], Lista[23], Lista[24], Lista[25], Lista[26], Lista[27], Lista[28], Lista[29], Lista[30]]
    Act_Cliente2(ID, Lista4, Lista1, Lista2, Lista3)
def Act_Cliente2(ID, Lista_Contacto, Lista_Datos_P, Lista_Forma_P, Lista_Sus_Prod):
    # Tabla: Datos Personales
    query = 'UPDATE DatosPersonales SET Apellido1 = ?, Apellido2 = ?, Nombre1 = ?, Nombre2 = ?, Nombre3 = ?, Dni = ?, Clasificacion = ?, Comentario = ? WHERE ID = ?'
    parameters = (Lista_Datos_P[0], Lista_Datos_P[1], Lista_Datos_P[2], Lista_Datos_P[3], Lista_Datos_P[4], Lista_Datos_P[5], Lista_Datos_P[6], Lista_Datos_P[7], ID)
    Realiza_consulta(mi_vars.DB_CLIENTES, query, parameters)

    # Tabla: Formas de Pago
    query = 'UPDATE FormasDePago SET Met1 = ?, Met2 = ?, Met3 = ?, Met4 = ?, Met5 = ? WHERE ID = ?'
    parameters = (Lista_Forma_P[0], Lista_Forma_P[1], Lista_Forma_P[2], Lista_Forma_P[3], Lista_Forma_P[4], ID)
    Realiza_consulta(mi_vars.DB_CLIENTES, query, parameters)

    # Tabla: Sus Productos
    query = 'UPDATE SusProductos SET Adquirido = ?, EnProceso = ?, Deseos = ?, Fecha = ?, Recordatorios = ? WHERE ID = ?'
    parameters = (Lista_Sus_Prod[0], Lista_Sus_Prod[1], Lista_Sus_Prod[2], Lista_Sus_Prod[3], Lista_Sus_Prod[4], ID)
    Realiza_consulta(mi_vars.DB_CLIENTES, query, parameters)

    # Tabla: Contacto
    query = 'UPDATE Contacto SET Agendado_Cel = ?, TelFijo = ?, Celular = ?, Localidad = ?, Direccion = ?, Facebook = ?, Instagram = ?, email1 = ?, email2 = ?, Contacto1 = ?, Contacto2 = ?, Contacto3 = ?, Conocimiento = ? WHERE ID = ?'
    parameters = ( Lista_Contacto[0], Lista_Contacto[1], Lista_Contacto[2], Lista_Contacto[3], Lista_Contacto[4], Lista_Contacto[5], Lista_Contacto[6], Lista_Contacto[7], Lista_Contacto[8], Lista_Contacto[9], Lista_Contacto[10], Lista_Contacto[11], Lista_Contacto[12], ID)
    Realiza_consulta(mi_vars.DB_CLIENTES, query, parameters)

# Actualiza los datos de un cliente previamente agendado, se usa en la actualización desde un csv descargado de la cuenta del celular
def Act_Cliente_csv(ID, Celular, Apellido, Nom1, Nom2, Nom3, Direccion, Comentario):
    query = 'UPDATE Contacto SET Celular = ?, Direccion = ? WHERE ID = ?'
    parameters = ( Celular, Direccion, ID)
    Realiza_consulta(mi_vars.DB_CLIENTES, query, parameters)

    query = 'UPDATE DatosPersonales SET Apellido1 = ?, Nombre1 = ?, Nombre2 = ?, Nombre3 = ?, Comentario = ? WHERE ID = ?'
    parameters = (Apellido, Nom1, Nom2, Nom3, Comentario, ID)
    Realiza_consulta(mi_vars.DB_CLIENTES, query, parameters)

'''########################################################################################################################################
###########################################################################################################################################
                                                                GENERAL                                                                 '''
# DEVUELVE LA TABLA COMPLETA QUE SE HAYA SOLICITADO
def Dev_Tabla(BaseDeDatos, Tabla):
    sql = 'SELECT * FROM "{}"' .format(Tabla)
    Resultado = Realiza_consulta(BaseDeDatos, sql)
    return Resultado

# DEVUELVE UN REGISTRO BUSCADO SEGÚN UN DATO EN STRING
def Reg_Un_param(BaseDeDatos, Tabla, Columna, DatoCoincide):
    sql = "SELECT * FROM {} WHERE {} = '{}'" .format( Tabla, Columna, DatoCoincide)
    Resultado = Realiza_consulta(BaseDeDatos,sql)
    return Resultado

# DEVUELVE UN REGISTRO BUSCADO SEGÚN UN DATO EN ENTERO
def Reg_Un_param_Int(BaseDeDatos, Tabla, Columna, DatoCoincide):
    sql = "SELECT * FROM {} WHERE {} = {}" .format( Tabla, Columna, DatoCoincide)
    Resultado = Realiza_consulta(BaseDeDatos,sql)
    return Resultado

# DEVUELVE UN REGISTRO PERO LOS DATOS DIRECTAMENTE EN UNA LISTA SEGÚN UN ENTERO
def Dev_Lista_Registro_Int(BaseDeDatos, Tabla, Columna, DatoCoincide):
    sql = "SELECT * FROM {} WHERE {} = {}" .format( Tabla, Columna, DatoCoincide)
    Resultado = Realiza_consulta(BaseDeDatos,sql)
    lista = []
    for i in Resultado:
        for n in range(len(i)):
            lista.append(i[n])
    return lista

# DEVUELVE UN DATO PARTICULAR SEGÚN UN ENTERO
# Nota: El dato debe existir, y el dato de la Col_Devuelve debe ser un valor entero entendiendo que 0 es la primer columna
def Dev_Dato_Int(BaseDeDatos, Tabla, Col_Compara, DatoCoincide, Col_Devuelve):
    sql = "SELECT * FROM {} WHERE {} = {}" .format( Tabla, Col_Compara, DatoCoincide)
    Resultado = Realiza_consulta(BaseDeDatos,sql)
    for i in Resultado:
        return i[Col_Devuelve]

'''########################################################################################################################################
###########################################################################################################################################
                                                                GENERAL                                                                 '''

# INSERTA UN REGISTRO EN LA BASE DE DATOS
def Reg_Add(BaseDeDatos, Activo, Codigo, Linea, Tipo, Interior, Repuesto, ConceptoBazar, ConceptoAyVta, PedidosEsp, Otros,Tamanio, Litros, PcioCosto, Costo10, PSPV, PcioLista, Puntos, PuntosMG, Comentarios, Imagen, Actualizado):
    sql = 'INSERT INTO Productos VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    parametros = (Activo, Codigo, Linea, Tipo, Interior, Repuesto, ConceptoBazar, ConceptoAyVta, PedidosEsp, Otros,Tamanio, Litros, PcioCosto, Costo10, PSPV, PcioLista, Puntos, PuntosMG, Comentarios, Imagen, Actualizado)
    Realiza_consulta(BaseDeDatos, sql, parametros)

# ACTUALIZA LOS PRODUCTOS EN LA BASE DE DATOS
# La tabla se edita acá, en éste caso se llama "Productos"
def Act_Reg_Prod(BaseDeDatos, ID, Activo, Codigo, Linea, Tipo, Interior, Repuesto, ConceptoBazar, ConceptoAyVta, PedidosEsp, Otros,Tamanio, Litros, PcioCosto, Costo10, PSPV, PcioLista, Puntos, PuntosMG, Comentarios, Imagen, Actualizado):
    if Comentarios == "":
        query = 'UPDATE Productos SET Activo = ?, Codigo = ?, Linea = ?, Tipo = ?, Interior = ?, Repuesto = ?, ConceptoBazar = ?, ConceptoAyVta = ?, PedidosEsp = ?, Otros = ?, Tamanio = ?, Litros = ?, PcioCosto = ?, Costo10 = ?, PSPV = ?, PcioLista = ?, Puntos = ?, PuntosMG = ?, Imagen = ?, Actualizado = ? WHERE ID = ?'
        parameters = (Activo, Codigo, Linea, Tipo, Interior, Repuesto, ConceptoBazar, ConceptoAyVta, PedidosEsp, Otros,Tamanio, Litros, PcioCosto, Costo10, PSPV, PcioLista, Puntos, PuntosMG, Imagen, Actualizado, ID)
    else:
        query = 'UPDATE Productos SET Activo = ?, Codigo = ?, Linea = ?, Tipo = ?, Interior = ?, Repuesto = ?, ConceptoBazar = ?, ConceptoAyVta = ?, PedidosEsp = ?, Otros = ?, Tamanio = ?, Litros = ?, PcioCosto = ?, Costo10 = ?, PSPV = ?, PcioLista = ?, Puntos = ?, PuntosMG = ?,  Comentarios = ?, Imagen = ?, Actualizado = ? WHERE ID = ?'
        parameters = (Activo, Codigo, Linea, Tipo, Interior, Repuesto, ConceptoBazar, ConceptoAyVta, PedidosEsp, Otros,Tamanio, Litros, PcioCosto, Costo10, PSPV, PcioLista, Puntos, PuntosMG, Comentarios, Imagen, Actualizado, ID)
    Realiza_consulta(BaseDeDatos, query, parameters)

def Act_Reg_Interior(BaseDeDatos, ID, Activo, Valor, Texto):
    query = 'UPDATE Interior SET Activo = ?, Valor = ?, Texto = ? WHERE ID = ?'
    parameters = (Activo, Valor, Texto, ID)
    Realiza_consulta(BaseDeDatos, query, parameters)

def Act_Reg_Linea(BaseDeDatos, ID, Activo, Valor, Texto):
    query = 'UPDATE Linea SET Activo = ?, Valor = ?, Texto = ? WHERE ID = ?'
    parameters = (Activo, Valor, Texto, ID)
    Realiza_consulta(BaseDeDatos, query, parameters)

def Act_Reg_Tipo(BaseDeDatos, ID, Activo, Valor, Texto):
    query = 'UPDATE Tipo SET Activo = ?, Valor = ?, Texto = ? WHERE ID = ?'
    parameters = (Activo, Valor, Texto, ID)
    Realiza_consulta(BaseDeDatos, query, parameters)

# Actualiza la tabla "Config", sirve para actualizar todos los totales de "Registros" que hay en cada una de las tablas
def Act_Reg_Cant(BaseDeDatos, Cantidad, NomTabla):
    query = 'UPDATE Config SET Registros = ? WHERE Tabla = ?'
    parameters = (Cantidad, NomTabla)
    Realiza_consulta(BaseDeDatos, query, parameters)

# Devuelve en una lista la traducción de los datos de un producto, ya que por ejemplo la línea de un producto en la base de datos figura con un número y no en texto
def Dev_Producto_String(ID):
    auxs = ""
    Reg = Reg_Un_param_Int(mi_vars.BaseDeDatos, "Productos", "ID", ID)
    Lista = [] 
    # Será conformada de la sgt manera: Tipo - Linea - Interior - Repuesto - Bazar - AyVta - PedEspeciales - Otros - Tamanio - Litros
    for pos in Reg:
        Lista.append(pos[4])
        Lista.append(pos[3])
        Lista.append(pos[5])
        Lista.append(pos[6])
        Lista.append(pos[7])
        Lista.append(pos[8])
        Lista.append(pos[9])
        Lista.append(pos[10])
        Lista.append(pos[11])
        Lista.append(pos[12])
    # Si es una Pieza le cargamos sus datos, sino lo tratamos como las demás piezas
    if Lista[0] > 0:
        auxs = Dev_Dato_Int(mi_vars.BaseDeDatos, "Tipo", "ID", Lista[0], 3)
        auxs += " " + Dev_Dato_Int(mi_vars.BaseDeDatos, "Linea", "ID", Lista[1], 3)
        auxs += " " + Dev_Dato_Int(mi_vars.BaseDeDatos, "Interior", "ID", Lista[2], 3)
        auxs += " " + Lista[8] + "cm"
        auxs += " " + Lista[9] + "lts"
    else:
        for i in range(3,8):
            if i != "":
                auxs = Lista[i] + " "
                if Lista[8] != "":
                    auxs += Lista[8] + "cm "
                if Lista[9] != "":
                    auxs += Lista[9] + "lts"
                break
    return auxs




# BUSCA UN PRODUCTO SEGÚN UN CÓDIGO. 
# DEVUELVE 2 VARIABLES:
    # VARIABLE 1:
        # 0 = Cuando no existe el código
        # 1 = Código normal
    # VARIABLE 2: La posición que indica si está activo
def Busca_Cod(Codigo):
    
    # Buscamos el dato de la lista de códigos principal
    Registro = Reg_Un_param(mi_vars.BaseDeDatos, "Productos", "Codigo", Codigo)

    # He creado primero la lista row con valores de cero(0), porque no puedo capturar la excepción en caso de que haya un error al no
        # encontrar el código en la base de datos. Entonces, la línea: for posicion in Registro: no se ejecuta cuando el valor del Registro es
        # nulo. Al no ejecutarse, row no se actualiza, por ende, deduzco si se encontró o no el Registro.
    row = [ '0', '0', '0']
    for posicion in Registro:
        row = [posicion[0], posicion[1], posicion[2]]

    # Con éste if, determino si se han cargado los datos o no.
    # True: NO SE ENCONTRÓ EL CODIGO EN LA BD. False: Ejecución normal
    if row[0] == '0':
        return 0, False
    else:
        return 1, row[0]


print('Módulo ManejoBBDD.py cargado correctamente.')

'''
Act_Reg_Tipo("./db\\prod.db", 2, True, 1, "-")
Act_Reg_Tipo("./BBDD\\Productos.db", 3, True, 2, "Sartén")
Act_Reg_Tipo("./BBDD\\Productos.db", 4, True, 3, "Cacerola Redonda")
Act_Reg_Tipo("./BBDD\\Productos.db", 5, True, 4, "Cacerola Cuadrada")
Act_Reg_Tipo("./BBDD\\Productos.db", 6, True, 5, "Bifera")
Act_Reg_Tipo("./BBDD\\Productos.db", 7, True, 6, "Utensillos")
'''
#CONECTA CON LA BD, Y RETORNA LOS DATOS SOLICITADOS
# Los pasos para trabajar en la bd, son: Conectarse, realizar la consulta, cargarla en una variable y desconectarse
# query será el parámetro que traiga el tipo de consuta que se desea, y en caso de haber parámetros, se utilizarán, de lo contrario, la tupla queda vacía
def Realiza_consulta( BaseDeDatos, query, parameters = ()):
    db_nombre = BaseDeDatos
    # Realizamos la conección y la almacenamos en la variable conn
    with sqlite3.connect(db_nombre) as conn:
        # Cursor, es una propiedad que nos indica en qué posición estamos dentro de la base de datos, y lo almacenamos en la variable Cur
        Cur = conn.cursor()
        # Execute, es la función que realiza la consulta, y los resultados obtenidos serán almacenados en la variable resultado
        resultado = Cur.execute(query, parameters)
        conn.commit()
    return resultado


#print(str(Dev_ID_ClienteInt("ConfigFormaPago", "Orden", 2)))
#print(str(Dev_ID_ClienteTexto("ConfigFormaPago", "Nombre", "Visa")))

#print(Dev_ID_ClienteTexto("Contacto","Agendado_Cel","Pg 1093"))

#print(Dev_Lista_Registro_Int(mi_vars.BaseDeDatos, "Productos", "ID", 41))
#print(Dev_Producto_String(22))