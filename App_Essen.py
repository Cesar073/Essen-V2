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

        self.initUI()

        self.ui.stackedWidget.setCurrentIndex(1)
    
    def initUI(self):
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

        # Colocamos esos botones en el layout del Frame de Menú imagen
        self.ui.verticalLayout.addWidget(l_btn_expande_1)
        self.ui.verticalLayout.addWidget(l_btn_expande_2)
        self.ui.verticalLayout.addWidget(l_btn_expande_3)
        self.ui.verticalLayout.addWidget(l_btn_expande_4)
        self.ui.verticalLayout.addWidget(l_btn_expande_5)
        self.ui.verticalLayout.addWidget(l_btn_expande_6)
        self.ui.verticalLayout.addWidget(l_btn_expande_7)
        self.ui.verticalLayout.addWidget(l_btn_expande_8)
        self.ui.verticalLayout.addWidget(l_btn_expande_9)

        # Cargamos las imágenes
        pixmap = QPixmap('./sources/img/icon/men.png').scaled(60,60)
        l_btn_expande_1.setPixmap(pixmap)
        l_btn_expande_1.setAlignment(Qt.AlignRight)
        l_btn_expande_1.setToolTip("Expande/Contrae")
        pixmap = QPixmap('./sources/img/icon/promo.png').scaled(60,60)
        l_btn_expande_2.setPixmap(pixmap)
        l_btn_expande_2.setAlignment(Qt.AlignRight)
        pixmap = QPixmap('./sources/img/icon/pedidos.png').scaled(60,60)
        l_btn_expande_3.setPixmap(pixmap)
        l_btn_expande_3.setAlignment(Qt.AlignRight)
        pixmap = QPixmap('./sources/img/icon/productos.png').scaled(60,60)
        l_btn_expande_4.setPixmap(pixmap)
        l_btn_expande_4.setAlignment(Qt.AlignRight)
        pixmap = QPixmap('./sources/img/icon/clientes.png').scaled(60,60)
        l_btn_expande_5.setPixmap(pixmap)
        l_btn_expande_5.setAlignment(Qt.AlignRight)
        pixmap = QPixmap('./sources/img/icon/stock.png').scaled(60,60)
        l_btn_expande_6.setPixmap(pixmap)
        l_btn_expande_6.setAlignment(Qt.AlignRight)
        pixmap = QPixmap('./sources/img/icon/recordatorios.png').scaled(60,60)
        l_btn_expande_7.setPixmap(pixmap)
        l_btn_expande_7.setAlignment(Qt.AlignRight)
        pixmap = QPixmap('./sources/img/icon/estado.png').scaled(60,60)
        l_btn_expande_8.setPixmap(pixmap)
        l_btn_expande_8.setAlignment(Qt.AlignRight)
        pixmap = QPixmap('./sources/img/icon/config.png').scaled(60,60)
        l_btn_expande_9.setPixmap(pixmap)
        l_btn_expande_9.setAlignment(Qt.AlignRight)





        # CREACIÓN COMPLETA DEL MENÚ 1 - IMAGENES:
        self.ui.frame_label.setFixedWidth(0)
        self.ui.frame_label.setStyleSheet("background-color: red;")

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

        # Colocamos esos botones en el layout del Frame de Menú leyenda
        self.ui.verticalLayout_2.addWidget(l_btn_leyenda_1)
        self.ui.verticalLayout_2.addWidget(l_btn_leyenda_2)
        self.ui.verticalLayout_2.addWidget(l_btn_leyenda_3)
        self.ui.verticalLayout_2.addWidget(l_btn_leyenda_4)
        self.ui.verticalLayout_2.addWidget(l_btn_leyenda_5)
        self.ui.verticalLayout_2.addWidget(l_btn_leyenda_6)
        self.ui.verticalLayout_2.addWidget(l_btn_leyenda_7)
        self.ui.verticalLayout_2.addWidget(l_btn_leyenda_8)
        self.ui.verticalLayout_2.addWidget(l_btn_leyenda_9)
        
        # Configuramos el texto que tendrá cada uno
        l_btn_leyenda_1.setText("Expande/Contrae")
        l_btn_leyenda_1.setFont(QtGui.QFont('Unispace', 14))
        #l_btn_leyenda_1.lista_val[9] = ["Expande / Contrae","Expande / Contrae","Expande / Contrae"]
        l_btn_leyenda_2.setText("Promociones")
        l_btn_leyenda_2.setFont(QtGui.QFont('Unispace', 14))
        #l_btn_leyenda_2.lista_val[9] = ["Promociones","Promociones","Promociones"]
        l_btn_leyenda_3.setText("Pedidos")
        l_btn_leyenda_3.setFont(QtGui.QFont('Unispace', 14))
        #l_btn_leyenda_3.lista_val[9] = ["Pedidos","Pedidos","Pedidos"]
        l_btn_leyenda_4.setText("Productos")
        l_btn_leyenda_4.setFont(QtGui.QFont('Unispace', 14))
        #l_btn_leyenda_4.lista_val[9] = ["Productos","Productos","Productos"]
        l_btn_leyenda_5.setText("Clientes")
        l_btn_leyenda_5.setFont(QtGui.QFont('Unispace', 14))
        #l_btn_leyenda_5.lista_val[9] = ["Clientes","Clientes","Clientes"]
        l_btn_leyenda_6.setText("Stock Interno")
        l_btn_leyenda_6.setFont(QtGui.QFont('Unispace', 14))
        #l_btn_leyenda_6.lista_val[9] = ["Stock Interno","Stock Interno","Stock Interno"]
        l_btn_leyenda_7.setText("Recordatorios")
        l_btn_leyenda_7.setFont(QtGui.QFont('Unispace', 14))
        #l_btn_leyenda_7.lista_val[9] = ["Recordatorios","Recordatorios","Recordatorios"]
        l_btn_leyenda_8.setText("Estado General")
        l_btn_leyenda_8.setFont(QtGui.QFont('Unispace', 14))
        l_btn_leyenda_9.setText("Configuración")
        l_btn_leyenda_9.setFont(QtGui.QFont('Unispace', 14))



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

        l_btn_expande_1.seApreta = False
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
        
        if pos == 1:
            # page_ventas
            self.ui.stackedWidget.setCurrentIndex(1)
        elif pos == 3:
            # page_productos
            self.ui.stackedWidget.setCurrentIndex(0)
        else:
            QMessageBox.information(self, "Atención!", "Sección en desarrollo", QMessageBox.Ok)

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