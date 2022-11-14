import RegistrationWindow as Rw
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap


class Authorize(QMainWindow):
    def __init__(self):
        super(Authorize, self).__init__()
        uic.loadUi("ui/authorize.ui", self)

        pixmap = QPixmap("pictures/Yandex_Lyceum_logo.png").scaled(430, 80)
        self.image_label.setPixmap(pixmap)

        self.create_card_window = None
        self.registration_window = None

        self.authorize_button.clicked.connect(self.log_in)
        self.registration_button.clicked.connect(self.registration_redirect)

    def log_in(self):
        self.close()

    def registration_redirect(self):
        self.registration_window = Rw.Registration()
        self.registration_window.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    auth = Authorize()
    auth.show()
    sys.exit(app.exec())
