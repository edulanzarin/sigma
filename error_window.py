import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)
from PyQt5.QtGui import QKeySequence, QIcon
from PyQt5.QtCore import Qt, pyqtSignal
from login_function import (
    verificar_credenciais,
    registrar_login,
    get_hora_atual,
    get_hostname,
    get_ip_address,
)


class ErrorWindow(QWidget):
    login_success = pyqtSignal()

    def __init__(self):
        super().__init__()

        # Defina o ícone da janela
        icon = QIcon(r".\assets\error.png")
        self.setWindowIcon(icon)

        self.setWindowTitle("Erro")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.button_error = QPushButton("Ok")
        self.button_error.clicked.connect(self.close)

        self.message_label = QLabel("")

        layout.addWidget(self.button_error)
        layout.addWidget(self.message_label)

        self.setLayout(layout)

        # Adicione um atalho de teclado para o botão
        enter_shortcut = QKeySequence(Qt.Key_Return)
        self.button_error.setShortcut(enter_shortcut)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ErrorWindow()
    window.show()
    sys.exit(app.exec_())
