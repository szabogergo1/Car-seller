from PyQt5 import QtWidgets, QtGui
import sys

from PyQt5.QtWidgets import QAction, QFileDialog, QInputDialog, QDialog, QAbstractItemView

from mainwindow_minta import Ui_MainWindow
from addwindow import AddWindow
from modifywindow import ModifyWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.pushButton_delete.clicked.connect(self.deleteCar)
        self.pushButton_add.clicked.connect(self.addCar)
        self.pushButton_modify.clicked.connect(self.modifyCar)
        self.pushButton_search.clicked.connect(self.searchCar)

        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        menuBar = self.menuBar()
        filelMenu = menuBar.addMenu('&Fájl')
        fileOpen = QAction('&Megnyitás', self)
        fileOpen.triggered.connect(self.openFile)

        fileSave = QAction('&Mentés', self)
        fileSave.triggered.connect(self.saveFile)

        filelMenu.addAction(fileOpen)
        filelMenu.addAction(fileSave)

        self.cars = []
        self.type_list = []
        self.price_list = []
        self.brand_list = []

    def openFile(self):
        name, _ = QFileDialog.getOpenFileName(self, 'Open File', options=QFileDialog.DontUseNativeDialog)
        if name:
            self.cars = []
            with open(name) as f:
                lines = f.readlines()
            lines = [line.rstrip('\n') for line in lines]
            for line in lines:
                words = line.split(" ")
                d = (words[0], words[1], words[2], int(words[3]), words[4], words[5])
                self.cars.append(d)

            self.sort_cars()
            self.fillTable()

            self.comboBox_brand.clear()
            self.comboBox_type.clear()
            self.comboBox_price.clear()

            self.brand_list = []
            self.type_list = []
            self.price_list = []

            for i in range(len(self.cars)):
                if self.cars[i][1] not in self.brand_list:
                    self.brand_list.append(self.cars[i][1])

                if self.cars[i][2] not in self.type_list:
                    self.type_list.append(self.cars[i][2])

                if self.cars[i][3] not in self.price_list:
                    self.price_list.append(self.cars[i][3])

            self.comboBox_brand.addItems(self.brand_list)
            self.comboBox_type.addItems(self.type_list)
            self.sort_price()
            string_price_list = (str(j) for j in self.price_list)
            self.comboBox_price.addItems(string_price_list)

    def fillTable(self):
        self.tableWidget.setRowCount(len(self.cars))
        for i in range(len(self.cars)):
            for j in range(6):
                cells = QtWidgets.QTableWidgetItem()
                cells.setText(str(self.cars[i][j]))
                self.tableWidget.setItem(i, j, cells)

    def saveFile(self):
        f = open("SavedData.txt", "w")

        rows = self.tableWidget.rowCount()
        for i in range(rows):
            d = []
            for j in range(6):
                d.append(self.tableWidget.item(i, j).text())

            for k in range(6):
                if k < 5:
                    print(f"{d[k]} ", end="", file=f)
                else:
                    print(f"{d[k]}", file=f)

    def deleteCar(self):
        indexes = self.tableWidget.selectionModel().selectedRows()
        tmp = []
        for index in sorted(indexes):
            for i in range(len(self.cars)):
                if index.data() != self.cars[i][0]:
                    tmp.append(self.cars[i])

        self.cars = tmp
        self.fillTable()

    def addCar(self):
        addNewItem = AddWindow(self.cars)
        if addNewItem.exec_() == QDialog.Accepted:
            self.cars.append(addNewItem.add_new)
            self.sort_cars()

            for i in range(len(self.cars)):
                if self.cars[i][1] not in self.brand_list:
                    self.brand_list.append(self.cars[i][1])

                if self.cars[i][2] not in self.type_list:
                    self.type_list.append(self.cars[i][2])

                if self.cars[i][3] not in self.price_list:
                    self.price_list.append(self.cars[i][3])

            self.comboBox_brand.clear()
            self.comboBox_type.clear()
            self.comboBox_price.clear()

            self.comboBox_brand.addItems(self.brand_list)
            self.comboBox_type.addItems(self.type_list)
            self.sort_price()
            string_price_list = (str(j) for j in self.price_list)
            self.comboBox_price.addItems(string_price_list)

            self.fillTable()

    def modifyCar(self):
        indexes = self.tableWidget.selectionModel().selectedRows()
        tmp = []
        if indexes:
            for index in sorted(indexes):
                for i in range(len(self.cars)):
                    if index.data() == self.cars[i][0]:
                        tmp.append(self.cars[i])
                        break
                my_list = list(self.cars)
                my_list.remove(tmp[0])
                self.cars = my_list
                self.brand_list.remove(tmp[0][1])
                self.type_list.remove(tmp[0][2])
                self.price_list.remove(tmp[0][3])
                self.comboBox_brand.clear()
                self.comboBox_type.clear()
                self.comboBox_price.clear()

            modify_Car = ModifyWindow(tmp, self.cars)
            if modify_Car.exec_() == QDialog.Accepted:
                self.cars.append(modify_Car.modify_car)
                self.sort_cars()
                self.fillTable()
                for i in range(len(self.cars)):
                    if self.cars[i][1] not in self.brand_list:
                        self.brand_list.append(self.cars[i][1])

                    if self.cars[i][2] not in self.type_list:
                        self.type_list.append(self.cars[i][2])

                    if self.cars[i][3] not in self.price_list:
                        self.price_list.append(self.cars[i][3])

                self.comboBox_brand.addItems(self.brand_list)
                self.comboBox_type.addItems(self.type_list)
                self.sort_price()
                string_price_list = (str(j) for j in self.price_list)
                self.comboBox_price.addItems(string_price_list)
            else:
                self.cars.append(tmp[0])
                self.sort_cars()
                self.fillTable()
                self.brand_list.append(tmp[0][1])
                self.type_list.append(tmp[0][2])
                self.price_list.append(tmp[0][3])
                self.comboBox_brand.addItems(self.brand_list)
                self.comboBox_type.addItems(self.type_list)
                self.sort_price()
                string_price_list = (str(j) for j in self.price_list)
                self.comboBox_price.addItems(string_price_list)

    def searchCar(self):
        brand = self.comboBox_brand.currentText()
        car_type = self.comboBox_type.currentText()
        price = self.comboBox_price.currentText()

        for i in range(len(self.cars)):
            for j in range(self.tableWidget.columnCount()):
                self.tableWidget.item(i, j).setBackground(QtGui.QColor('white'))

        for i in range(len(self.cars)):
            if brand == self.cars[i][1] and car_type == self.cars[i][2] and int(price) >= self.cars[i][3]:
                for j in range(self.tableWidget.columnCount()):
                    self.tableWidget.item(i, j).setBackground(QtGui.QColor('yellow'))

    def sort_cars(self):
        for i in range(len(self.cars) - 1):
            for j in range(i + 1, len(self.cars)):
                if self.cars[i][3] > self.cars[j][3]:
                    a = self.cars[i]
                    self.cars[i] = self.cars[j]
                    self.cars[j] = a

    def sort_price(self):
        for i in range(len(self.price_list)-1):
            for j in range(i+1, len(self.price_list)):
                if self.price_list[i] > self.price_list[j]:
                    tmp = self.price_list[i]
                    self.price_list[i] = self.price_list[j]
                    self.price_list[j] = tmp


app = QtWidgets.QApplication(sys.argv)
form = MainWindow()
form.show()
sys.exit(app.exec_())
