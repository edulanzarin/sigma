from connect_banco import conectar_banco


def listar_conciliacoes(id_empresa):
    try:
        conn = conectar_banco()
        cursor = conn.cursor()

        # Verifica se a tabela existe
        cursor.execute(
            f"SELECT name FROM sqlite_master WHERE type='table' AND name='conciliacoes_{id_empresa}'"
        )
        table_exists = cursor.fetchone()

        if table_exists:
            # Se a tabela existir, execute a consulta
            cursor.execute(f"SELECT * FROM conciliacoes_{id_empresa}")
            conciliacoes = cursor.fetchall()

            # Faça o que você deseja com os resultados (por exemplo, exiba-os em uma janela)
            for conciliacao in conciliacoes:
                # Realize a ação desejada com os dados da conciliação
                print(conciliacao)

        conn.close()

    except Exception as e:
        # Lide com erros de forma adequada, como exibindo uma mensagem de erro
        print("Erro ao listar conciliações:", str(e))
