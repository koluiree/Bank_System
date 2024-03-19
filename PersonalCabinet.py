import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5.QtGui import QPixmap


class PersonalCabinet(QMainWindow):
    def __init__(self, active_account):
        super(PersonalCabinet, self).__init__()
        uic.loadUi("ui/personal_cabinet.ui", self)

        self.active_account = active_account

        con = sqlite3.connect("bank_info.sqlite")
        cur = con.cursor()

        data = cur.execute(f"""SELECT card_number, cvv2, validity, pay_system, balance FROM account_info
        WHERE login == '{self.active_account}'""").fetchone()

        card: str = data[0]
        cvv2: int = data[1]
        validity: str = data[2]
        pay_system: int = data[3]
        balance: int = data[4]
        # выносим платёжную систему пользователя, для того чтобы указать ее на картинке в личном кабинете
        pay_system: str = cur.execute(f"""SELECT systems FROM pay_systems WHERE id == {pay_system}""").fetchone()[0]

        # тоже самое с остальными данными
        name = cur.execute(f"""SELECT translated_name, translated_surname FROM user_info
        WHERE login == '{self.active_account}'""").fetchone()
        con.close()

        # костыль для создания красивых разделений у номера карты :)
        card_on_label = ''
        for i, num in zip(str(card), range(17)):
            if num % 4 == 0:
                card_on_label += '     ' + i
            else:
                card_on_label += i

        name = ' '.join(name)

        # сбор всех данных и вывод их в окно
        self.name_label.setText(name)
        self.card_number_label.setText(card_on_label.lstrip())
        self.cvv2_label.setText(str(cvv2))
        self.validity_label.setText(validity)
        self.pay_system_label.setText(pay_system.upper())
        self.balance_label.setText(str(balance) + ' тугриков')
        self.update_transactions_table()

    def update_balance(self):
        pass

    def only_income_table(self):
        pass

    def only_outcome_table(self):
        pass

    def update_transactions_table(self):
        con = sqlite3.connect("bank_info.sqlite")
        cur = con.cursor()

        transactions: list = cur.execute(f"""SELECT from_user, to_user, amount FROM transactions
                WHERE to_user == '{self.active_account}' OR from_user == '{self.active_account}'""").fetchall()
        print(transactions)

        con.close()

        self.transactions_table.setColumnCount(3)
        self.transactions_table.setRowCount(len(transactions))
        self.transactions_table.setHorizontalHeaderLabels(["От кого", "Кому", "Сумма перевода"])

        for row_num in range(len(transactions)):
            self.transactions_table.setItem(row_num, 0, QTableWidgetItem(transactions[row_num][0]))
            self.transactions_table.setItem(row_num, 1, QTableWidgetItem(transactions[row_num][1]))
            self.transactions_table.setItem(row_num, 2, QTableWidgetItem(str(transactions[row_num][2])))

