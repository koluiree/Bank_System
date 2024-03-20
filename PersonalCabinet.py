import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from datetime import datetime


# сортировка с помощью .sort(time, key=lambda a: и тут по времени из модуля datetime)

class PersonalCabinet(QMainWindow):
    def __init__(self, active_account):
        super(PersonalCabinet, self).__init__()
        uic.loadUi("ui/personal_cabinet.ui", self)

        self.active_account = active_account
        self.transfer_window = TransferInterface(self.active_account)

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
                card_on_label += '    ' + i
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

        self.incoming_button.clicked.connect(self.only_income_table)
        self.outcoming_button.clicked.connect(self.only_outcome_table)
        self.all_button.clicked.connect(self.update_transactions_table)
        self.transfer_button.clicked.connect(self.redirect_to_transfer)

    def update_balance(self):
        pass

    def only_income_table(self):
        con = sqlite3.connect("bank_info.sqlite")
        cur = con.cursor()

        income: list = cur.execute(f"""SELECT date, from_user, to_user, amount FROM transactions
                        WHERE to_user == '{self.active_account}'""").fetchall()

        con.close()

        self.transactions_table.setRowCount(len(income))

        for row_num in range(len(income) - 1, -1, -1):
            self.transactions_table.setItem(len(income) - row_num - 1, 0, QTableWidgetItem(income[row_num][0]))
            self.transactions_table.setItem(len(income) - row_num - 1, 1, QTableWidgetItem(income[row_num][1]))
            self.transactions_table.setItem(len(income) - row_num - 1, 2, QTableWidgetItem(income[row_num][2]))
            self.transactions_table.setItem(len(income) - row_num - 1, 3, QTableWidgetItem(str(income[row_num][3])))

    def only_outcome_table(self):
        con = sqlite3.connect("bank_info.sqlite")
        cur = con.cursor()

        outcome: list = cur.execute(f"""SELECT date, from_user, to_user, amount FROM transactions
                                    WHERE from_user == '{self.active_account}'""").fetchall()

        con.close()

        self.transactions_table.setRowCount(len(outcome))

        for row_num in range(len(outcome) - 1, -1, -1):
            self.transactions_table.setItem(len(outcome) - row_num - 1, 0, QTableWidgetItem(outcome[row_num][0]))
            self.transactions_table.setItem(len(outcome) - row_num - 1, 1, QTableWidgetItem(outcome[row_num][1]))
            self.transactions_table.setItem(len(outcome) - row_num - 1, 2, QTableWidgetItem(outcome[row_num][2]))
            self.transactions_table.setItem(len(outcome) - row_num - 1, 3, QTableWidgetItem(str(outcome[row_num][3])))

    def update_transactions_table(self):
        con = sqlite3.connect("bank_info.sqlite")
        cur = con.cursor()

        transactions: list = cur.execute(f"""SELECT date, from_user, to_user, amount FROM transactions
                    WHERE to_user == '{self.active_account}' OR from_user == '{self.active_account}'""").fetchall()

        con.close()

        self.transactions_table.setColumnCount(4)
        self.transactions_table.setRowCount(len(transactions))
        self.transactions_table.setHorizontalHeaderLabels(["Когда", "От кого", "Кому", "Сумма"])

        for row_num in range(len(transactions) - 1, -1, -1):
            self.transactions_table.setItem(len(transactions) - row_num - 1, 0,
                                            QTableWidgetItem(transactions[row_num][0]))
            self.transactions_table.setItem(len(transactions) - row_num - 1, 1,
                                            QTableWidgetItem(transactions[row_num][1]))
            self.transactions_table.setItem(len(transactions) - row_num - 1, 2,
                                            QTableWidgetItem(transactions[row_num][2]))
            self.transactions_table.setItem(len(transactions) - row_num - 1, 3,
                                            QTableWidgetItem(str(transactions[row_num][3])))

    def redirect_to_transfer(self):
        self.transfer_window.show()


class TransferInterface(QMainWindow):
    def __init__(self, active_account):
        super(TransferInterface, self).__init__()
        uic.loadUi('ui/transfer.ui', self)

        self.active_account = active_account
