from PyQt5 import QtWidgets
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

    def openFile(self):
        self.cars = []
        name, _ = QFileDialog.getOpenFileName(self, 'Open File', options=QFileDialog.DontUseNativeDialog)
        with open(name) as f:
            lines = f.readlines()
        lines = [line.rstrip('\n') for line in lines]
        for line in lines:
            words = line.split(" ")
            d = (words[0], words[1], words[2], int(words[3]), words[4], words[5])
            self.cars.append(d)

        self.sort_cars()
        self.fillTable()

        self.comboBox_type.addItems()

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
            self.fillTable()

    def modifyCar(self):
        indexes = self.tableWidget.selectionModel().selectedRows()
        tmp = []
        for index in sorted(indexes):
            for i in range(len(self.cars)):
                if index.data() == self.cars[i][0]:
                    tmp.append(self.cars[i])
                    break
            my_list = list(self.cars)
            my_list.remove(tmp[0])
            self.cars = my_list

        modifyCar = ModifyWindow(tmp, self.cars)
        if modifyCar.exec_() == QDialog.Accepted:
            self.cars.append(modifyCar.modify_car)
            self.sort_cars()
            self.fillTable()

    def sort_cars(self):
        for i in range(len(self.cars) - 1):
            for j in range(i + 1, len(self.cars)):
                if self.cars[i][3] > self.cars[j][3]:
                    a = self.cars[i]
                    self.cars[i] = self.cars[j]
                    self.cars[j] = a


app = QtWidgets.QApplication(sys.argv)
form = MainWindow()
form.show()
sys.exit(app.exec_())
