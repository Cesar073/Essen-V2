''' 
FORMATOS
def Formato_Decimal(Valor, Decimales):
def Formato_Unidades(Valor):
def Formato_Contabilidad(Valor):

FUNCIONES GLOBALES
def Es_Numero_Int(Valor):
def Es_Numero(Valor):

FUNCIONES INTERNAS
def Ajusta_Decimales(Valor, Decimales):
def Separador_Int_Float(Valor):
def Punto_Mil(Valor):
def Texto_A_Num(Texto):
'''
from datetime import datetime

# Convierte la fecha actual al mes corriente, para ser guardado en la base de datos. El parámetro indica la posición inicial del Año
def R_T_Dev_Fecha_Act(Izq_Anio = True):
    dt = datetime.now()
    if Izq_Anio == True:
        Resultado = str(dt.year) + '/' + str(dt.month) + '/' + str(dt.day)
    else:
        Resultado = str(dt.day) + '/' + str(dt.month) + '/' + str(dt.year)
    return Resultado

'''################################################################   FORMATOS   ################################################################'''

# Discrimina el mes de una fecha que viene en formato de string
def Devuelve_Valor_Mes(Valor):
    Texto = str(Valor)
    Estado = 0
    Aux = ''
    for i in Texto:
        if i == '/':
            Estado += 1
        else:
            if Estado == 2:
                return Aux
            elif Estado == 1:
                Aux += i

# Devuelve el mes en texto según un número del 1 al 12
def Devuelve_Mes_Texto(Valor):
    if Es_Numero_Int(Valor) == True:
        Valor = int(Valor)
        if Valor > 0 and Valor < 13:
            if Valor == 1:
                return 'Enero'
            if Valor == 2:
                return 'Febrero'
            if Valor == 3:
                return 'Marzo'
            if Valor == 4:
                return 'Abril'
            if Valor == 5:
                return 'Mayo'
            if Valor == 6:
                return 'Junio'
            if Valor == 7:
                return 'Julio'
            if Valor == 8:
                return 'Agosto'
            if Valor == 9:
                return 'Septiembre'
            if Valor == 10:
                return 'Octubre'
            if Valor == 11:
                return 'Noviembre'
            if Valor == 12:
                return 'Diciembre'
    return False

#FORMATO DE NÚMEROS
    # Sólo permite números enteros
def Devuelve_Entero(Valor):
    Aux1 = str(Valor)
    Aux2 = ''
    for i in Aux1:
        if Es_Numero(i) == True:
            Aux2 += i
        else:
            return Aux2
    return Aux2

#FORMATO CONTABLE
    # 1005 >>> 1.005,00
    # Devuelve False si no es un número que se pueda tratar
def Formato_Decimal(Valor, Decimales):
    # Recibe un valor numérico y siempre devuelve un valor con formato Contable con la cantidad de decimales indicados.
    # En caso de que el valor que llega venga con decimales coloca los verdaderos decimales.
    if Es_Numero(Valor):
        Aux1 = round(float(Valor), Decimales)
        Entero, Decimal = Separador_Int_Float(Aux1)
        return (Punto_Mil(Entero) + ',' + Ajusta_Decimales(Decimal, Decimales))
    else:
        return False

# En las bases de datos se guardan valores tipo float, pero ese valor en la variable del LineEdit dentro de la ventana debe tener un formato de string específico
    # y acá se lo devolvemos. Es decir, que si un número tiene un punto y ceros después del punto, no hay razón para que exista un valor, así que hay que dejar
    # el valor como si fuera tan sólo un número entero, pero por el contrario, si tiene valor decimal, ya sea uno o 2, se debe colocar su valor exacto.
def Formato_ValorF_Variable(Valor):
    VEntero, Decimal = Separador_Int_Float(Valor)
    Aux = int(Decimal)
    if Aux > 0:
        Aux2 = str(VEntero)
        resultado = Aux2 + '.' + str(Aux)
        return resultado
    else:
        return str(VEntero)

