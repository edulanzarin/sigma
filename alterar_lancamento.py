from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
)
from datetime import datetime
from connect_banco import conectar_banco


class AlterarLancamentoDialog(QDialog):
    def __init__(self, transaction_id, transaction_data, selected_row):
        super().__init__()

        self.setWindowTitle("Editar Lançamento")
        self.setGeometry(100, 100, 400, 200)

        self.transaction_id = transaction_id
        self.transaction_data = transaction_data
        self.selected_row = selected_row

        self.debit_label = QLabel("Débito:")
        self.debit_edit = QLineEdit()
        self.debit_edit.setText(transaction_data[1])

        self.credit_label = QLabel("Crédito:")
        self.credit_edit = QLineEdit()
        self.credit_edit.setText(transaction_data[2])

        self.value_label = QLabel("Valor:")
        self.value_edit = QLineEdit()
        self.value_edit.setText(transaction_data[3])

        self.description_label = QLabel("Descrição:")
        self.description_edit = QLineEdit()
        self.description_edit.setText(transaction_data[4])

        # Botão para salvar as alterações
        self.save_button = QPushButton("Salvar")
        self.save_button.clicked.connect(self.save_changes)

        # Layout da janela de edição
        layout = QVBoxLayout()

        form_layout = QVBoxLayout()
        form_layout.addWidget(self.debit_label)
        form_layout.addWidget(self.debit_edit)
        form_layout.addWidget(self.credit_label)
        form_layout.addWidget(self.credit_edit)
        form_layout.addWidget(self.value_label)
        form_layout.addWidget(self.value_edit)
        form_layout.addWidget(self.description_label)
        form_layout.addWidget(self.description_edit)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)

        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        self.setLayout(layout)
        self.row_index = self.selected_row

    def save_changes(self):
        new_debit = self.debit_edit.text()
        new_credit = self.credit_edit.text()
        new_value = self.value_edit.text()
        new_description = self.description_edit.text()

        if self.row_index is not None and 0 <= self.row_index < len(
            self.transaction_data
        ):
            updated_transaction = self.transaction_data[self.row_index]

            # Ajuste a consulta SQL para incluir apenas a cláusula WHERE com base no id_transacao
            update_query = """
            UPDATE transacoes
            SET debito = %s, credito = %s, valor = %s, descricao = %s
            WHERE id_transacao = %s
            """

            conn = conectar_banco()
            cursor = conn.cursor()

            cursor.execute(
                update_query,
                (
                    new_debit,
                    new_credit,
                    new_value,
                    new_description,
                    updated_transaction[0],  # id_transacao
                ),
            )

            conn.commit()
            conn.close()

            self.accept()
        else:
            print("Índice fora dos limites da lista ou não definido")
