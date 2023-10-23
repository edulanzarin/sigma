import pandas as pd
import re


# Função para processar uma página do PDF
def process_safra(dados_pdf):
    data_list = []
    descricao_list = []
    valor_list = []
    deb_cred_list = []

    for pagina_num, pagina in enumerate(dados_pdf.pages):
        linhas = pagina.extract_text().split("\n")
        if pagina_num == 0:
            start_line = 8
        else:
            start_line = 2
        last_date = ""
        descricao_anterior = ""
        linhas_puladas = 0
        for i, linha in enumerate(linhas[start_line:]):
            if "Banco Safra S/A" in linha:
                linhas_puladas = 10
                continue
            if linhas_puladas > 0:
                linhas_puladas -= 1
                continue
            if "SALDO" not in linha:
                partes = linha.split()
                if len(partes) >= 3:
                    if "/" in partes[0]:
                        if any(char.isdigit() for char in partes[-1]):
                            if "-" in partes[-1]:
                                valor = ""
                                pagamento = partes[-1]
                            else:
                                valor = partes[-1]
                                pagamento = ""
                            # Usar uma expressão regular para remover letras da data
                            data = re.sub(r"[^0-9/]", "", partes[0])
                            descricao = " ".join(partes[1:-2])
                            last_date = data
                        else:
                            descricao_anterior = partes[1:-2]
                            continue
                    else:
                        if "-" in partes[-1]:
                            valor = ""
                            pagamento = partes[-1]
                        else:
                            valor = partes[-1]
                            pagamento = ""
                        descricao = (
                            " ".join(descricao_anterior) + " " + " ".join(partes[0:-2])
                        )
                        data = last_date

                    deb_cred = "CRED" if "-" in partes[-3] else "DEB"
                    pagamento = pagamento.replace("-", "")

                    data_list.append(data)
                    descricao_list.append(descricao)
                    valor_list.append(valor)
                    deb_cred_list.append(deb_cred)

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
