from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QMessageBox

from addwindow_minta import Ui_AddWindow


class AddWindow(QDialog, Ui_AddWindow):

    def __init__(self, data, parent=None):
        super(AddWindow, self).__init__(parent)
        self.setupUi(self)

        self.data = data

        self.pushButton_add.clicked.connect(self.add)
        self.pushButton_cancel.clicked.connect(self.close)

        self.add_new = []

    def add(self):
        identification = self.lineEdit_ident.text()
        brand = self.lineEdit_brand.text()
        car_type = self.lineEdit_type.text()
        price = self.lineEdit_price.text()
        number = self.lineEdit_number.text()
        location = self.lineEdit_location.text()

        r = True
        pr = 0

        for i in range(len(self.data)):
            if identification == self.data[i][0]:
                QMessageBox.about(self, "Hiba", "Már létezik ilyen azonosítójú autó!")
                r = False
            elif number == self.data[i][4]:
                QMessageBox.about(self, "Hiba", "Már létezik ilyen alvázszámú autó!")
                r = False

        try:
            pr = int(price)
            if pr <= 0 or pr >= 15000000:
                QMessageBox.about(self, "Hiba", "Az ár 0-nál nagyobb és 15.000.000-nál kisebb!")
                r = False
        except ValueError:
            QMessageBox.about(self, "Hiba", "Az árban nem szerepelhetnek betűk!")
            r = False

        if r:
            self.add_new = (identification, brand, car_type, pr, number, location)
            self.accept()
