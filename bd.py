import tkinter as tk
from tkinter import ttk
import mysql.connector

tabela_conciliacao = ""


def criar_tabela_conciliacao():
    janela_insercao = tk.Toplevel(root)
    janela_insercao.title("Inserção de Dados")

    # Crie os elementos da interface para inserir os dados
    descricao_label = tk.Label(janela_insercao, text="Descrição:")
    descricao_label.pack()
    descricao_entry = tk.Entry(janela_insercao)
    descricao_entry.pack()

    conta_debito_label = tk.Label(janela_insercao, text="Conta de Débito:")
    conta_debito_label.pack()
    conta_debito_entry = tk.Entry(janela_insercao)
    conta_debito_entry.pack()

    conta_credito_label = tk.Label(janela_insercao, text="Conta de Crédito:")
    conta_credito_label.pack()
    conta_credito_entry = tk.Entry(janela_insercao)
    conta_credito_entry.pack()

    # Função para inserir os dados no banco de dados
    def inserir_dados():
        descricao = descricao_entry.get()
        conta_debito = conta_debito_entry.get()
        conta_credito = conta_credito_entry.get()

        # Valide as colunas numéricas para garantir que sejam números inteiros
        try:
            conta_debito = int(conta_debito)
            conta_credito = int(conta_credito)
        except ValueError:
            mensagem_label.config(
                text="Conta de Débito e Conta de Crédito devem ser números inteiros."
            )
            return

        # Insira os dados na tabela de conciliação
        cursor.execute(
            "INSERT INTO "
            + tabela_conciliacao
            + " (descricao, conta_debito, conta_credito) VALUES (%s, %s, %s)",
            (descricao, conta_debito, conta_credito),
        )
        conexao.commit()
        mensagem_label.config(text="Dados inseridos com sucesso.")

    # Botão para inserir os dados
    inserir_button = tk.Button(
        janela_insercao, text="Inserir Dados", command=inserir_dados
    )
    inserir_button.pack()
    global tabela_conciliacao
    empresa_selecionada = empresa_combobox.get()
    cursor.execute(
        "SELECT id_empresa FROM empresas WHERE nome_empresa = %s",
        (empresa_selecionada,),
    )
    id_empresa = cursor.fetchone()

    if id_empresa:
        id_empresa = id_empresa[0]
        tabela_conciliacao = f"conciliacao_{id_empresa}"

        # Verifique se a tabela de conciliação já existe
        cursor.execute(f"SHOW TABLES LIKE '{tabela_conciliacao}'")
        tabela_existe = cursor.fetchone()

        if not tabela_existe:
            # Se a tabela de conciliação não existe, crie-a
            cursor.execute(
                f"CREATE TABLE {tabela_conciliacao} ("
                "id_conciliacao INT PRIMARY KEY NOT NULL AUTO_INCREMENT UNIQUE, "
                "descricao varchar(100), "
                "conta_debito int, "
                "conta_credito int"
                ")"
            )

            conexao.commit()
            mensagem_label.config(
                text=f"Tabela de conciliação para {empresa_selecionada} criada."
            )
        else:
            mensagem_label.config(
                text=f"Tabela de conciliação para {empresa_selecionada} já existe."
            )
    else:
        mensagem_label.config(text="Empresa não encontrada.")


