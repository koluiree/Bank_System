import RegistrationWindow as Rw
import PasswordGenerator as Pg
import PersonalCabinet as Pc
import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap


class Authorize(QMainWindow):
    def __init__(self):
        super(Authorize, self).__init__()
        uic.loadUi("ui/authorize.ui", self)

        # Создаю переменные в которых будут храниться окна для дальнейшего перенаправления
        self.create_card_window = None
        self.registration_window = None
        self.personal_cabinet = None

        self.authorize_button.clicked.connect(self.log_in)
        self.registration_button.clicked.connect(self.registration_redirect)

    def log_in(self):
        con = sqlite3.connect("bank_info.sqlite")
        cur = con.cursor()
        try:
            login, password = self.login_edit.text(), self.password_edit.text() # Получаю логин и пароль введенные пользователем

            password_db = cur.execute(f"""SELECT password FROM account_info 
            WHERE login == '{login}'""").fetchone()[0]
            # Получаю пароль из базы данных по индивидуальному номеру и сверяю его с введенным пользователем паролем
            if password_db != password:
                raise Pg.LetterError

            con.close()

            self.personal_cabinet = Pc.PersonalCabinet(login)
            self.personal_cabinet.show()
            self.close()
        except Exception as e:
            print(e)
            self.error_label.setText("Данные введены неверно")

    def registration_redirect(self):
        self.registration_window = Rw.Registration()
        self.registration_window.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    auth = Authorize()
    auth.show()
    sys.exit(app.exec())
