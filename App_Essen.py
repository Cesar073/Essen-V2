import sys
import platform
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (Signal, QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *

from PySide2 import QtWidgets
from PySide2.QtWidgets import QMainWindow, QMessageBox, QFileDialog
from PySide2.QtGui import QIcon, QPixmap, QFont
from PySide2.QtCore import QDir, Qt

import PySide2.QtGui

from sources.vtn.mw_ppal import Ui_MainWindow
from sources.cls.cla_ventas import *
from sources.cls.cla_busc import V_Buscar
from sources.cls.cla_editor_img import V_Editor
import sources.mod.vars as mi_vars
import sources.mod.mdb as mdb
import sources.mod.form as fts



class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.lista_val_img = []
        self.lista_val_leyenda = []
        #self.showMaximized()
        ancho = self.width()
        alto = self.height()
        self.setMinimumSize(ancho, alto)
        self.setMaximumSize(ancho, alto)

        self.Configura_Menu_img()
        self.Configura_Menu_lab()
        self.Configura_Ventas()

        self.Carga_iconos()

        self.ui.stackedWidget.setCurrentIndex(1)
    
    def Configura_Menu_img(self):
        # CREACIÓN COMPLETA DEL MENÚ 1 - IMAGENES:
        ancho = 60
        self.ui.frame_img.setFixedWidth(ancho)

        # Listas para configurar la clase de Labels como Botones
        self.lista_val_img.append([85,85,85])           # backcolor normal
        self.lista_val_img.append([255,92,225])         # backcolor apretado
        self.lista_val_img.append([45,45,45])           # backcolor hover
        self.lista_val_img.append([0,0,0])              # grosor del borde en normal/apretado/hover
        self.lista_val_img.append([85,85,85])           # color borde normal
        self.lista_val_img.append([0,0,0])              # color borde apretado
        self.lista_val_img.append([0,0,0])              # color borde hover
        self.lista_val_img.append([ancho,60])           # width/height modo normal
        self.lista_val_img.append([ancho,60])           # width/height modo expandido
        self.lista_val_img.append(["","",""])           # Texto del boton
        self.lista_val_img.append("")                   # ToolTip
        
        # Creamos los 9 botones con imagenes
        l_btn_expande_1 = QlabelClickeable(self.lista_val_img, self)
        l_btn_expande_2 = QlabelClickeable(self.lista_val_img, self)
        l_btn_expande_3 = QlabelClickeable(self.lista_val_img, self)
        l_btn_expande_4 = QlabelClickeable(self.lista_val_img, self)
        l_btn_expande_5 = QlabelClickeable(self.lista_val_img, self)
        l_btn_expande_6 = QlabelClickeable(self.lista_val_img, self)
        l_btn_expande_7 = QlabelClickeable(self.lista_val_img, self)
        l_btn_expande_8 = QlabelClickeable(self.lista_val_img, self)
        l_btn_expande_9 = QlabelClickeable(self.lista_val_img, self)

        # Colocamos todos los botones en una lista para poder trabajar con ellos en bucles
        self.LISTA_BOTON_IMG = []
        self.LISTA_BOTON_IMG.append(l_btn_expande_1)
        self.LISTA_BOTON_IMG.append(l_btn_expande_2)
        self.LISTA_BOTON_IMG.append(l_btn_expande_3)
        self.LISTA_BOTON_IMG.append(l_btn_expande_4)
        self.LISTA_BOTON_IMG.append(l_btn_expande_5)
        self.LISTA_BOTON_IMG.append(l_btn_expande_6)
        self.LISTA_BOTON_IMG.append(l_btn_expande_7)
        self.LISTA_BOTON_IMG.append(l_btn_expande_8)
        self.LISTA_BOTON_IMG.append(l_btn_expande_9)

        # Colocamos en listas tanto el nombre de las imagenes como el texto a cargar en los botones para utilizarlos en bucles
        Lista_Aux1 = ["men", "promo", "pedidos", "productos", "clientes", "stock", "recordatorios", "estados", "config"]
        Lista_Aux2 = ["Expande/Contrae", "Promociones", "Pedidos", "Productos", "Clientes", "Stock Interno", "Recordatorios", "Estado General", "Configuración"]

        count = 0
        while count < len(self.LISTA_BOTON_IMG):

            # Agregamos los botones a su layout
            self.ui.verticalLayout.addWidget(self.LISTA_BOTON_IMG[count])

            # Configuramos sus imagenes
            pixmap = QPixmap('./sources/img/icon/{}.png'.format(Lista_Aux1[count])).scaled(60,60)
            self.LISTA_BOTON_IMG[count].setPixmap(pixmap)
            self.LISTA_BOTON_IMG[count].setAlignment(Qt.AlignRight)
            self.LISTA_BOTON_IMG[count].setToolTip(Lista_Aux2[count])

            count += 1
        
        # CONFIGURAMOS LAS ACCIONES
        l_btn_expande_1.clicked.connect(lambda: self.Clic_Boton(0, True))
        l_btn_expande_2.clicked.connect(lambda: self.Clic_Boton(1, True))
        l_btn_expande_3.clicked.connect(lambda: self.Clic_Boton(2, True))
        l_btn_expande_4.clicked.connect(lambda: self.Clic_Boton(3, True))
        l_btn_expande_5.clicked.connect(lambda: self.Clic_Boton(4, True))
        l_btn_expande_6.clicked.connect(lambda: self.Clic_Boton(5, True))
        l_btn_expande_7.clicked.connect(lambda: self.Clic_Boton(6, True))
        l_btn_expande_8.clicked.connect(lambda: self.Clic_Boton(7, True))
        l_btn_expande_9.clicked.connect(lambda: self.Clic_Boton(8, True))

        l_btn_expande_1.flotar.connect(lambda: self.Flotar(0, True))
        l_btn_expande_2.flotar.connect(lambda: self.Flotar(1, True))
        l_btn_expande_3.flotar.connect(lambda: self.Flotar(2, True))
        l_btn_expande_4.flotar.connect(lambda: self.Flotar(3, True))
        l_btn_expande_5.flotar.connect(lambda: self.Flotar(4, True))
        l_btn_expande_6.flotar.connect(lambda: self.Flotar(5, True))
        l_btn_expande_7.flotar.connect(lambda: self.Flotar(6, True))
        l_btn_expande_8.flotar.connect(lambda: self.Flotar(7, True))
        l_btn_expande_9.flotar.connect(lambda: self.Flotar(8, True))

        l_btn_expande_1.retirar.connect(lambda: self.Retirar(0, True))
        l_btn_expande_2.retirar.connect(lambda: self.Retirar(1, True))
        l_btn_expande_3.retirar.connect(lambda: self.Retirar(2, True))
        l_btn_expande_4.retirar.connect(lambda: self.Retirar(3, True))
        l_btn_expande_5.retirar.connect(lambda: self.Retirar(4, True))
        l_btn_expande_6.retirar.connect(lambda: self.Retirar(5, True))
        l_btn_expande_7.retirar.connect(lambda: self.Retirar(6, True))
        l_btn_expande_8.retirar.connect(lambda: self.Retirar(7, True))
        l_btn_expande_9.retirar.connect(lambda: self.Retirar(8, True))

        # En dicho boton, evitamos que quede indicado si está apretado, porque esa función es para marcar en qué ventana estamos y éste botón sólo expande o contrae
        l_btn_expande_1.seApreta = False

    def Configura_Menu_lab(self):

        # CREACIÓN COMPLETA DEL MENÚ 1 - IMAGENES:
        self.ui.frame_label.setFixedWidth(0)

        # Listas para configurar la clase de Labels como Botones
        self.lista_val_leyenda.append([85,85,85])       # backcolor normal
        self.lista_val_leyenda.append([255,92,225])     # backcolor apretado
        self.lista_val_leyenda.append([45,45,45])       # backcolor hover
        self.lista_val_leyenda.append([0,0,0])          # grosor del borde en normal/apretado/hover
        self.lista_val_leyenda.append([85,85,85])       # color borde normal
        self.lista_val_leyenda.append([0,0,0])          # color borde apretado
        self.lista_val_leyenda.append([0,0,0])          # color borde hover
        self.lista_val_leyenda.append([0,60])           # width/height modo normal
        self.lista_val_leyenda.append([200,60])         # width/height modo expandido
        self.lista_val_leyenda.append(["dfhg","sdf","fsdf"])       # Texto del boton
        self.lista_val_leyenda.append("")               # ToolTip

        # Creamos los 9 botones con leyendas
        l_btn_leyenda_1 = QlabelClickeable(self.lista_val_leyenda, self)
        l_btn_leyenda_2 = QlabelClickeable(self.lista_val_leyenda, self)
        l_btn_leyenda_3 = QlabelClickeable(self.lista_val_leyenda, self)
        l_btn_leyenda_4 = QlabelClickeable(self.lista_val_leyenda, self)
        l_btn_leyenda_5 = QlabelClickeable(self.lista_val_leyenda, self)
        l_btn_leyenda_6 = QlabelClickeable(self.lista_val_leyenda, self)
        l_btn_leyenda_7 = QlabelClickeable(self.lista_val_leyenda, self)
        l_btn_leyenda_8 = QlabelClickeable(self.lista_val_leyenda, self)
        l_btn_leyenda_9 = QlabelClickeable(self.lista_val_leyenda, self)

        self.LISTA_BOTON_LEY = []
        self.LISTA_BOTON_LEY.append(l_btn_leyenda_1)
        self.LISTA_BOTON_LEY.append(l_btn_leyenda_2)
        self.LISTA_BOTON_LEY.append(l_btn_leyenda_3)
        self.LISTA_BOTON_LEY.append(l_btn_leyenda_4)
        self.LISTA_BOTON_LEY.append(l_btn_leyenda_5)
        self.LISTA_BOTON_LEY.append(l_btn_leyenda_6)
        self.LISTA_BOTON_LEY.append(l_btn_leyenda_7)
        self.LISTA_BOTON_LEY.append(l_btn_leyenda_8)
        self.LISTA_BOTON_LEY.append(l_btn_leyenda_9)

        Lista_Aux2 = ["Expande/Contrae", "Promociones", "Pedidos", "Productos", "Clientes", "Stock Interno", "Recordatorios", "Estado General", "Configuración"]

        count = 0
        while count < len(self.LISTA_BOTON_LEY):

            # Colocamos esos botones en el layout del Frame de Menú leyenda
            self.ui.verticalLayout_2.addWidget(self.LISTA_BOTON_LEY[count])
        
            # Configuramos el texto que tendrá cada uno
            self.LISTA_BOTON_LEY[count].setText(Lista_Aux2[count])
            self.LISTA_BOTON_LEY[count].setFont(QtGui.QFont('Unispace', 14))

            count += 1
        
        l_btn_leyenda_1.clicked.connect(lambda: self.Clic_Boton(0, False))
        l_btn_leyenda_2.clicked.connect(lambda: self.Clic_Boton(1, False))
        l_btn_leyenda_3.clicked.connect(lambda: self.Clic_Boton(2, False))
        l_btn_leyenda_4.clicked.connect(lambda: self.Clic_Boton(3, False))
        l_btn_leyenda_5.clicked.connect(lambda: self.Clic_Boton(4, False))
        l_btn_leyenda_6.clicked.connect(lambda: self.Clic_Boton(5, False))
        l_btn_leyenda_7.clicked.connect(lambda: self.Clic_Boton(6, False))
        l_btn_leyenda_8.clicked.connect(lambda: self.Clic_Boton(7, False))
        l_btn_leyenda_9.clicked.connect(lambda: self.Clic_Boton(8, False))

        l_btn_leyenda_1.flotar.connect(lambda: self.Flotar(0, False))
        l_btn_leyenda_2.flotar.connect(lambda: self.Flotar(1, False))
        l_btn_leyenda_3.flotar.connect(lambda: self.Flotar(2, False))
        l_btn_leyenda_4.flotar.connect(lambda: self.Flotar(3, False))
        l_btn_leyenda_5.flotar.connect(lambda: self.Flotar(4, False))
        l_btn_leyenda_6.flotar.connect(lambda: self.Flotar(5, False))
        l_btn_leyenda_7.flotar.connect(lambda: self.Flotar(6, False))
        l_btn_leyenda_8.flotar.connect(lambda: self.Flotar(7, False))
        l_btn_leyenda_9.flotar.connect(lambda: self.Flotar(8, False))

        l_btn_leyenda_1.retirar.connect(lambda: self.Retirar(0, False))
        l_btn_leyenda_2.retirar.connect(lambda: self.Retirar(1, False))
        l_btn_leyenda_3.retirar.connect(lambda: self.Retirar(2, False))
        l_btn_leyenda_4.retirar.connect(lambda: self.Retirar(3, False))
        l_btn_leyenda_5.retirar.connect(lambda: self.Retirar(4, False))
        l_btn_leyenda_6.retirar.connect(lambda: self.Retirar(5, False))
        l_btn_leyenda_7.retirar.connect(lambda: self.Retirar(6, False))
        l_btn_leyenda_8.retirar.connect(lambda: self.Retirar(7, False))
        l_btn_leyenda_9.retirar.connect(lambda: self.Retirar(8, False))

        self.BOTON_APRETADO = 0

        # Al igual que en el botón compañero de la imagen, anulamos la posibilidad de que quede marcado porque el botón que expande o contrae no nos sirve que indique eso
        l_btn_leyenda_1.seApreta = False

    def Flotar(self, pos, img):
        if pos != self.BOTON_APRETADO or pos == 0:
            if img == True:
                self.LISTA_BOTON_LEY[pos].configuraBoton(2)
                self.LISTA_BOTON_IMG[pos].configuraBoton(2)
            else:
                self.LISTA_BOTON_LEY[pos].configuraBoton(2)
                self.LISTA_BOTON_IMG[pos].configuraBoton(2)

    def Retirar(self, pos, img):
        if pos != self.BOTON_APRETADO or pos == 0:
            if img == True:
                self.LISTA_BOTON_LEY[pos].configuraBoton(0)
                self.LISTA_BOTON_IMG[pos].configuraBoton(0)
            else:
                self.LISTA_BOTON_LEY[pos].configuraBoton(0)
                self.LISTA_BOTON_IMG[pos].configuraBoton(0)

    def Clic_Boton(self, pos, img):
        
        if pos > 0:
            if img == True:
                self.LISTA_BOTON_LEY[pos].configuraBoton(1)
            else:
                self.LISTA_BOTON_IMG[pos].configuraBoton(1)

            if pos != self.BOTON_APRETADO:
                self.LISTA_BOTON_IMG[self.BOTON_APRETADO].configuraBoton(0)
                self.LISTA_BOTON_LEY[self.BOTON_APRETADO].configuraBoton(0)
                self.LISTA_BOTON_IMG[self.BOTON_APRETADO].apretado = False
                self.LISTA_BOTON_LEY[self.BOTON_APRETADO].apretado = False
                self.BOTON_APRETADO = pos
                self.LISTA_BOTON_IMG[pos].apretado = True
                self.LISTA_BOTON_LEY[pos].apretado = True
                self.contrae()
        else:
            self.LISTA_BOTON_LEY[pos].configuraBoton(0)
            self.clic_expande()
        
        self.Muestra_Ventana(pos)

    def clic_expande(self):
        print("FuncionXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        self.imprime()

        width = self.ui.frame_label.width()
        if width == 0:
            inicio = 0
            fin = 200
        else:
            inicio = 200
            fin = 0

        self.animation = QPropertyAnimation(self.ui.frame_label, b"minimumWidth")
        self.animation.setDuration(400)
        self.animation.setStartValue(inicio)
        self.animation.setEndValue(fin)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()
        self.imprime()

    def contrae(self):
        if self.ui.frame_label.width() > 0:
            self.clic_expande()

    def imprime(self):
        #print("ANCHO: {} ALTO: {}".format(str(self.ui.frame_menu.width()),str(self.ui.frame_menu.height())))
        print("ANCHO: {} ALTO: {}".format(str(self.ui.frame_img.width()),str(self.ui.frame_img.height())))
        print("ANCHO: {} ALTO: {}".format(str(self.ui.frame_label.width()),str(self.ui.frame_label.height())))

    def Muestra_Ventana(self, pos):
        '''Es la función que se encarga de mostrar la ventana que corresponde, aquí es donde se agregan las funciones que querramos aplicar cuando se debe mostrar alguna.'''
        
        # Botón de Expande/Contrae
        if pos == 0:
            pass

        # page_ventas
        elif pos == 1:
            self.ui.stackedWidget.setCurrentIndex(1)
            if len(self.Lista_vtn_ventas[0]) > 0:
                V_Ventas.Carga_Listas(self.Lista_vtn_ventas[0])

            if mi_vars.ORIGEN_BUSCAR == 1:
                mi_vars.ORIGEN_BUSCAR = 0
                if len(mi_vars.LISTABUSCADO) > 0:
                    V_Ventas.Carga_Listas(mi_vars.LISTABUSCADO)   

        # page_productos
        elif pos == 3:
            self.ui.stackedWidget.setCurrentIndex(0)
        
        # page_buscar
        elif pos == 9:
            # Limpiamos la lista que contiene los valores buscados, aquellos que se usan en la ventana que nos llamó
            mi_vars.LISTABUSCADO = []
            # Utilizamos ésta lista vacía para que deje invisibles todos los botones y los labels
            V_Buscar.Car_Img_Btn_Art(mi_vars.LISTABUSCADO)
            # Se deshabilitan los botones que sólo deben estar habilitados cuando la lista de productos supera las 20 unidades
            self.ui.push_Atras.setEnabled(False)
            self.ui.push_Adelante.setEnabled(False)
            # Actualizamos las imagenes que corresponden a la 2da cinta de botones
            V_Buscar.Actualiza_Lineas()
            # Quitamos las selecciones que pudieron haber quedado de otra búsqueda
            V_Buscar.Controla_Selecciones()
        
        # Resto de botones sin terminar
        else:
            QMessageBox.information(self, "Atención!", "Sección en desarrollo", QMessageBox.Ok)

    def Carga_iconos(self):
        '''Debido a que el código generado por QtDesigner carga mal el path de los íconos, vamos a cargarlos de manera manual.'''
        lista_1 = [self.ui.push_Bproduc,
            self.ui.push_Descuento,
            self.ui.push_Regalo,
            self.ui.push_Cprecio,
            self.ui.push_Agregar_Envio,
            self.ui.push_Borrar,
            self.ui.push_Limpiar_2,
            self.ui.push_Buscar,
            self.ui.push_Anterior,
            self.ui.push_Siguiente,
            self.ui.push_Guardar,
            self.ui.push_Limpiar,
            self.ui.push_Excel]
        
        lista_2 = ["buscar.png",
            "descuento.png",
            "regalo.png",
            "cambiar.png",
            "envios.png",
            "borrar.png",
            "limpiar.png",
            "buscar.png",
            "anterior.png",
            "siguiente.png",
            "guardar.png",
            "limpiar.png",
            "excel.png"]

        for i in range(len(lista_1)):
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("./sources/img/icon/{}".format(lista_2[i])), QtGui.QIcon.Normal, QtGui.QIcon.On)
            lista_1[i].setIcon(icon)

            # Los primeros 7 botones son de la ventana de VENTAS, donde están los combos, precios, y eso. Los demás por el momento tienen otro tamaño de iconos.
            if i > 6:
                lista_1[i].setIconSize(QtCore.QSize(60, 60))
            else:
                lista_1[i].setIconSize(QtCore.QSize(40, 40))

    ###########################################################################################################################################################################
    #                                                                       CONFIGURACIONES DE LAS VENTANAS
    ###########################################################################################################################################################################

    def Configura_Ventas(self):

        # VARIABLES DE LA VENTANA
        self.Lista_vtn_ventas = []
        # Lista cuando vuelve del buscador
        self.Lista_vtn_ventas.append([])
        # Variable que indica cuál de las 5 opciones de intereses que tenemos disponibles, está apretada
        # Su valor corresponde a la ubicación en la columna que tiene cada uno dentro de la base de datos, que indica si está activa o no
        # self.Op_Interes = 0
        self.Lista_vtn_ventas.append(0)
        # self.LINE_BOOL = False
        self.Lista_vtn_ventas.append(True)

        self.Lista_vtn_ventas[2] = False
        Registro = mdb.Reg_Un_param(mi_vars.BaseDeDatos, "Config", "Tabla", "Regalo")
        for Dato in Registro:
            self.ui.line_PorcRegalo.setText(str(Dato[2]))
            self.ui.line_MargenRegalo.setText(str(Dato[3]))
        self.Lista_vtn_ventas[2] = True

        # SIGNALS - SLOTS
        self.ui.push_Bproduc.clicked.connect(lambda: V_Ventas.Abrimos_Vtna_Buscar(self.ui))
        self.ui.push_Descuento.clicked.connect(lambda: V_Ventas.Aplicamos_Descuento(self.ui, self.Lista_vtn_ventas))
        self.ui.push_Regalo.clicked.connect(lambda: V_Ventas.Regalo_100_desc(self.ui, self.Lista_vtn_ventas))
        #self.ui.push_Cprecio.clicked.connect(lambda: V_Ventas.CAMBIAR_PRECIO)
        #self.ui.push_Agregar_Envio.clicked.connect(lambda: V_Ventas.COBRAR_ENVÍOS)

        self.ui.push_Borrar.clicked.connect(lambda: V_Ventas.Borrar_Uno(self.ui, self.Lista_vtn_ventas))
        self.ui.push_Limpiar_2.clicked.connect(lambda: V_Ventas.Limpiar(self.ui, self.Lista_vtn_ventas))

        # ACA VA EL COMBOBOX
        self.ui.line_Numero.textChanged.connect(lambda: V_Ventas.Change_Line_Combos(self.ui))
        #self.ui.push_Resta1.clicked.connect(V_Ventas.RESTA_UNO)
        #self.ui.push_Suma1.clicked.connect(V_Ventas.SUMA_1)

        # ACA VA SUGERIR REGALO
        self.ui.line_PorcRegalo.textChanged.connect(lambda: V_Ventas.Cambio_Line_Porc_Regalo(self.ui, self.Lista_vtn_ventas))
        self.ui.line_MargenRegalo.textChanged.connect(lambda: V_Ventas.Cambio_Line_Marg_Regalo(self.ui, self.Lista_vtn_ventas))

        self.ui.push_Int1.clicked.connect(lambda: V_Ventas.Btn_Int1(self.ui, self.Lista_vtn_ventas))
        self.ui.push_Int2.clicked.connect(lambda: V_Ventas.Btn_Int2(self.ui, self.Lista_vtn_ventas))
        self.ui.push_Int3.clicked.connect(lambda: V_Ventas.Btn_Int3(self.ui, self.Lista_vtn_ventas))
        self.ui.push_Int4.clicked.connect(lambda: V_Ventas.Btn_Int4(self.ui, self.Lista_vtn_ventas))
        self.ui.push_Int5.clicked.connect(lambda: V_Ventas.Btn_Int5(self.ui, self.Lista_vtn_ventas))

        self.ui.list_Detalle.clicked.connect(lambda: V_Ventas.ClickLista1(self.ui))
        self.ui.list_Desc.clicked.connect(lambda: V_Ventas.ClickLista2(self.ui))
        self.ui.list_Costo.clicked.connect(lambda: V_Ventas.ClickLista3(self.ui))
        self.ui.list_Costo10.clicked.connect(lambda: V_Ventas.ClickLista4(self.ui))
        self.ui.list_Pspv.clicked.connect(lambda: V_Ventas.ClickLista5(self.ui))
        self.ui.list_Lista.clicked.connect(lambda: V_Ventas.ClickLista6(self.ui))
        
        self.ui.list_Desc.itemDoubleClicked.connect(lambda: V_Ventas.Doble_Clic_Descuento(self.ui, self.Lista_vtn_ventas))

        #self.ui.push_Edita_Combos.itemDoubleClicked.connect(V_Ventas.EDITA_COMBOS)

    def Configura_Buscar(self):
        # BOTONES
        # Interacción
        self.ui.push_Cancelar.clicked.connect(lambda: V_Buscar.Btn_Cancelar)
        self.ui.push_Cargar.clicked.connect(lambda: V_Buscar.Btn_Cargar)
        self.ui.push_Atras.clicked.connect(lambda: V_Buscar.Btn_Atras)
        self.ui.push_Adelante.clicked.connect(lambda: V_Buscar.Btn_Adelante)

        # Menú Principal
        self.ui.push_Repuesto.clicked.connect(lambda: V_Buscar.Btn_Repuesto)
        self.ui.push_Bazar.clicked.connect(lambda: V_Buscar.Btn_Bazar)
        self.ui.push_Aventas.clicked.connect(lambda: V_Buscar.Btn_Aventas)
        self.ui.push_PedidosEsp.clicked.connect(lambda: V_Buscar.Btn_PedidosEsp)
        self.ui.push_Otros.clicked.connect(lambda: V_Buscar.Btn_Otros)
        # Menú Secundario
        self.ui.push_op1.clicked.connect(lambda: V_Buscar.Btn_op1)
        self.ui.push_op2.clicked.connect(lambda: V_Buscar.Btn_op2)
        self.ui.push_op3.clicked.connect(lambda: V_Buscar.Btn_op3)
        self.ui.push_op4.clicked.connect(lambda: V_Buscar.Btn_op4)
        self.ui.push_op5.clicked.connect(lambda: V_Buscar.Btn_op5)
        self.ui.push_op6.clicked.connect(lambda: V_Buscar.Btn_op6)
        self.ui.push_op7.clicked.connect(lambda: V_Buscar.Btn_op7)

        # Botones de Imagenes
        self.ui.push_1.clicked.connect(lambda: V_Buscar.Boton1)
        self.ui.push_2.clicked.connect(lambda: V_Buscar.Boton2)
        self.ui.push_3.clicked.connect(lambda: V_Buscar.Boton3)
        self.ui.push_4.clicked.connect(lambda: V_Buscar.Boton4)
        self.ui.push_5.clicked.connect(lambda: V_Buscar.Boton5)
        self.ui.push_6.clicked.connect(lambda: V_Buscar.Boton6)
        self.ui.push_7.clicked.connect(lambda: V_Buscar.Boton7)
        self.ui.push_8.clicked.connect(lambda: V_Buscar.Boton8)
        self.ui.push_9.clicked.connect(lambda: V_Buscar.Boton9)
        self.ui.push_10.clicked.connect(lambda: V_Buscar.Boton10)
        self.ui.push_11.clicked.connect(lambda: V_Buscar.Boton11)
        self.ui.push_12.clicked.connect(lambda: V_Buscar.Boton12)
        self.ui.push_13.clicked.connect(lambda: V_Buscar.Boton13)
        self.ui.push_14.clicked.connect(lambda: V_Buscar.Boton14)
        self.ui.push_15.clicked.connect(lambda: V_Buscar.Boton15)
        self.ui.push_16.clicked.connect(lambda: V_Buscar.Boton16)
        self.ui.push_17.clicked.connect(lambda: V_Buscar.Boton17)
        self.ui.push_18.clicked.connect(lambda: V_Buscar.Boton18)
        self.ui.push_19.clicked.connect(lambda: V_Buscar.Boton19)
        self.ui.push_20.clicked.connect(lambda: V_Buscar.Boton20)

        # Lista con las variables de la ventana
        self.Lista_vtn_buscar = []
        '''
        LISTABUSCAR > Es la lista completa de elementos que se buscaron. Si por ejemplo se buscaron 34 productos, la lista tiene los 34 productos a pesar de que en pantalla 
        sólo figuran de a 20 productos. Desde ahí se nutre el programa para saber qué productos hay que mostrar en pantalla.
        LISTABPOS > Es la lista de las posiciones que existen con colores pintados. Por ejemplo, si estamos en una lista de elementos que están mostrados en pantalla y 
        presionamos otro botón que cambia los productos mostrados, ésta lista le indica los botones que están seleccionados para saber cuáles hay que des-seleccionar. Por el 
        contrario si la lista está vacía es porque no hay nada en pantalla seleccionado. Es importante aclarar que ésta lista tiene la finalidad de tener el aviso, una bandera 
        que indica qué está seleccionado actualmente y no sirve para más nada. Además importante aclarar que cada valor en la lista representa la posición de un botón, que van 
        del 1 al 20.

        ATENCIÓN QUE ES DEL MÓDULO DE VARIABLES:
        mi_vars.LISTABUSCADO > Es una lista global que acumula todos los productos en que se tienen interés y se han buscado. Luego al abrir por ejemplo la ventana de combos, 
        la misma tiene acceso a ésta lista y carga lo que se seleccionó en ésta ventana.
        '''
        # Pos 0: LISTABUSCAR = []
        # Pos 1: LISTABPOS = []
        self.Lista_vtn_buscar.append([])
        self.Lista_vtn_buscar.append([])

        # Indica a los botones de Anterior y Siguiente cuál es el Inicio de la lista
        # Pos 2: self.INICIOLISTABUSCAR = 0
        self.Lista_vtn_buscar.append(0)

        # Variable para saber si se cierra la ventana desde el botón de CARGAR, de lo contrario, no hay que llevar datos
        # Pos 3: self.VUELVE_CARGAR = False
        self.Lista_vtn_buscar.append(False)

        # Cargamos en ésta variable el botón que se apretó, para que si se vuelve a apretar el mismo no se realice todo el proceso de carga de datos
        # Pos 4: self.BOTON_APRETADO = -1
        self.Lista_vtn_buscar.append(-1)

        self.ui.push_Atras.setEnabled(False)
        self.ui.push_Adelante.setEnabled(False)

# Clase que convierte un Label en un botón
class QlabelClickeable(QLabel):

    # "clicked" es un evento que lo nombré así sólo porque en los botones se llama así y mantengo el nombre, pero podría ponerle cualquier nombre. Cuando se presiona el label, se emite una señal a éste evento entonces cuando tengamos que conectarlo a una función, hacemos igual que los botones ej: self.label.clicked.connect(self.funcion).
    # En PyQt5 ésta misma sintaxis sería: clicked = QtCore.pyqtSignal(str)
    # El parámetro str, es un valor que puede utilizarse para reconocer el botón que se ha presionado por ejemplo.
    clicked = QtCore.Signal(str)

    flotar = QtCore.Signal(bool)
    retirar = QtCore.Signal(bool)

    def __init__(self, Lista=[], parent=None):
        super(QlabelClickeable, self).__init__(parent)

        

        # Una lista que contiene adentro listas de 3 números enteros (RGB) de los colores que queremos tener para cada evento.
        # Luego tiene una lista con varios valores para configurar otros atributos.
            # pos0 = Color normal
            # pos1 = Color boton apretado
            # pos2 = Color mouse hover
            # pos3 = grosor del borde normal / apretado / hover
            # pos4 = color del borde normal
            # pos5 = color del borde apretado
            # pos6 = color del borde hover
            # pos7 = width/height boton normal
            # pos8 = width/height boton expandido
            # pos9 = Texto del boton normal/apretado/hover
            # pos10 = Texto de ToolTip

        if len(Lista) > 0:
            self.lista_val = Lista
        else:
            self.lista_val.append([85,85,85])       # 0
            self.lista_val.append([255,92,225])     # 1
            self.lista_val.append([45,45,45])       # 2
            self.lista_val.append([1,1,1])          # 3
            self.lista_val.append([85,85,85])       # 4
            self.lista_val.append([0,0,0])          # 5
            self.lista_val.append([0,0,0])          # 6
            self.lista_val.append([80,60])          # 7
            self.lista_val.append([80,60])          # 8
            self.lista_val.append(["","",""])       # 9
            self.lista_val.append("")               # 10
        
        if self.lista_val[10] != "":
            self.setToolTip(self.lista_val[10])
        
        self.setMinimumSize(self.lista_val[7][0], self.lista_val[7][1])
        self.setMaximumSize(self.lista_val[8][0], self.lista_val[8][1])

        # Bandera para indicarle a leaveEvent y enterEvent que no deben reconfigurar el botón mientras esté apretado
        self.apretado = False

        # Indicamos que el boton responde a un cambio si es que es apretado
        self.seApreta = True

        self.configuraBoton(0)

    def leaveEvent(self, event):
        '''Evento de retirar el mouse de encima del label'''
        print("mouse out")
        #if self.apretado == False:
        #    self.configuraBoton(0)
        self.retirar.emit(True)

    # Evento cuando el mouse hace clic sobre el label
    def mousePressEvent(self, event):
        '''Evento Clic en un label'''
        print("Press")
        if self.seApreta == True:
            self.configuraBoton(1)
        self.apretado = True
        self.clicked.emit("Clic")
    
    # Evento que se ejecuta casi siempre que se ejecuta otro evento, no le encontré utilidad pero puede ser útil en algún momento.
    def mouseReleaseEvent(self, event):
        '''Evento que se ejecuta cada vez que se ejecuta otro evento'''
        print("Release")
    
    def enterEvent(self, event):
        '''Evento de pasar con el mouse por encima en un label'''
        print("Move")
        #if self.apretado == False:
        #    self.configuraBoton(2)
        self.flotar.emit(True)

    def configuraBoton(self, tipo):
        '''Configura el botón según los valores del parametro tipo(0=Normal / 1=Apretado / 2=MouseHover)'''
        
        lista_back = []
        solid = int
        lista_borde = []
        texto = str

        # Modo normal - o cuando se lo quiere llevar a ese modo luego de dejar de estar apretado el botón
        lista_back = self.lista_val[tipo]
        solid = self.lista_val[3][tipo]
        lista_borde = self.lista_val[4 + tipo]

        # Edita el texto que tiene el label
        #if self.text() != self.lista_val[9][tipo]:
        #    self.setText(self.lista_val[9][tipo])
        
        self.apretado = False

        self.setStyleSheet("background-color: rgb({},{},{});border: {}px solid;border-color: rgb({},{},{});".format(lista_back[0],lista_back[1],lista_back[2],solid,lista_borde[0],lista_borde[1],lista_borde[2]))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())