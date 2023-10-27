import sys
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QMainWindow,
    QTextEdit,
    QApplication
)

from connect_banco import conectar_banco
from error_window import MyErrorMessage

class SqlWindow(QMainWindow):
    def __init__(self, id_usuario):
        super().__init__()

        self.id_usuario = id_usuario

        self.setGeometry(100, 100, 600, 400)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.sql_input = QTextEdit()
        layout.addWidget(self.sql_input)

        self.execute_button = QPushButton("Execute")
        self.execute_button.clicked.connect(self.execute_sql)
        self.execute_button.setStyleSheet(
            "QPushButton {"
            "max-width: 50px;"
            "}"
        )
        layout.addWidget(self.execute_button)

        self.result_display = QTextEdit()
        layout.addWidget(self.result_display)

        central_widget.setLayout(layout)

    def load_user_id(self, id_usuario):
        # Este método será chamado para carregar o id_usuario
        self.id_usuario = id_usuario

    def execute_sql(self):
        sql_code = self.sql_input.toPlainText()

        # Replace these values with your MySQL server connection details
        conn = conectar_banco()

        cursor = conn.cursor()
        try:
            cursor.execute(sql_code)
            result = cursor.fetchall()
            conn.commit()
            self.result_display.setPlainText("\n".join(str(row) for row in result))
        except Exception as e:
            error_message = MyErrorMessage()
            error_message.showMessage(
                "Erro ao atualizar valores no banco de dados! " + str(e)
            )
            error_message.exec_()


        conn.close()

def main():
    app = QApplication(sys.argv)
    window = SqlWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()