from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QPixmap
import sys


class PersonalCabinet(QMainWindow):
    def __init__(self):
        super(PersonalCabinet, self).__init__()
        uic.loadUi("ui/personal_cabinet.ui", self)

        pixmap_card = QPixmap("pictures/Bank_card.png").scaled(400, 231)
        self.card_image.setPixmap(pixmap_card)


    def mouseMoveEvent(self, event):
        self.label.setText(f"Координаты: {event.x()}, {event.y()}")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    auth = PersonalCabinet()
    auth.show()
    sys.exit(app.exec())

