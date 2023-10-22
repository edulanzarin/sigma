import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from register_window import RegisterWindow


class StartWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.register_window = (
            None  # Inicialmente, a janela de registro é definida como None
        )

        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        # Botão para cadastrar um novo usuário
        register_button = QPushButton("Cadastrar Novo Usuário")
        register_button.setFixedWidth(100)
        register_button.clicked.connect(self.open_register_window)

        layout.addWidget(register_button)
        self.setLayout(layout)

    def open_register_window(self):
        if not self.register_window:
            self.register_window = (
                RegisterWindow()
            )  # Crie a janela de cadastro de usuários se ainda não existir
        self.register_window.show()


def main():
    app = QApplication(sys.argv)
    start_window = StartWindow()
    start_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
