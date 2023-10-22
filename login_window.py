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


class LoginWindow(QWidget):
    login_success = pyqtSignal()

    def __init__(self):
        super().__init__()

        # Defina o ícone da janela
        icon = QIcon(r".\assets\login.png")
        self.setWindowIcon(icon)

        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.label_user = QLabel("Usuário:")
        self.text_user = QLineEdit()

        self.label_password = QLabel("Senha:")
        self.text_password = QLineEdit()
        self.text_password.setEchoMode(QLineEdit.Password)

        self.button_login = QPushButton("Entrar")
        self.button_login.clicked.connect(self.login)

        self.message_label = QLabel("")

        layout.addWidget(self.label_user)
        layout.addWidget(self.text_user)
        layout.addWidget(self.label_password)
        layout.addWidget(self.text_password)
        layout.addWidget(self.button_login)
        layout.addWidget(self.message_label)

        self.setLayout(layout)

        # Adicione um atalho de teclado para o botão
        enter_shortcut = QKeySequence(Qt.Key_Return)
        self.button_login.setShortcut(enter_shortcut)

    def login(self):
        user = self.text_user.text()
        password = self.text_password.text()

        # Verificar as credenciais no banco de dados
        id_usuario = verificar_credenciais(user, password)

        if id_usuario:
            self.message_label.setText("Login bem-sucedido")
            # Emita o sinal de sucesso do login
            self.login_success.emit()
            # Obtenha o IP da máquina usando a função get_ip_address
            nome_computador = get_hostname()
            ip_computador = get_ip_address()
            hora_atual = get_hora_atual()
            # Registre o login com o IP
            registrar_login(id_usuario[0], hora_atual, ip_computador, nome_computador)
        else:
            self.message_label.setText("Falha no login")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
