import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QLabel,
)
from PyQt5.QtGui import QIcon
from start_window import StartWindow
from empresas_menu import EmpresasWindow
from conciliacao_window import ConciliacaoWindow
from sql_window import SqlWindow

class MainWindow(QMainWindow):
    def __init__(self, id_usuario):
        super().__init__()

        self.id_usuario = id_usuario
        # Defina o ícone da janela
        icon = QIcon(r".\assets\icon.ico")
        self.setWindowIcon(icon)

        self.setWindowTitle("Sigma")
        self.setGeometry(100, 100, 800, 600)

        # Maximize a janela principal
        self.showMaximized()

        # Crie um widget central que será o conteúdo principal da janela
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Crie um layout principal para a janela (vertical) e defina a margem como zero
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Crie um menu no topo
        menu_bar = self.menuBar()

        # Crie abas usando QTabWidget
        self.tabs = QTabWidget()

        # Defina o alinhamento das abas para preencher todo o espaço disponível
        self.tabs.setTabPosition(QTabWidget.North)

        # Adicione abas
        tab1 = QWidget()
        tab2 = QWidget()
        tab3 = QWidget()
        tab4 = QWidget()

        self.tabs.addTab(tab1, "Início")
        self.tabs.addTab(tab2, "Empresas")
        self.tabs.addTab(tab3, "Conciliações")

        if id_usuario == 1:
            self.tabs.addTab(tab4, "SQL Query")  # Adicione a aba somente se id_usuario for igual a 1

        tab1_layout = QVBoxLayout()
        self.start_window = StartWindow()
        tab1_layout.addWidget(self.start_window)
        tab1.setLayout(tab1_layout)

        tab2_layout = QVBoxLayout()
        self.empresas_window = EmpresasWindow(id_usuario)
        tab2_layout.addWidget(self.empresas_window)
        tab2.setLayout(tab2_layout)

        tab3_layout = QVBoxLayout()
        self.conciliacao_window = ConciliacaoWindow()
        tab3_layout.addWidget(self.conciliacao_window)
        tab3.setLayout(tab3_layout)

        if id_usuario == 1:
            tab4_layout = QVBoxLayout()
            self.sql_window = SqlWindow(id_usuario)
            tab4_layout.addWidget(self.sql_window)
            tab4.setLayout(tab4_layout)

        # Defina o menu no topo
        self.setMenuBar(menu_bar)

        # Adicione o menu e as abas ao layout principal
        main_layout.addWidget(self.tabs)

        # Defina o layout principal como o layout da janela
        self.central_widget.setLayout(main_layout)

    def open_start_window(self):
        # Abre a StartWindow dentro da guia "Início"
        self.start_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Suponha que o ID do usuário seja passado como argumento da linha de comando
    user_id = int(sys.argv[1])
    window = MainWindow(user_id)
    window.show()
    sys.exit(app.exec_())
