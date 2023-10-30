import sys
import PyPDF2
import os
import pandas as pd
from datetime import datetime
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
    QSizePolicy,
    QInputDialog,
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from error_window import MyErrorMessage
from processing_window import ProcessingWindow

from connect_banco import conectar_banco
from process_cresol import process_cresol
from process_safra import process_safra
from process_safra_internacional import process_safra_internacional
from process_sicredi import process_sicredi
from process_viacredi import process_viacredi
from process_sicoob import process_sicoob
from comprovante_sicoob import comprovante_sicoob


class EmpresasWindow(QWidget):
    def __init__(self, id_usuario):
        super().__init__()
        self.id_usuario = id_usuario
        self.combined_df = None
        self.folder_path = ""  # Adicione um atributo folder_path


        self.setWindowTitle("Empresas")
        self.setGeometry(100, 100, 800, 600)

        self.pdf_file_path = ""

        # Crie um layout vertical para incluir o ícone e os QComboBox de empresas e bancos
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
        self.combo_empresas.currentIndexChanged.connect(
            self.load_bancos
        )  # Conecte o sinal

        layout_1.addWidget(icon1_label)
        layout_1.addWidget(self.combo_empresas)

        # Crie um layout horizontal para o ícone e o QComboBox de bancos
        layout_2 = QHBoxLayout()
        layout_2.setAlignment(Qt.AlignTop)

        # Adicione um ícone personalizado ao QComboBox de bancos
        icon_2 = QIcon(r".\assets\bank.png")

        # Crie um QLabel para o ícone de bancos
        icon2_label = QLabel()
        icon2_label.setPixmap(icon_2.pixmap(18, 18))  # Defina o tamanho do ícone

        # Defina a política de dimensionamento do icon_label para ocupar 5% do espaço
        icon2_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Converta o valor em ponto flutuante para inteiro
        max_width = int(self.width() * 0.03)
        icon2_label.setMaximumWidth(max_width)  # 5% da largura da janela

        # Crie o QComboBox de bancos
        self.combo_bancos = QComboBox()

        layout_2.addWidget(icon2_label)
        layout_2.addWidget(self.combo_bancos)

        # Crie um layout horizontal para o ícone, a label e o botão
        layout_3 = QHBoxLayout()
        layout_3.setAlignment(Qt.AlignTop)

        # Adicione um ícone personalizado ao layout
        icon_3 = QIcon(r".\assets\pdf.png")

        # Crie um QLabel para o ícone
        icon3_label = QLabel()
        icon3_label.setPixmap(icon_3.pixmap(18, 18))  # Defina o tamanho do ícone

        # Defina a política de dimensionamento do icon_label para ocupar 5% do espaço
        icon3_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Converta o valor em ponto flutuante para inteiro
        max_width = int(self.width() * 0.03)
        icon3_label.setMaximumWidth(max_width)  # 5% da largura da janela

        # Crie uma QLabel para mostrar o nome do arquivo escolhido
        self.pdf_label = QLabel("Extrato bancário")
        self.pdf_label.setStyleSheet(
            "QLabel {"
            "border: 0.5px solid lightgray;"
            "border-radius: 5px;"
            "padding: 5px;"
            "font-size: 14rem;"  # Adicione sublinhado para indicar que é clicável
            "}"
        )
        self.pdf_label.setCursor(
            Qt.PointingHandCursor
        )  # Mude o cursor para a mão ao passar por cima
        self.pdf_label.setOpenExternalLinks(
            False
        )  # Impede que os links sejam abertos em um navegador externo

        self.pdf_label.mousePressEvent = self.choose_pdf  #

        self.choose_file = False

        layout_3.addWidget(icon3_label)
        layout_3.addWidget(self.pdf_label)

        # LAYOUT PARA SELECIONAR PAGAMENTOS
        # Crie um layout horizontal para o ícone, a label e o botão
        layout_4 = QHBoxLayout()
        layout_4.setAlignment(Qt.AlignTop)

        # Adicione um ícone personalizado ao layout
        icon_4 = QIcon(r".\assets\pagamento.png")

        # Crie um QLabel para o ícone
        icon4_label = QLabel()
        icon4_label.setPixmap(icon_4.pixmap(18, 18))  # Defina o tamanho do ícone

        # Defina a política de dimensionamento do icon_label para ocupar 5% do espaço
        icon4_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Converta o valor em ponto flutuante para inteiro
        max_width = int(self.width() * 0.03)
        icon4_label.setMaximumWidth(max_width)  # 5% da largura da janela

        # Crie uma QLabel para mostrar o nome do arquivo escolhido
        self.pagamento_label = QLabel("Comprovantes de pagamentos")
        self.pagamento_label.setStyleSheet(
            "QLabel {"
            "border: 0.5px solid lightgray;"
            "border-radius: 5px;"
            "padding: 5px;"
            "font-size: 14rem;"
            "}"
        )
        self.pagamento_label.setCursor(
            Qt.PointingHandCursor
        )  # Mude o cursor para a mão ao passar por cima
        self.pagamento_label.setOpenExternalLinks(
            False
        )  # Impede que os links sejam abertos em um navegador externo

        self.pagamento_label.mousePressEvent = self.choose_pagamentos 

        self.carregar_button = QPushButton("Carregar")
        self.carregar_button.clicked.connect(self.carregar_button_clicked)
        self.carregar_button.setStyleSheet(
            "QPushButton { max-width: 80px; font-size: 12px;}"
        )
        self.carregar_button.setEnabled(False)
        self.carregar_button.setCursor(Qt.PointingHandCursor)

        layout_4.addWidget(icon4_label)
        layout_4.addWidget(self.pagamento_label)
        layout_4.addWidget(self.carregar_button)

        # LAYOUT PARA BOTÕES
        layout_5 = QHBoxLayout()
        layout_5.setAlignment(Qt.AlignTop)

        self.process_button = QPushButton("Processar")
        self.process_button.clicked.connect(self.process_button_clicked)
        self.process_button.setStyleSheet(
            "QPushButton { max-width: 80px; font-size: 12px;}"
        )
        self.process_button.setEnabled(False)
        self.process_button.setCursor(Qt.PointingHandCursor)

        self.conciliar_button = QPushButton("Conciliar")
        self.conciliar_button.clicked.connect(self.conciliar_button_clicked)
        self.conciliar_button.setStyleSheet(
            "QPushButton { max-width: 80px; font-size: 12px;}"
        )
        self.conciliar_button.setEnabled(False)
        self.conciliar_button.setCursor(Qt.PointingHandCursor)

        self.save_button = QPushButton("Salvar")
        self.save_button.clicked.connect(self.save_button_clicked)
        self.save_button.setStyleSheet(
            "QPushButton { max-width: 80px; font-size: 12px;}"
        )
        self.save_button.setEnabled(False)
        self.save_button.setCursor(Qt.PointingHandCursor)

        layout_5.addStretch(1)
        layout_5.addWidget(self.process_button)
        layout_5.addWidget(self.conciliar_button)
        layout_5.addWidget(self.save_button)
        layout_5.addStretch(1)

        layout_7 = QHBoxLayout()
        layout_7.setAlignment(Qt.AlignTop)
        icon7_label = QLabel()
        layout_7.addWidget(icon7_label)

        main_layout.addLayout(layout_1)
        main_layout.addLayout(layout_2)
        main_layout.addLayout(layout_3)
        main_layout.addLayout(layout_4)
        main_layout.addLayout(layout_5)
        main_layout.addLayout(layout_7)

        # Crie um modelo de item padrão para a tabela
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(
            5
        )  # Cinco colunas: data, debito, credito, valor, descricao
        self.table_widget.setHorizontalHeaderLabels(
            ["Data", "Débito", "Crédito", "Valor", "Descrição"]
        )
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.setSortingEnabled(True)
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.cellDoubleClicked.connect(self.edit_cell)

        main_layout.addWidget(self.table_widget)
        self.setLayout(main_layout)
        self.load_empresas()

    def choose_pagamentos(self, event):
        self.folder_path = QFileDialog.getExistingDirectory(self, "Escolher uma pasta com comprovantes de pagamentos")
        self.carregar_button.setEnabled(True)

        self.pagamento_label.setText(self.folder_path)
        # Atualize o estado do botão "Processar" com base na variável choose_file
        self.process_button.setEnabled(self.choose_file)

    def carregar_button_clicked(self):
        if self.folder_path:
            try:
                # Initialize combined_df if it's None
                if self.combined_df is None:
                    self.combined_df = pd.DataFrame()

                # Iterate through the files in the folder
                for filename in os.listdir(self.folder_path):
                    if filename.endswith(".pdf"):
                        pdf_file_path = os.path.join(self.folder_path, filename)
                        pdf_file = open(pdf_file_path, "rb")
                        dados_pdf = PyPDF2.PdfReader(pdf_file)
                        # Process the PDF and add its data to combined_df
                        df = comprovante_sicoob(dados_pdf)
                        self.combined_df = pd.concat([self.combined_df, df], ignore_index=True)

                selected_banco = self.combo_bancos.currentText()
                selected_banco = selected_banco.split(" - ")[0]

                if selected_banco == "30":
                    # Convert the date strings in the "DATA" column to datetime.date objects
                    self.combined_df['DATA'] = pd.to_datetime(self.combined_df['DATA'], format="%d/%m/%Y").dt.date

                    tabela_nome = f"comprovante_{selected_banco}"

                    conn = conectar_banco()
                    cursor = conn.cursor()

                    create_table_query = f"""
                    CREATE TABLE IF NOT EXISTS {tabela_nome} (
                        id_comprovante INT AUTO_INCREMENT PRIMARY KEY,
                        data DATE,
                        descricao VARCHAR(255),
                        valor FLOAT,
                        desconto FLOAT,
                        juros FLOAT
                    )
                    """
                    cursor.execute(create_table_query)
                    conn.commit()

                    delete_records_query = f"DELETE FROM {tabela_nome}"
                    cursor.execute(delete_records_query)
                    conn.commit()

                    for index, row in self.combined_df.iterrows():
                        data = row['DATA']
                        descricao = row["DESCRICAO"]
                        valor = row["VALOR"]
                        desconto = row["DESCONTO"]
                        juros = row["JUROS"]

                        # Inserção dos dados
                        insert_data_query = f"""
                        INSERT INTO {tabela_nome} (data, descricao, valor, desconto, juros)
                        VALUES (%s, %s, %s, %s, %s)
                        """

                        cursor.execute(
                            insert_data_query, (data, descricao, valor, desconto, juros)
                        )
                        conn.commit()

                    cursor.close()
                    conn.close()
            except Exception as e:
                error_message = MyErrorMessage()
                error_message.showMessage("Erro ao carregar os comprovantes! " + str(e))
                error_message.exec_()


    def load_user_id(self, id_usuario):
        # Este método será chamado para carregar o id_usuario
        self.id_usuario = id_usuario

    def edit_cell(self, row, column):
        if column in (1, 2):  # Verifique se a coluna é débito (1) ou crédito (2)
            item = self.table_widget.item(row, column)
            if item is not None:
                current_value = item.text()
            else:
                current_value = ""  # Valor padrão se a célula estiver vazia

            new_value, ok = QInputDialog.getText(
                self,
                "Editar Valor",
                f"Digite o novo valor de {self.table_widget.horizontalHeaderItem(column).text()}:",
                text=current_value,
            )

            if ok:
                # Atualize o valor na tabela
                if item is not None:
                    item.setText(new_value)
                else:
                    item = QTableWidgetItem(new_value)
                    self.table_widget.setItem(row, column, item)

                # Atualize o valor no banco de dados
                descricao_item = self.table_widget.item(row, 4)
                if descricao_item is not None:
                    descricao = descricao_item.text()
                    self.update_database(descricao, column, new_value)

    def update_database(self, descricao, column, new_value):
        try:
            conn = conectar_banco()
            cursor = conn.cursor()

            update_query = """
            UPDATE transacoes
            SET {} = %s
            WHERE descricao = %s
            """.format(
                "debito" if column == 1 else "credito"
            )

            cursor.execute(update_query, (new_value, descricao))
            conn.commit()
            conn.close()

        except Exception as e:
            error_message = MyErrorMessage()
            error_message.showMessage(
                "Erro ao atualizar valores no banco de dados! " + str(e)
            )
            error_message.exec_()

    def load_bancos(self):
        try:
            conn = conectar_banco()
            cursor = conn.cursor()

            self.combo_bancos.clear()

            selected_index = self.combo_empresas.currentIndex()
            if selected_index >= 0:
                selected_empresa = self.combo_empresas.itemText(selected_index)
                empresa_selecionada = selected_empresa.split(" - ")[1]
                cursor.execute(
                    "SELECT id_empresa FROM empresas WHERE nome_empresa = %s",
                    (empresa_selecionada,),
                )
                self.id_empresa = cursor.fetchone()

                cursor.execute(
                    "SELECT b.codigo_banco, b.nome_banco FROM bancos b "
                    "JOIN empresa_banco eb ON b.id_banco = eb.id_banco "
                    "WHERE eb.id_empresa = %s",
                    self.id_empresa,
                )

                bancos = cursor.fetchall()

                for banco in bancos:
                    codigo_banco, nome_banco = banco
                    self.combo_bancos.addItem(f"{codigo_banco} - {nome_banco}")

            conn.close()

        except Exception as e:
            error_message = MyErrorMessage()
            error_message.showMessage("Erro ao carregar bancos! " + str(e))
            error_message.exec_()

    def choose_pdf(self, event):
        # Abra uma caixa de diálogo para selecionar um arquivo
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Escolher um arquivo PDF",
            "",  # Deixe esta string vazia para permitir que o usuário escolha de qualquer local
            "Arquivos PDF (*.pdf);;Todos os Arquivos (*)",
            options=options,
        )

        # Atualize a variável pdf_file_path para o caminho escolhido
        if file_name:
            self.pdf_file_path = file_name  # Defina a variável pdf_file_path
            self.pdf_label.setText(file_name)
            self.choose_file = True
        else:
            self.choose_file = False

        # Atualize o estado do botão "Processar" com base na variável choose_file
        self.process_button.setEnabled(self.choose_file)

    def conciliar_button_clicked(self):
        try:
            conn = conectar_banco()
            cursor = conn.cursor()

            # Recupere o ID da empresa selecionada
            selected_index = self.combo_empresas.currentIndex()
            if selected_index >= 0:
                selected_empresa = self.combo_empresas.itemText(selected_index)
                empresa_selecionada = selected_empresa.split(" - ")[1]
                cursor.execute(
                    "SELECT id_empresa FROM empresas WHERE nome_empresa = %s",
                    (empresa_selecionada,),
                )
                self.id_empresa = cursor.fetchone()

                if self.id_empresa:
                    # Construa o nome da tabela da empresa específica
                    nome_tabela_conciliacao = f"conciliacao_{self.id_empresa[0]}"

                    # Consulta SQL para atualizar a tabela de conciliação
                    update_query = f"""
                    UPDATE transacoes AS t
                    SET t.debito = (
                        CASE
                            WHEN EXISTS (
                                SELECT 1
                                FROM {nome_tabela_conciliacao} AS c
                                WHERE t.descricao LIKE CONCAT('%', LOWER(c.descricao), '%')
                            ) THEN
                                (SELECT COALESCE(debito, conta_debito)
                                FROM {nome_tabela_conciliacao} AS c
                                WHERE t.descricao LIKE CONCAT('%', LOWER(c.descricao), '%')
                                LIMIT 1)
                            ELSE
                                t.debito  -- Mantém o valor original de debito
                        END
                    ),
                    t.credito = (
                        CASE
                            WHEN EXISTS (
                                SELECT 1
                                FROM {nome_tabela_conciliacao} AS c
                                WHERE t.descricao LIKE CONCAT('%', LOWER(c.descricao), '%')
                            ) THEN
                                (SELECT COALESCE(credito, conta_credito)
                                FROM {nome_tabela_conciliacao} AS c
                                WHERE t.descricao LIKE CONCAT('%', LOWER(c.descricao), '%')
                                LIMIT 1)
                            ELSE
                                t.credito  -- Mantém o valor original de credito
                        END
                    );
                    """

                    cursor.execute(update_query)
                    conn.commit()
                    conn.close()
                    self.load_transacoes()
                else:
                    QMessageBox.warning(self, "Erro", "ID da empresa não encontrado.")
            else:
                QMessageBox.warning(
                    self, "Erro", "Selecione uma empresa para realizar a conciliação."
                )

            conn.close()
        except Exception as e:
            error_message = MyErrorMessage()
            error_message.showMessage("Erro ao realizar a conciliação! " + str(e))
            error_message.exec_()

    def atualizar_descricoes_transacoes(self):
        try:
            conn = conectar_banco()  # Conecta-se ao banco de dados
            cursor = conn.cursor()

            # Recupere os dados da tabela de transações
            cursor.execute("SELECT data_transacao, valor, descricao FROM transacoes")
            transacoes = cursor.fetchall()

            for data_transacao, valor, descricao in transacoes:
                # Verifique se há uma correspondência na tabela de comprovantes (comprovante_30)
                cursor.execute(
                    "SELECT descricao FROM comprovante_30 WHERE data = %s AND valor = %s",
                    (data_transacao, valor),
                )
                matching_row = cursor.fetchone()

                if matching_row:
                    # Se houver uma correspondência, atualize a descrição na tabela de transações
                    nova_descricao = matching_row[0]
                    cursor.execute(
                        "UPDATE transacoes SET descricao = %s WHERE data_transacao = %s AND valor = %s",
                        (nova_descricao, data_transacao, valor),
                    )

            conn.commit()
            conn.close()
            print("Descrições atualizadas com sucesso!")

        except Exception as e:
            print("Erro ao atualizar as descrições das transações:", str(e))

    def process_button_clicked(self):
        self.processing_window = ProcessingWindow()
        self.processing_window.show()
        if not self.pdf_file_path:
            error_message = MyErrorMessage()
            error_message.showMessage(
                "Nenhum arquivo selecionado. Escolha um arquivo PDF antes de processar."
            )
            error_message.exec_()
            return

        selected_banco = self.combo_bancos.currentText()
        selected_banco = selected_banco.split(" - ")[0]

        if selected_banco not in ("37", "23", "14", "30"):
            # Banco não suportado, exiba uma mensagem de erro
            error_message = MyErrorMessage()
            error_message.showMessage("Banco não cadastrado!")
            error_message.exec_()
            return

        pdf_file = open(self.pdf_file_path, "rb")
        dados_pdf = PyPDF2.PdfReader(pdf_file)

        if selected_banco == "37":
            df = process_viacredi(dados_pdf)
        if selected_banco == "23":
            df = process_sicredi(dados_pdf)
        if selected_banco == "14":
            df = process_safra(dados_pdf)
        if selected_banco == "30":
            df = process_sicoob(dados_pdf)

        conn = conectar_banco()
        cursor = conn.cursor()
        delete_table_query = "DROP TABLE IF EXISTS transacoes"
        cursor.execute(delete_table_query)
        create_table_query = """
        CREATE TABLE transacoes (
            id_transacao INT AUTO_INCREMENT PRIMARY KEY UNIQUE,
            data_transacao DATE,
            debito varchar(10),
            credito varchar(10),
            valor FLOAT,
            descricao VARCHAR(255)
        );
        """
        cursor.execute(create_table_query)

        df = df.where(pd.notna(df), None)

        # Insira os dados no banco de dados
        for _, row in df.iterrows():
            # Converta as colunas para tipos de dados apropriados, se necessário
            data_transacao = datetime.strptime(row["DATA"], "%d/%m/%Y").date()

            # Trate o valor "NaN" como nulo (None) para debito e credito
            debito = int(row["DEB"]) if not pd.isna(row["DEB"]) else None
            credito = int(row["CRED"]) if not pd.isna(row["CRED"]) else None

            valor = float(row["VALOR"])
            descricao = str(row["DESCRICAO"])

            insert_query = """
            INSERT INTO transacoes (data_transacao, debito, credito, valor, descricao)
            VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(
                insert_query, (data_transacao, debito, credito, valor, descricao)
            )

        conn.commit()
        conn.close()

        if selected_banco == "30":
            conn = conectar_banco()
            cursor = conn.cursor()
            cursor.execute("SHOW TABLES LIKE 'comprovante_30'")
            table_exists = cursor.fetchone()

            if table_exists:
                self.atualizar_descricoes_transacoes()
            else:
                # A tabela "comprovante_30" não existe, exiba uma mensagem
                QMessageBox.warning(
                    self, "Tabela não encontrada", "A tabela 'comprovante_30' não existe."
                )

            conn.close()

        self.load_transacoes()
        self.save_button.setEnabled(True)
        self.conciliar_button.setEnabled(True)
        self.process_button.setEnabled(True)
        self.processing_window.close()

    def update_table(self, data):
        self.table_widget.setRowCount(len(data))
        self.table_widget.setColumnCount(
            5
        )  # Certifique-se de configurar o número de colunas
        self.table_widget.setHorizontalHeaderLabels(
            ["Data", "Débito", "Crédito", "Valor", "Descrição"]
        )

        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                # Crie itens editáveis para permitir a edição
                item = QTableWidgetItem(str(value) if value is not None else "")
                item.setFlags(item.flags() | Qt.ItemIsEditable)
                self.table_widget.setItem(row, col, item)
        # Defina a altura das linhas para 20 pixels
        for row in range(self.table_widget.rowCount()):
            self.table_widget.setRowHeight(row, 10)

        # Conecte o sinal de edição de célula para salvar as alterações no banco de dados
        self.process_button.setEnabled(True)
        self.save_button.setEnabled(True)
        self.conciliar_button.setEnabled(True)

    def save_button_clicked(self):
        if self.table_widget.rowCount() == 0:
            QMessageBox.warning(
                self,
                "Nenhum dado para salvar",
                "Não há dados na tabela para salvar em um arquivo Excel.",
            )
            return

        # Abra uma caixa de diálogo para escolher o local e o nome do arquivo Excel
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar Tabela em Excel",
            "",  # Deixe esta string vazia para permitir que o usuário escolha o local
            "Arquivos Excel (*.xlsx);;Todos os Arquivos (*)",
            options=options,
        )

        if file_name:
            # Crie um DataFrame a partir dos dados da tabela
            data = []
            for row in range(self.table_widget.rowCount()):
                row_data = []
                for col in range(5):
                    item = self.table_widget.item(row, col)
                    if item is not None:
                        row_data.append(item.text())
                    else:
                        row_data.append(None)
                data.append(row_data)

            df = pd.DataFrame(
                data, columns=["Data", "Débito", "Crédito", "Valor", "Descrição"]
            )

            # Salve o DataFrame em um arquivo Excel
            df.to_excel(file_name, index=False)
            QMessageBox.information(
                self, "Salvo com sucesso", f"A tabela foi salva em {file_name}."
            )

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
            error_message = MyErrorMessage()
            error_message.showMessage("Erro ao carregar empresa! " + str(e))
            error_message.exec_()

        # Desabilite o botão "Processar" no início, pois nenhum arquivo foi escolhido ainda
        self.process_button.setEnabled(False)

    def load_transacoes(self):
        try:
            conn = conectar_banco()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT data_transacao, debito, credito, valor, descricao FROM transacoes"
            )
            transacoes = cursor.fetchall()
            data = [list(transacao) for transacao in transacoes]
            # Formatando as datas para o formato brasileiro
            for row in data:
                if row[0] is not None:  # Verifique se a data não é nula
                    row[0] = row[0].strftime("%d/%m/%Y")  # Formato brasileiro

            self.table_widget.clearContents()
            self.table_widget.setRowCount(0)
            self.update_table(data)

            conn.close()
            # Atualize a largura da coluna "Data" após carregar os dados
            self.table_widget.setColumnWidth(
                0, 100
            )  # Ajuste o valor conforme necessário

            # Atualize a largura da coluna "Descrição" após carregar os dados
            self.table_widget.setColumnWidth(
                4, 300
            )  # Ajuste o valor conforme necessário

        except Exception as e:
            error_message = MyErrorMessage()
            error_message.showMessage("Erro ao carregar extrato! " + str(e))
            error_message.exec_()


def main():
    app = QApplication(sys.argv)
    window = EmpresasWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
