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
from PyQt5.QtCore import Qt

from connect_banco import conectar_banco
from error_window import MyErrorMessage


class CadastroConciliacaoWindow(QWidget):
    def __init__(self, selected_empresa):
        super().__init__()
        self.selected_empresa = selected_empresa

        # Defina o ícone da janela
        icon = QIcon(r".\assets\cadastro.png")
        self.setWindowIcon(icon)

        self.setWindowTitle("Cadastrar Conciliação")
        self.setGeometry(250, 250, 450, 300)

        layout = QVBoxLayout()

        self.label_descricao = QLabel("Descrição")
        self.text_descricao = QLineEdit()

        self.label_debito = QLabel("Conta débito")
        self.text_debito = QLineEdit()

        self.label_credito = QLabel("Conta crédito")
        self.text_credito = QLineEdit()

        self.button_cadastrar = QPushButton("Cadastrar")
        self.button_cadastrar.clicked.connect(self.cadastrar_button_clicked)

        self.message_label = QLabel("")

        layout.addWidget(self.label_descricao)
        layout.addWidget(self.text_descricao)
        layout.addWidget(self.label_debito)
        layout.addWidget(self.text_debito)
        layout.addWidget(self.label_credito)
        layout.addWidget(self.text_credito)
        layout.addWidget(self.button_cadastrar)
        layout.addWidget(self.message_label)

        self.setLayout(layout)

        # Adicione um atalho de teclado para o botão
        enter_shortcut = QKeySequence(Qt.Key_Return)
        self.button_cadastrar.setShortcut(enter_shortcut)

    def cadastrar_button_clicked(self):
        # 1. Extrair os valores dos campos de texto
        descricao = self.text_descricao.text()
        debito = self.text_debito.text()
        credito = self.text_credito.text()

        try:
            # 3. Consultar o banco de dados para obter o id_empresa
            conn = conectar_banco()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id_empresa FROM empresas WHERE nome_empresa = %s",
                (self.selected_empresa,),
            )
            result = cursor.fetchone()

            if result:
                id_empresa = result[0]

                # 4. Inserir os valores na tabela
                table_name = f"conciliacao_{id_empresa}"
                cursor.execute(
                    f"INSERT INTO {table_name} (descricao, conta_debito, conta_credito) VALUES (%s, %s, %s)",
                    (descricao, debito, credito),
                )

                conn.commit()
                conn.close()

                # Limpar os campos de texto após a inserção bem-sucedida
                self.text_descricao.clear()
                self.text_debito.clear()
                self.text_credito.clear()

            else:
                # Lidar com o caso em que o id_empresa não foi encontrado
                error_message = MyErrorMessage()
                error_message.showMessage("Id da empresa não encontrado.")
                error_message.exec_()

        except Exception as e:
            error_message = MyErrorMessage()
            error_message.showMessage("Erro ao cadastrar conciliações: " + str(e))
            error_message.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CadastroConciliacaoWindow()
    window.show()
    sys.exit(app.exec_())
