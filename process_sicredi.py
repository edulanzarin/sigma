import pandas as pd


def process_sicredi(dados_pdf):
    data_list = []
    descricao_list = []
    valor_list = []
    linhas_imprimir = True  # Variável de controle para a primeira página
    deb_cred_list = []

    for pagina_num, pagina in enumerate(dados_pdf.pages, 1):
        texto_pagina = pagina.extract_text()
        linhas = texto_pagina.split("\n")

        for linha_num, linha in enumerate(linhas, 1):
            partes = linha.split()
            if len(partes) >= 5:
                if pagina_num == 1 and linha_num < 6:
                    continue  # Ignorar as cinco primeiras linhas da primeira página
                if "Saldo da conta" in linha:
                    linhas_imprimir = False
                    break  # Parar de processar quando encontrar "Saldo da conta"

                data = partes[0]
                descricao = " ".join(partes[1:-2])

                if "-" in partes[-2]:
                    pagamento = partes[-2]
                    valor = ""
                else:
                    pagamento = ""
                    valor = partes[-2]

                deb_cred = "CRED" if "-" in partes[-2] else "DEB"
                pagamento = pagamento.replace("-", "")

                data_list.append(data)
                descricao_list.append(descricao)
                valor_list.append(valor)
                deb_cred_list.append(deb_cred)

        if not linhas_imprimir:
            break  # Parar de processar páginas subsequentes

    # Criar um DataFrame com os dados
    df = pd.DataFrame(
        {
            "DATA": data_list,
            "VALOR": valor_list,
            "DEB": [37 if dc == "DEB" else None for dc in deb_cred_list],
            "CRED": [37 if dc == "CRED" else None for dc in deb_cred_list],
            "DESCRICAO": descricao_list,
        }
    )

    return df
