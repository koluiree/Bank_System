import DataCheck as Dc
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

        self.generate_password_button.clicked.connect(self.generate_password)
        self.previous_window_button.clicked.connect(self.redirect_to_main)
        self.next_stage_button.clicked.connect(self.registration)

    def registration(self):
        # Флаги для проверки пароля и логина, введенных пользователем
        login_flag = False
        password_flag = False

        try:
            Dc.check_login(self.login_edit.text())
            Dc.check_login_exists(self.login_edit.text())
            login_flag = True
        except Dc.LengthError:
            self.error_label.setText('Длина логина меньше 4 символов!')
        except Dc.LetterError:
            self.error_label.setText('Логин содержит недопустимые символы!')
        except Dc.LoginError:
            self.error_label.setText('Логин занят')

        if login_flag:
            try:
                Dc.check_password(self.password_edit.text())
                password_flag = True
            except Dc.LengthError:
                self.error_label.setText('Длина пароля меньше 8 символов!')
            except Dc.LetterError:
                self.error_label.setText('Ошибка в структуре пароля!')
            except Dc.DigitError:
                self.error_label.setText('Пароль не содержит цифр!')

            if self.password_edit.text() != self.confirm_password_edit.text():
                self.error_label.setText('Пароли не совпадают!')
                password_flag = False
        # Если пароль с логином оказались подходящими, перенаправив на функции запоминания данных и смены окна
        if password_flag and login_flag:
            self.account_data()
            self.next_stage()

    def generate_password(self):
        random_password = Dc.generate(randint(10, 16))
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
        DATA = (self.login_edit.text(), self.password_edit.text())  # Запоминаются данные пользователя