def listar_conciliacoes():
    id_mapping = {}
    global tabela_conciliacao
    empresa_selecionada = empresa_combobox.get()
    cursor.execute(
        "SELECT id_empresa FROM empresas WHERE nome_empresa = %s",
        (empresa_selecionada,),
    )
    id_empresa = cursor.fetchone()

    if id_empresa:
        id_empresa = id_empresa[0]
        tabela_conciliacao = f"conciliacao_{id_empresa}"

        # Abre uma nova janela para listar e operar sobre as conciliações
        janela_listagem = tk.Toplevel(root)
        janela_listagem.title("Listagem de Conciliações")

        # Lista as conciliações na nova janela
        cursor.execute(f"SELECT * FROM {tabela_conciliacao}")
        conciliacoes = cursor.fetchall()

        lista_conciliacoes = ttk.Treeview(
            janela_listagem, columns=("Descrição", "Conta Débito", "Conta Crédito")
        )

        lista_conciliacoes.heading("#1", text="Descrição")
        lista_conciliacoes.heading("#2", text="Conta Débito")
        lista_conciliacoes.heading("#3", text="Conta Crédito")
        lista_conciliacoes["show"] = "headings"
        lista_conciliacoes.pack()

        for i, conciliacao in enumerate(conciliacoes):
            id_mapping[i] = conciliacao[0]  # Mapeie o índice (i) para o ID real
            lista_conciliacoes.insert(
                "",
                "end",
                values=(conciliacao[1], conciliacao[2], conciliacao[3]),
            )

        # Funções para excluir e alterar conciliações
        def excluir_conciliacao():
            selecionado = lista_conciliacoes.selection()
            if selecionado:
                indice_selecionado = lista_conciliacoes.index(selecionado)
                id_do_banco_de_dados = id_mapping.get(indice_selecionado)
                if id_do_banco_de_dados is not None:
                    try:
                        # Certifique-se de que o id_conciliacao seja um número inteiro válido
                        id_do_banco_de_dados = int(id_do_banco_de_dados)
                    except ValueError:
                        mensagem_label.config(
                            text="Erro: Selecione uma conciliação válida para excluir."
                        )
                        return

                    cursor.execute(
                        f"DELETE FROM {tabela_conciliacao} WHERE id_conciliacao = %s",
                        (id_do_banco_de_dados,),
                    )
                    conexao.commit()
                    lista_conciliacoes.delete(selecionado)
                    mensagem_label.config(text="Conciliação excluída com sucesso.")
            else:
                mensagem_label.config(text="Selecione uma conciliação para excluir.")

        def alterar_conciliacao():
            selecionado = lista_conciliacoes.selection()
            if selecionado:
                indice_selecionado = lista_conciliacoes.index(selecionado)
                id_do_banco_de_dados = id_mapping.get(indice_selecionado)
                janela_alteracao = tk.Toplevel(janela_listagem)
                janela_alteracao.title("Alteração de Dados")

                descricao_label = tk.Label(janela_alteracao, text="Descrição:")
                descricao_label.pack()
                novo_descricao_entry = tk.Entry(janela_alteracao)
                novo_descricao_entry.pack()

                conta_debito_label = tk.Label(janela_alteracao, text="Conta de Débito:")
                conta_debito_label.pack()
                nova_conta_debito_entry = tk.Entry(janela_alteracao)
                nova_conta_debito_entry.pack()

                conta_credito_label = tk.Label(
                    janela_alteracao, text="Conta de Crédito:"
                )
                conta_credito_label.pack()
                nova_conta_credito_entry = tk.Entry(janela_alteracao)
                nova_conta_credito_entry.pack()

                # Preencher campos com os valores atuais
                valores_atuais = lista_conciliacoes.item(selecionado[0])["values"]
                novo_descricao_entry.insert(0, valores_atuais[0])
                nova_conta_debito_entry.insert(0, valores_atuais[1])
                nova_conta_credito_entry.insert(0, valores_atuais[2])

                # Função para atualizar os dados
                def atualizar_dados():
                    novo_descricao = novo_descricao_entry.get()
                    nova_conta_debito = nova_conta_debito_entry.get()
                    nova_conta_credito = nova_conta_credito_entry.get()

                    try:
                        # Certifique-se de que as contas sejam números inteiros válidos
                        nova_conta_debito = int(nova_conta_debito)
                        nova_conta_credito = int(nova_conta_credito)
                    except ValueError:
                        mensagem_label.config(
                            text="Conta de Débito e Conta de Crédito devem ser números inteiros."
                        )
                        return

                    cursor.execute(
                        f"UPDATE {tabela_conciliacao} SET descricao = %s, conta_debito = %s, conta_credito = %s WHERE id_conciliacao = %s",
                        (
                            novo_descricao,
                            nova_conta_debito,
                            nova_conta_credito,
                            id_do_banco_de_dados,
                        ),
                    )
                    conexao.commit()
                    mensagem_label.config(text="Dados atualizados com sucesso.")
                    janela_alteracao.destroy()
                    # Atualize a lista após a alteração
                    lista_conciliacoes.item(
                        selecionado[0],
                        values=(novo_descricao, nova_conta_debito, nova_conta_credito),
                    )

                # Botão para atualizar os dados
                atualizar_button = tk.Button(
                    janela_alteracao, text="Atualizar Dados", command=atualizar_dados
                )
                atualizar_button.pack()
            else:
                mensagem_label.config(text="Selecione uma conciliação para alterar.")

        def atualizar_lista_conciliacoes():
            cursor.execute(f"SELECT * FROM {tabela_conciliacao}")
            conciliacoes = cursor.fetchall()
            lista_conciliacoes.delete(*lista_conciliacoes.get_children())

            for i, conciliacao in enumerate(conciliacoes):
                id_mapping[i] = conciliacao[0]
                lista_conciliacoes.insert(
                    "",
                    "end",
                    values=(conciliacao[1], conciliacao[2], conciliacao[3]),
                )

        # Botões para excluir e alterar conciliações
        excluir_button = tk.Button(
            janela_listagem, text="Excluir Conciliação", command=excluir_conciliacao
        )
        excluir_button.pack()

        alterar_button = tk.Button(
            janela_listagem, text="Alterar Conciliação", command=alterar_conciliacao
        )
        alterar_button.pack()

        atualizar_lista_button = tk.Button(
            janela_listagem,
            text="Atualizar Lista",
            command=atualizar_lista_conciliacoes,
        )
        atualizar_lista_button.pack()

        atualizar_lista_conciliacoes()


# Código de conexão ao banco de dados
conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="empresas",
)
cursor = conexao.cursor()

root = tk.Tk()
root.title("Sigma")
root.state("zoomed")

empresa_label = tk.Label(root, text="Escolha uma empresa:")
empresa_label.pack()

cursor.execute("SELECT nome_empresa FROM empresas")
empresas = [row[0] for row in cursor.fetchall()]
empresa_combobox = ttk.Combobox(root, values=empresas)
empresa_combobox.pack()

conciliar_button = tk.Button(root, text="Conciliar", command=criar_tabela_conciliacao)
conciliar_button.pack()

listar_conciliacoes_button = tk.Button(
    root, text="Listar Conciliações", command=listar_conciliacoes
)
listar_conciliacoes_button.pack()

mensagem_label = tk.Label(root, text="", wraplength=400)
mensagem_label.pack()

root.mainloop()

# Código de fechamento de conexão
cursor.close()
conexao.close()
