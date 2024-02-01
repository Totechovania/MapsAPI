from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow
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
        response = self.get_map()

        img = response.content

        pixmap = QPixmap()
        pixmap.loadFromData(img)

        self.label.setPixmap(pixmap)

    def get_map(self):
        ll = input().split()
        scale = input()

        map_params = {
            "ll": ",".join(ll),
            "spn": ",".join([scale, scale]),
            "l": "map"
        }

        map_api_server = "http://static-maps.yandex.ru/1.x/"

        response = requests.get(map_api_server, params=map_params)

        return response


