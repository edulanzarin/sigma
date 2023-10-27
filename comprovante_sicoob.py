import pandas as pd


def comprovante_sicoob(dados_pdf):
    data_list = []
    descricao_list = []
    valor_list = []
    desconto_list = []
    juros_list = []

    for pagina_num, pagina in enumerate(dados_pdf.pages, 1):
        texto_pagina = pagina.extract_text()
        linhas = texto_pagina.split("\n")

        for linha in linhas:
            partes = linha.split(" ")

            if "Data Pagamento:" in linha:
                data = partes[-1]
            if "Nome Fantasia Beneficiário:" in linha:
                descricao = " ".join(partes[4:])
            if "Valor Documento:" in linha:
                valor_str = partes[-1]
                valor = valor_str.replace(".", "").replace(",", ".")
            if "(-)" in linha:
                desconto_str = partes[-1]
                desconto = desconto_str.replace(".", "").replace(",", ".")
            if "(+)" in linha:
                juros_str = partes[-1]
                juros = juros_str.replace(".", "").replace(",", ".")
                if data is not None and descricao is not None and valor is not None:
                    data_list.append(data)
                    descricao_list.append(descricao)
                    valor_list.append(valor)
                    desconto_list.append(desconto)
                    juros_list.append(juros)

    df = pd.DataFrame(
        {
            "DATA": data_list,
            "DESCRICAO": descricao_list,
            "VALOR": valor_list,
            "DESCONTO": desconto_list,
            "JUROS": juros_list,
        }
    )

    return df 
