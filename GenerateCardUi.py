import CardDataGenerator as Cdg
import RegistrationWindow as Rw
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPixmap


class GenerateCard(QMainWindow):
    def __init__(self):
        super(GenerateCard, self).__init__()
        uic.loadUi("ui/generating_card.ui", self)

        pixmap_mir = QPixmap("pictures/mir.png").scaled(100, 30)
        pixmap_visa = QPixmap("pictures/visa.png").scaled(100, 30)
        pixmap_mastercard = QPixmap("pictures/mastercard.png").scaled(100, 90)

        self.registration_window = None

        self.pay_system = False

        self.patronymic = ""
        self.card_data = ()

        self.mir_image.setPixmap(pixmap_mir)
        self.visa_image.setPixmap(pixmap_visa)
        self.mastercard_image.setPixmap(pixmap_mastercard)

        self.previous_window_button.clicked.connect(self.redirect_to_registration)
        self.create_button.clicked.connect(self.end_registration)

    def creating_card(self):
        for i in self.pay_system_button_group.buttons():
            if i.isChecked():
                self.pay_system = i.objectName()

        try:
            if self.name_edit.text() and self.surname_edit.text():
                full_name = f"{self.name_edit.text()} {self.surname_edit.text()}"
            else:
                raise Cdg.ImportNameError

            self.patronymic = self.patronymic_edit.text()
            Cdg.checking_data(self.patronymic)
            Cdg.checking_data(self.name_edit.text())
            Cdg.checking_data(self.surname_edit.text())

            if not self.pay_system:
                raise Cdg.PaySystemError

            self.card_data = Cdg.full_data_of_card(self.pay_system, full_name)
        except Cdg.ImportNameError:
            self.error_label.setText("Некорректно введены данные")
        except Cdg.PaySystemError:
            self.error_label.setText("Выберите банковскую систему")

    def end_registration(self):
        self.creating_card()
        con = sqlite3.connect("bank_info.sqlite")
        cur = con.cursor()
        account_data = Rw.DATA
        print(account_data)
        print(self.card_data)
        pay_system_key = cur.execute(f"SELECT id FROM pay_systems WHERE systems = '{self.pay_system}'").fetchone()[0]
        cur.execute(f"""INSERT INTO account_info (login, password, card_number, cvv2, validity)
        VALUES ('{account_data[0]}', '{account_data[1]}', '{self.card_data[0]}', {self.card_data[1]}, '{self.card_data[2]}'""")
        cur.execute(f"""INSERT INTO user_info VALUES ('{self.card_data[5]}', '{self.name_edit.text()}', '{self.surname_edit.text()}',
        '{self.patronymic}', '{self.card_data[3]}', '{self.card_data[4]}')""")

        con.commit()
        con.close()

    def redirect_to_registration(self):
        self.registration_window = Rw.Registration()
        self.registration_window.show()
        self.close()

