import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication,
    QHeaderView,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QComboBox,
    QFileDialog,
    QMessageBox,
    QTableWidgetItem,
    QTableWidget,
    QErrorMessage,
    QInputDialog,
)
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy

from connect_banco import conectar_banco
from error_window import MyErrorMessage
from cadastro_conciliacao import CadastroConciliacaoWindow


class ConciliacaoWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Conciliações")
        self.setGeometry(100, 100, 800, 600)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        # Crie um layout horizontal para o ícone e o QComboBox de empresas
        layout_1 = QHBoxLayout()
        layout_1.setAlignment(Qt.AlignTop)

        # Adicione um ícone personalizado ao QComboBox de empresas
        icon_1 = QIcon(r".\assets\list.png")

        # Crie um QLabel para o ícone de empresas
        icon1_label = QLabel()
        icon1_label.setPixmap(icon_1.pixmap(18, 18))  # Defina o tamanho do ícone

        # Defina a política de dimensionamento do icon_label para ocupar 5% do espaço
        icon1_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Converta o valor em ponto flutuante para inteiro
        max_width = int(self.width() * 0.03)
        icon1_label.setMaximumWidth(max_width)  # 5% da largura da janela

        # Crie o QComboBox de empresas
        self.combo_empresas = QComboBox()

        layout_1.addWidget(icon1_label)
        layout_1.addWidget(self.combo_empresas)

        layout_3 = QHBoxLayout()
        layout_3.setAlignment(Qt.AlignTop)
        icon_3 = QIcon(r".\assets\excel.png")
        icon3_label = QLabel()
        icon3_label.setPixmap(icon_3.pixmap(18, 18))  # Defina o tamanho do ícone
        icon3_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        max_width = int(self.width() * 0.03)
        icon3_label.setMaximumWidth(max_width)  # 5% da largura da janela
        self.excel_label = QLabel(
            "Cadastro em massa - Formato das colunas no Excel (DESCRICAO | DEB | CRED)"
        )
        self.excel_label.setStyleSheet(
            "QLabel {"
            "border: 0.5px solid lightgray;"
            "border-radius: 5px;"
            "padding: 5px;"
            "font-size: 14rem;"  # Adicione sublinhado para indicar que é clicável
            "}"
        )
        self.excel_label.setCursor(
            Qt.PointingHandCursor
        )  # Mude o cursor para a mão ao passar por cima
        self.excel_label.setOpenExternalLinks(
            False
        )  # Impede que os links sejam abertos em um navegador externo
        self.excel_label.mousePressEvent = self.excel_cadastro

        layout_3.addWidget(icon3_label)
        layout_3.addWidget(self.excel_label)

        layout_2 = QHBoxLayout()
        layout_2.setAlignment(Qt.AlignTop)

        self.listar_button = QPushButton("Listar Conciliações")
        self.listar_button.clicked.connect(self.listar_button_clicked)
        self.listar_button.setStyleSheet(
            "QPushButton { min-width: 120px; font-size: 12px;}"
        )
        self.listar_button.setCursor(Qt.PointingHandCursor)

        self.cadastrar_button = QPushButton("Cadastrar Conciliações")
        self.cadastrar_button.clicked.connect(self.cadastrar_button_clicked)
        self.cadastrar_button.setStyleSheet(
            "QPushButton { min-width: 120px; font-size: 12px;}"
        )
        self.cadastrar_button.setCursor(Qt.PointingHandCursor)

        self.excel_button = QPushButton("Cadastrar Lista")
        self.excel_button.clicked.connect(self.cadastrar_lista_button_clicked)
        self.excel_button.setStyleSheet(
            "QPushButton { min-width: 120px; font-size: 12px;}"
        )
        self.excel_button.setEnabled(False)
        self.excel_button.setCursor(Qt.PointingHandCursor)

        layout_2.addStretch(1)
        layout_2.addWidget(self.listar_button)
        layout_2.addWidget(self.cadastrar_button)
        layout_2.addWidget(self.excel_button)
        layout_2.addStretch(1)

        layout_7 = QHBoxLayout()
        layout_7.setAlignment(Qt.AlignTop)
        icon7_label = QLabel()
        layout_7.addWidget(icon7_label)

        main_layout.addLayout(layout_1)
        main_layout.addLayout(layout_3)
        main_layout.addLayout(layout_2)
        main_layout.addLayout(layout_7)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(
            3
        )  # Cinco colunas: data, debito, credito, valor, descricao
        self.table_widget.setHorizontalHeaderLabels(["Descrição", "Débito", "Crédito"])
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.setSortingEnabled(True)
        self.table_widget.verticalHeader().setVisible(False)

        self.table_widget.itemDoubleClicked.connect(self.editar_celula)
        main_layout.addWidget(self.table_widget)

        self.load_empresas()
        self.setLayout(main_layout)

    def editar_celula(self, item):
        # Obter a linha e coluna da célula clicada
        row = item.row()
        column = item.column()

        # Verificar se o item existe
        if item is not None:
            # Obter o valor atual da célula
            valor_atual = item.text()

            # Obter o nome da coluna da célula
            nome_coluna = self.table_widget.horizontalHeaderItem(column).text()

            # Criar uma janela de edição com mensagem personalizada
            valor_editado, ok = QInputDialog.getText(
                self,
                f"Editar Valor de {nome_coluna}",
                f"Digite o novo valor de {nome_coluna}:",
                text=valor_atual,
            )

            # Se o usuário pressionar OK na janela de edição
            if ok:
                # Atualizar o valor na célula
                item.setText(valor_editado)

                # Atualizar o valor no banco de dados
                selected_empresa = self.combo_empresas.currentText()
                selected_empresa = selected_empresa.split(" - ")[1]

                try:
                    # Obter o ID da empresa
                    conn = conectar_banco()
                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT id_empresa FROM empresas WHERE nome_empresa = %s",
                        (selected_empresa,),
                    )
                    result = cursor.fetchone()

                    if result:
                        id_empresa = result[0]

                        # Obter informações da célula (por exemplo, descrição, débito, crédito)
                        colunas = self.table_widget.columnCount()
                        valores = [
                            item.text()
                            for col in range(colunas)
                            for item in [self.table_widget.item(row, col)]
                        ]

                        # Atualizar o valor no banco de dados
                        table_name = f"conciliacao_{id_empresa}"
                        cursor.execute(
                            f"UPDATE {table_name} SET descricao = %s, conta_debito = %s, conta_credito = %s WHERE id_conciliacao = %s",
                            (valores[0], valores[1], valores[2], row + 1),
                        )  # Supondo que o ID seja a posição da linha + 1

                        conn.commit()
                        conn.close()

                except Exception as e:
                    error_message = MyErrorMessage()
                    error_message.showMessage(
                        "Erro ao atualizar valor no banco de dados: " + str(e)
                    )
                    error_message.exec_()

    def load_empresas(self):
        try:
            conn = conectar_banco()
            cursor = conn.cursor()

            cursor.execute("SELECT codigo_empresa, nome_empresa FROM empresas")

            empresas = cursor.fetchall()

            self.combo_empresas.clear()

            for empresa in empresas:
                codigo_empresa, nome_empresa = empresa
                self.combo_empresas.addItem(f"{codigo_empresa} - {nome_empresa}")

            conn.close()

        except Exception as e:
            error_message = QErrorMessage()
            error_message.showMessage("Erro ao carregar bancos: " + str(e))
            error_message.exec_()

    def listar_button_clicked(self):
        selected_empresa = self.combo_empresas.currentText()
        selected_empresa = selected_empresa.split(" - ")[1]

        try:
            # Consultar o banco de dados para obter o id_empresa
            conn = conectar_banco()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id_empresa FROM empresas WHERE nome_empresa = %s",
                (selected_empresa,),
            )
            result = cursor.fetchone()

            if result:
                id_empresa = result[0]

                # Executar uma consulta SQL na tabela conciliacao_{id_empresa}
                table_name = f"conciliacao_{id_empresa}"
                cursor.execute(
                    f"SELECT descricao, conta_debito, conta_credito FROM {table_name}"
                )
                conciliacoes = cursor.fetchall()

                # Atualizar a tabela na interface gráfica
                self.update_table_widget(conciliacoes)

                conn.close()

        except Exception as e:
            error_message = MyErrorMessage()
            error_message.showMessage("Erro ao listar conciliações: " + str(e))
            error_message.exec_()

    def update_table_widget(self, data):
        # Limpar a tabela existente
        self.table_widget.setRowCount(0)

        # Preencher a tabela com os resultados da consulta
        for row_data in data:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)

            for col, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                self.table_widget.setItem(row_position, col, item)

    def cadastrar_button_clicked(self):
        selected_empresa = self.combo_empresas.currentText()
        selected_empresa = selected_empresa.split(" - ")[1]

        self.cadastro_window = CadastroConciliacaoWindow(selected_empresa)
        self.cadastro_window.show()

        try:
            # 2. Consultar o banco de dados para obter o id_empresa
            conn = conectar_banco()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id_empresa FROM empresas WHERE nome_empresa = %s",
                (selected_empresa,),
            )
            result = cursor.fetchone()

            if result:
                id_empresa = result[0]

                # 3. Verificar e criar a tabela
                table_name = f"conciliacao_{id_empresa}"
                cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
                table_exists = cursor.fetchone()

                if not table_exists:
                    # A tabela não existe, então você pode criá-la aqui
                    cursor.execute(
                        f"CREATE TABLE {table_name} ("
                        "id_conciliacao INT PRIMARY KEY NOT NULL AUTO_INCREMENT UNIQUE, "
                        "descricao varchar(100), "
                        "conta_debito int, "
                        "conta_credito int"
                        ")"
                    )

                conn.commit()
                conn.close()

        except Exception as e:
            error_message = MyErrorMessage()
            error_message.showMessage("Erro ao cadastrar conciliações: " + str(e))
            error_message.exec_()

    def excel_cadastro(self, event):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly  # Permite somente leitura
        options |= QFileDialog.ExistingFiles  # Permite seleção de múltiplos arquivos
        file_dialog = QFileDialog.getOpenFileName(
            self,
            "Selecionar arquivo Excel",
            "",  # Diretório inicial (deixe em branco para usar o diretório padrão)
            "Arquivos Excel (*.xlsx *.xls *.csv);;Todos os arquivos (*)",
            options=options,
        )

        if file_dialog[0]:
            # file_dialog[0] contém o caminho do arquivo selecionado
            selected_file = file_dialog[0]
            self.excel_label.setText(selected_file)  # Atualize o texto da QLabel
            self.excel_button.setEnabled(True)

    def cadastrar_lista_button_clicked(self):
        arquivo_excel = self.excel_label.text()
        if not arquivo_excel:
            QMessageBox.warning(
                self, "Aviso", "Por favor, selecione um arquivo Excel primeiro."
            )
            return

        self.inserir_dados_no_banco(arquivo_excel)

    def inserir_dados_no_banco(self, arquivo_excel):
        try:
            # Carregue o arquivo Excel usando pandas
            df = pd.read_excel(arquivo_excel)  # Você pode usar 'read_csv' para CSVs

            selected_empresa = self.combo_empresas.currentText()
            selected_empresa = selected_empresa.split(" - ")[1]

            conn = conectar_banco()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id_empresa FROM empresas WHERE nome_empresa = %s",
                (selected_empresa,),
            )
            result = cursor.fetchone()

            if result:
                id_empresa = result[0]

                # Use os dados do DataFrame para inserir no banco de dados
                table_name = f"conciliacao_{id_empresa}"

                for _, row in df.iterrows():
                    descricao = row["DESCRICAO"]
                    debito = row["DEB"]
                    credito = row["CRED"]

                    cursor.execute(
                        f"INSERT INTO {table_name} (descricao, conta_debito, conta_credito) VALUES (%s, %s, %s)",
                        (descricao, debito, credito),
                    )

                conn.commit()
                conn.close()

        except Exception as e:
            error_message = MyErrorMessage()
            error_message.showMessage("Erro ao inserir dados no banco: " + str(e))
            error_message.exec_()


def main():
    app = QApplication(sys.argv)
    window = ConciliacaoWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
