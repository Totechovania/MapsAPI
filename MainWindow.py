from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
from map_api_form import Ui_MainWindow
import requests
from io import BytesIO
from PIL import Image


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_UI()

    def init_UI(self):
        self.ll = list(map(float, input().split()))
        self.scale = float(input())
        self.MIN_SCALE = 0.0005
        self.MAX_SCALE = 0.1

        self.update_map()

    def get_map(self):
        map_params = {
            "ll": ",".join(map(str, self.ll)),
            "spn": ",".join(map(str, (self.scale, self.scale))),
            "l": "map"
        }

        map_api_server = "http://static-maps.yandex.ru/1.x/"

        response = requests.get(map_api_server, params=map_params)

        return response

    def update_map(self):
        response = self.get_map()
        if response:
            img = response.content

            pixmap = QPixmap()
            pixmap.loadFromData(img)

            self.label.setPixmap(pixmap)

    def set_scale(self, scale):
        self.scale = max(self.MIN_SCALE, min(self.MAX_SCALE, scale))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            previous = self.scale
            self.set_scale(self.scale + 0.0005)
            if self.scale != previous:
                self.update_map()
        elif event.key() == Qt.Key_PageDown:
            previous = self.scale
            self.set_scale(self.scale - 0.0005)
            if self.scale != previous:
                self.update_map()


