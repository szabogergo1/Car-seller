from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QMessageBox

from modifywindow_minta import Ui_ModifyWindow


class ModifyWindow(QDialog, Ui_ModifyWindow):

    def __init__(self, data, all_car, parent=None):
        super(ModifyWindow, self).__init__(parent)
        self.setupUi(self)

        self.data = data
        self.all_car = all_car

        self.pushButton_modify.clicked.connect(self.modify)
        self.pushButton_cancel.clicked.connect(self.close)

        self.modify_car = []

        if len(self.data) > 0:
            self.lineEdit_ident.setText(self.data[0][0])
            self.lineEdit_brand.setText(self.data[0][1])
            self.lineEdit_type.setText(self.data[0][2])
            self.lineEdit_price.setText(str(self.data[0][3]))
            self.lineEdit_number.setText(self.data[0][4])
            self.lineEdit_location.setText(self.data[0][5])

    def modify(self):
        identification = self.lineEdit_ident.text()
        brand = self.lineEdit_brand.text()
        car_type = self.lineEdit_type.text()
        price = self.lineEdit_price.text()
        number = self.lineEdit_number.text()
        location = self.lineEdit_location.text()

        r = True
        pr = 0

        for i in range(len(self.all_car)):
            if identification == self.all_car[i][0]:
                QMessageBox.about(self, "Hiba", "Már létezik ilyen azonosítójú autó!")
                r = False
            elif number == self.all_car[i][4]:
                QMessageBox.about(self, "Hiba", "Már létezik ilyen alvázszámú autó!")
                r = False

        try:
            pr = int(price)
        except ValueError:
            QMessageBox.about(self, "Hiba", "Az árban nem szerepelhetnek betűk!")
            r = False

        if r:
            self.modify_car = (identification, brand, car_type, pr, number, location)
            self.accept()

