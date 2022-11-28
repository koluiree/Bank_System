import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPixmap


class PersonalCabinet(QMainWindow):
    def __init__(self, active_account):
        super(PersonalCabinet, self).__init__()
        uic.loadUi("ui/personal_cabinet.ui", self)

        pixmap_card = QPixmap("pictures/Bank_card.png").scaled(400, 231)
        self.card_image.setPixmap(pixmap_card)

        self.active_account = active_account

        con = sqlite3.connect("bank_info.sqlite")
        cur = con.cursor()

        card, cvv2, validity = cur.execute(f"""SELECT card_number, cvv2, validity FROM account_info
        WHERE individual_user_number == '{self.active_account}'""").fetchone()

        name = cur.execute(f"""SELECT translated_name, translated_surname FROM user_info
        WHERE individual_user_number == '{self.active_account}'""").fetchone()
        con.close()

        card_on_label = ''
        for i, num in zip(str(card), range(17)):
            if num % 4 == 0:
                card_on_label += '     ' + i
            else:
                card_on_label += i

        name = ' '.join(name)

        self.name_label.setText(name)
        self.card_number_label.setText(card_on_label)
        self.cvv2_label.setText(str(cvv2))
        self.validity_label.setText(validity)

