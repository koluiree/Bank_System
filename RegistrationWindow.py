import PasswordGenerator as Pg
import GenerateCardUi as GCui
import main as m

from random import randint

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPixmap

DATA = None

class Registration(QMainWindow):
    def __init__(self):
        super(Registration, self).__init__()
        uic.loadUi("ui/registration.ui", self)

        self.main_window = None
        self.generate_card_window = None


        pixmap = QPixmap("pictures/Yandex_Lyceum_logo.png").scaled(430, 80)

        self.image_label.setPixmap(pixmap)

        self.generate_password_button.clicked.connect(self.generate_password)
        self.previous_window_button.clicked.connect(self.redirect_to_main)
        self.next_stage_button.clicked.connect(self.registration)

    def registration(self):
        login_flag = False
        password_flag = False

        try:
            Pg.check_login(self.login_edit.text())
            login_flag = True
        except Pg.LengthError:
            self.error_label.setText('Длина логина должна быть не менее 4 символов!')
        except Pg.LetterError:
            self.error_label.setText('Логин содержит недопустимые символы!')

        if login_flag:
            try:
                Pg.check_password(self.password_edit.text())
                password_flag = True
            except Pg.LengthError:
                self.error_label.setText('Длина пароля должна быть не менее 8 символов!')
            except Pg.LetterError:
                self.error_label.setText('Ошибка в структуре пароля!')
            except Pg.DigitError:
                self.error_label.setText('Пароль не содержит цифр!')

            if self.password_edit.text() != self.confirm_password_edit.text():
                self.error_label.setText('Пароли не совпадают!')

        if password_flag and login_flag:
            self.account_data()
            self.next_stage()

    def generate_password(self):
        random_password = Pg.generate(randint(10, 16))
        self.password_edit.setText(random_password)
        self.confirm_password_edit.setText(random_password)

    def redirect_to_main(self):
        self.main_window = m.Authorize()
        self.main_window.show()
        self.close()

    def next_stage(self):
        self.generate_card_window = GCui.GenerateCard()
        self.generate_card_window.show()
        self.close()

    def account_data(self):
        global DATA
        DATA = (self.login_edit.text(), self.password_edit.text())
