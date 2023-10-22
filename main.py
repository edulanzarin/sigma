import sys
from PyQt5.QtWidgets import QApplication
from login_window import LoginWindow
from main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    main_window = None  # Inicialmente, a janela principal é definida como None

    def on_login_success():
        nonlocal main_window  # Utilize a variável main_window fora do escopo local
        login_window.close()  # Fecha a janela de login
        main_window = MainWindow()
        main_window.show()

    login_window = LoginWindow()
    login_window.login_success.connect(on_login_success)
    login_window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