# FORMATO SÓLO PARA UNIDADES: CANTIDADES ENTERAS O KG. SI UN VALOR LLEGA TIPO FLOAT PERO SU PARTE DECIMAL ES 0 (CERO), ENTONCES DEVUELVE UN NÚMERO
    # ENTERO, DE LO CONTRARIO, DEVUELVE UN DECIMAL CON LA CANTIDAD DE DÍGITOS INDICADOS 
    # 5000 >>> 5.000
    # 1243.50 >>> 1.243,500
def Formato_Unidades(Valor, Decimales):
    # Recibe un valor numérico que puede ser del tipo float. Si el valor es entero, devuelve un número sin coma. De lo contrario, devuelve la cantidad de
    # decimales indicados por parámetro.

    if Es_Numero(Valor):
        Aux1 = str(Valor)
        if (Valor / 1) != (Valor // 1):
            Entero , Decimal = Separador_Int_Float(Valor)
            Entero = Punto_Mil(Entero)
            Decimal = Ajusta_Decimales(Decimal, Decimales)
            return Entero + ',' + Decimal
        else:
            return Punto_Mil(Aux1)


# AJUSTA EL FORMATO CONTABILIDAD AGREGANDO EL SIGNO $, PERO DEJANDO EL ESPACIO ENTRE EL SIGNO Y LOS NÚMERO PARA QUE APROXIMADAMENTE QUEDEN A LA MISMA DISTANCIA
# DEVUELVE UN STRING
# EJEMPLO: Si se va a rellenar una lista donde tenemos un número de 4 dígitos (58,50) y otro de 3 (2,50), lo que hacemos es agregar el signo $ adelante, y darle
    # la cantidad de espacios necesarios para mas o menos estar a la misma distancia, es decir, que el número de 4 dígitos tendrá el signo pesos, una cierta
    # cantidad de espacios y el número en cuestión, luego, cuando se haga el mismo proceso pero con el número de 3 dígitos, se le agregará un espacio más entre
    # el signo pesos y su número real.
    # De momento, preparándonos para la devaluación posible, lo que vamos a hacer es prepararlo para números de hasta 1 millón. Es decir, que todos los números
    # empezarán con un espacio, cuando sea 8 dígitos (###.###,##) tendrá 2 espacios, y así sucesivamente hasta el menor que son 3 dígitos.
def Formato_Contabilidad(Valor, V_F_Signo=True):
    Valor = Formato_Decimal(Valor, 2)
    if Valor == False:
        return False
    Aux = len(Valor)
    Aux2 = '  '
    if V_F_Signo == True:
        Aux2 = '$ '
    for i in range(12):
        if 13 - Aux > i:
            Aux2 += ' '
        else:
            break
    return Aux2 + Valor

# TRANSFORMA UN TEXTO A NÚMERO FLOAT
def Formato_Float(Texto):
    Aux = '0'
    if len(Texto) > 0:
        Aux = ''
        for letra in Texto:
            if Es_Numero_Int(letra) == True:
                Aux = Aux + letra
            if letra == ',':
                Aux = Aux + '.'
    
    return float(Aux)

'''################################################################   FUNCIONES GLOBALES   ################################################################'''

# Determina si es un número float o int, pero no distingue uno de otro.
# Devuelve: V o F
def Es_Numero(Valor):
    try:
        resultado = float(Valor)
        return True
    except ValueError:
        return False

def Redondear(Valor):
    Valor = float(Valor)
    Entero, Decimal = Separador_Int_Float(Valor)
    Entero = int(Entero)
    Decimal = int(Ajusta_Decimales(Decimal,1))
    if Decimal > 5:
        return Entero + 1
    else:
        return Entero

# Determina si es un número int.
# Devuelve: V o F
def Es_Numero_Int(Valor):
    try:
        resultado = int(Valor)
        return True
    except ValueError:
        return False

# Devuelve True si es el formato de fecha normal
def Es_Fecha(Fecha):
    if len(Fecha) == 10:
        if Fecha[2] == "/" and Fecha[5] == "/" and Es_Numero_Int(Fecha[0:2]) == True and Es_Numero_Int(Fecha[3:5]) == True and Es_Numero_Int(Fecha[6:]) == True:
            return True
        else:
            return False
    else:
        return False

'''################################################################   FUNCIONES INTERNAS   ################################################################'''

def Devuelve_Entero_Signo(Valor):
    if Es_Numero(Valor) == True:
        return Valor
    elif Valor == '.' or Valor == ',':
        return '.'
    else:
        return 'F'

# Recibe un valor en cualquier formato, y devuelve un string de hasta 2 decimales
def Ajusta_A_2_Dec(Valor):
    Aux1 = str(Valor)
    Bucle = 0
    Cont_Dec = 0
    largo = len(Aux1)
    Aux2 = ''
    Coma = False
    while largo > Bucle:
        Texto = Aux1[Bucle]
        if Coma == True:
            Cont_Dec += 1
            if Cont_Dec == 2:
                Aux2 += Texto
                return Aux2
            else:
                Aux2 += Texto
        else:
            if Texto == ',' or Texto == '.':
                Aux2 += '.'
                Coma = True
            else:
                Aux2 += Texto
        Bucle += 1
    return Aux2

# LLEGA LA PARTE DECIMAL DE UN NÚMERO, Y COMPLETAMOS O QUITAMOS PARA DEVOLVER EL MISMO NÚMERO CON LA CANTIDAD DECIMALES QUE SE DESEEN
    # Básicamente sirve para rellenar o quitar los decimales de otro número
    # 024 // 4 >>> 0240
    # 12504 // 2 >>> 12
def Ajusta_Decimales(Valor, Decimales):
    Aux1 = str(Valor)
    Contador = 0
    largo = len(Aux1)
    Aux2 = ''
    while Decimales > Contador:
        Contador += 1
        if Contador > largo:
            Aux2 += '0'
        else:
            Aux2 += Aux1[Contador - 1]
    return Aux2


# SEPARA PARTE DECIMAL Y ENTERA DE UN NÚMERO DEVOLVIENDO 2 STRING. SI VINIERA: .2 POR EJ, ENTONCES INTERPRETA 0 DE VALOR ENTERO
# 145.32 >>> 145 // 32
def Separador_Int_Float(Valor):
    AuxStr = str(Valor)
    if AuxStr[0] == '.':
        Valor = '0' + Valor
    Aux1 = str(float(Valor))
    Aux2 = ''
    Aux3 = ''
    coma = False
    for i in range(len(Aux1)):
        if coma == False:
            if Aux1[i] == '.':
                coma = True
            else:
                Aux2 += Aux1[i]
        else:
            Aux3 += Aux1[i]
    return Aux2, Aux3


# COLOCA EL PUNTO DE MIL, EN LA PARTE ENTERA DE CUALQUIER NÚMERO
# SIEMPRE DEBE VENIR UN NÚMERO ENTERO SIN PUNTOS NI COMAS
def Punto_Mil(Valor):
    # Tener en cuenta, que a ésta función la llaman desde otras donde ya se ha corroborado que el valor es numérico
    Valor = str(Valor)
    if Valor.count('.') > 0:
        Valor = float(Valor)
    aux = int(Valor)
    texto = str(aux)
    largo = len(texto)
    lista = []
    contador1 = 0
    contador2 = 0
    for i in texto:
        contador1 += 1
        contador2 += 1
        lista.append(texto[largo - contador1])
        if contador2 == 3 and contador1 < largo:
            lista.append('.')
            contador2 = 0
    lista.reverse()
    resultado = ''
    for n in range(len(lista)):
        resultado = resultado + lista[n]

    return resultado


# TRANSFORMA UN TEXTO EN UN NÚMERO FLOAT, ÚTIL PARA EL SISTEMA
    # 1.153,50 >>> 1153.5
def Str_Float(Valor):
    Valor = Valor.replace('.','')
    Valor = Valor.replace(',','.')
    if Valor == "":
        return 0.0
    else:
        return float(Valor)

# LAS SIGUIENTES FUNCIONES TRABAJAN EN CONJUNTO.
    # SE USAN PARA LOS LINE_EDIT DE VALORES NUMÉRICOS, ESTO SIRVE PARA QUE EL USUARIO INGRESE NÚMEROS EN UN EDIT, Y SE VAYAN COMPLETANDO TODO AUTOMÁTICAMENTE.
    # SI POR EJEMPLO ES UN LINE_EDIT DONDE SE COLOCAN PRECIOS CON 2 DECIMALES, ENTONCES CON SÓLO INGRESAR POR EJEMPLO: .2 >>> AL USUARIO LE VAMOS A MOSTRAR: 0,20
    # ES NECESARIO QUE LA VENTANA TENGA UNA VARIABLE TIPO STRING, PARA QUE GUARDE DE MANERA OCULTA PARA EL USUARIO, LO QUE SE ESTÁ INGRESANDO EN EL EDIT. 
    # LA PRIMER FUNCIÓN SE ENCARGA DE COLOCAR EN DICHA VARIABLE, EL VALOR CORRECTO QUE DEBE CONTENER, Y LA SEGUNDA FUNCIÓN LE DA EL FORMATO NECESARIO PARA DICHO
    # VALOR GUARDADO.

    # EL PRIMER PASO ES PURIFICAR LOS DATOS TIPEADOS POR EL USUARIO PARA SER ALMACENADOS EN LA VARIABLE ASOCIADA AL LINE_EDIT. A ESTO LO HACEMOS CUANDO ENVIAMOS 
    # A LA FUNCIÓN Texto_A_Num1 LO TIPEADO EN EL LINE_EDIT, LA CUÁL LE DEVUELVE EL VALOR CORRECTO QUE DEBE TENER ALMACENADO, DEBIDO A LOS SIGUIENTES ERRORES QUE SE
    # PUEDAN OCASIONAR. SI POR EJEMPLO EL USUARIO INGRESARÍA LETRAS O VARIAS COMAS Y PUNTOS, ESTO DEBE PURIFICARSE Y ALMACENARSE DE MANERA CORRECTA EN LA VARIABLE
    # INDICADA PARA EL LINE_EDIT, PORQUE SI ALMACENAMOS TODO LO QUE EL USUARIO TIPEA, PODEMOS DEVOLVERLE EL VALOR CORRECTO, PERO SI EL USUARIO POR EJEMPLO TIPEA
    # ALGO COMO: LSDF,SSDF2 >>> SE LE VA A MOSTAR: 0,20. HASTA EL MOMENTO TODO BIEN, PERO SI SE HA CONFUNDIDO Y QUIERE BORRAR LA COMA PARA INGRESAR UN VALOR
    # ENTERO DELANTE, DEBE PRESIONAR 6 VECES PARA BORRAR EL NÚMERO, YA QUE TIENE ANTES DE LA COMA UNOS 6 CARACTERES QUE EL EN REALIDAD NO LOS ESTARÍA VIENDO.
    # POR ELLO ES QUE LIMPIAMOS EL TEXTO Y LO DEJAMOS ALMACENADO COMO: .2 >>> ASÍ SÓLO PRESIONA 2 VECES BACKSPACE Y YA PUEDE TIPEAR EL VALOR CORRECTO.

    # EL SEGUNDO PASO ES ENVIAR DICHA VARIABLE A LA FUNCIÓN Texto_A_Num2, QUE SE ENCARGA DE TRANSFORMARLO A LO QUE SE QUIERE MOSTAR. EN EL EJEMPLO, DICHA VARIABLE
    # RECIBE: .2 Y DEVUELVE: 0,20

    # CABE ACLARAR QUE LA FUNCION CHANGE DEL EDIT, DEBE PERMITIR TANTO PUNTOS COMO COMAS, LUEGO TRANSFORMARLAS A AMBAS EN UN ÚNICO PUNTO.
    # LOS PUNTOS MIL LOS COLOCAMOS DE ACÁ, NO ES TAREA DEL USUARIO. EL USUARIO SÓLO COLOCA UN PUNTO O UNA COMA CUANDO QUIERA INDICAR DECIMALES. 
    # SI UN NÚMERO DEBE SER ENTERO, SÓLO DE INDICARSE QUE TIENE 0 DECIMALES.
    # 145asdf5  >>>  1455

def Texto_A_Num1(Texto, Decimales = 0):
    Aux = ''
    Coma = False
    Cont = 0
    if len(Texto) > 0:
        for letra in Texto:
            if Es_Numero(letra) == True:
                if Coma == True: 
                    Cont += 1
                    if Cont <= Decimales:
                        Aux += letra
                else:
                    Aux += letra
            else:
                if (letra == ',' or letra == '.') and Coma == False:
                    Coma = True
                    Aux += '.'
    if Decimales == 0:
        Aux = Aux.replace('.','')
    return Aux


# 
#def Texto_A_Num2(Texto, Decimales = 0):





# SU EXPLICACIÓN SE ENCUENTRA EN LA FUNCION Texto_A_Num1
def Texto_A_Num3(Texto, Decimales = 0):

    # ComaNum:
        # 1: Caracter no válido 
        # 2: Indica que es un número
        # 3: Indica que es una Coma
    ComaNum = 0
    BanderaEntera = False
    BanderaComa = False
    BanderaDecimal = False
    Aux = Texto
    Aux3 = ''
    resultado = 'Error'

    if len(Texto) > 0:
        # Con éste For armamos el número completo, siendo su parte entera, una coma y la parte decimal, o todo entero según se indique en "Decimales"
        for letra in Texto:
            # Determinamos si es un número o una coma
            if Es_Numero(letra) == True:
                ComaNum = 2
            else:
                if letra == '.' or letra == ',':
                    ComaNum = 3

            if ComaNum == 2:
                if BanderaComa == False:
                    BanderaEntera = True
                else:
                    BanderaDecimal = True

            if ComaNum == 3:
                if BanderaEntera == False:
                    if BanderaComa == False:
                        BanderaEntera = True
                        BanderaComa = True
                        Aux = '0' + Texto
                else:
                    BanderaComa = True

        

        if BanderaComa == False:
            Aux = Aux + '.0'
        else:
            if BanderaDecimal == False:
                Aux = Aux + '0'
        
        Aux2, Aux3 = Separador_Int_Float(Aux)
        Aux2 = Punto_Mil(Aux2)
        if Decimales > 0:
            if int(Aux3) > 0:
                Aux3 = Ajusta_Decimales(Aux3, Decimales)
                resultado = Aux2 + ',' + Aux3
            else:
                resultado = Aux2 + ',00'
        else:
            resultado = Aux2                
    return resultado

def Quita_Simbol(Valor):
    str(Valor)
    Valor = Valor.replace(".", "")
    Valor = Valor.replace(",", "")
    return Valor


def Normalize(Valor):
    Valor = Valor.lower()
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        Valor = Valor.replace(a, b).replace(a.upper(), b.upper())
    Valor = Valor.upper()
    return Valor

# ERROR   >>>   print(float(0125))
print('Módulo Formatos.py cargado correctamente.')
#print(Formato_Float(''))
#print(Texto_A_Num1('.2', 2))
#print(Texto_A_Num2('123.11', 2))
#print(Texto_A_Num2('12311', 2))
#print(Texto_A_Num2('123.11', 2))
#print(Texto_A_Num2('12311', 2))
#print(Texto_A_Num2('0', 2))
#print(Normalize("Holá perrá parietál"))
#print(Formato_ValorF_Variable(0.40))
#print(Punto_Mil(1000))
#print(Ajusta_A_2_Dec(123))

#print(Normalize("César"))