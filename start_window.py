import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSpacerItem,
    QSizePolicy,
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt

from register_window import RegisterWindow


class StartWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.register_window = None

        self.setGeometry(100, 100, 400, 200)

        layout = QHBoxLayout()

        left_container = QVBoxLayout()

        label = QLabel()
        label.setPixmap(QPixmap(r".\assets\sigmastart.png"))
        label.setAlignment(Qt.AlignCenter)
        left_container.addWidget(label, alignment=Qt.AlignTop)

        label2 = QLabel("Sigma")
        label2.setStyleSheet("QLabel {font-size: 20px; font: bold;}")
        label2.setAlignment(Qt.AlignCenter)
        left_container.addWidget(label2, alignment=Qt.AlignTop)

        left_container.addSpacerItem(
            QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        register_button = QPushButton("Cadastrar Novo Usuário")
        register_button.setFixedWidth(300)
        register_button.setStyleSheet(
            "QPushButton { min-height: 35px; font-size: 15px; font: bold; min-width: 200px; max-width: 200px;}"
        )
        register_button.clicked.connect(self.open_register_window)
        left_container.addWidget(register_button)
        left_container.addSpacerItem(
            QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        right_container = QVBoxLayout()

        image_label = QLabel()
        image_label.setPixmap(QPixmap(r".\assets\contador.png"))
        right_container.addWidget(image_label)
        right_container.setAlignment(Qt.AlignVCenter)

        spacer = QSpacerItem(300, 300, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addLayout(left_container)
        layout.addSpacerItem(spacer)
        layout.addLayout(right_container)

        self.setLayout(layout)

    def open_register_window(self):
        if not self.register_window:
            self.register_window = RegisterWindow()
        self.register_window.show()


def main():
    app = QApplication(sys.argv)
    start_window = StartWindow()
    start_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
