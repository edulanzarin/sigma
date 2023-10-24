from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication
from PyQt5.QtCore import Qt


class ProcessingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Processamento")
        self.setGeometry(0, 0, 100, 50)
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint)
        self.setWindowModality(Qt.ApplicationModal)

        # Centralize a janela na tela
        self.move(
            QApplication.desktop().screen().rect().center() - self.rect().center()
        )

        layout = QVBoxLayout()
        label = QLabel("Processando, por favor aguarde...")
        layout.addWidget(label)

        self.setLayout(layout)
