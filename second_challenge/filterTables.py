import tabula
import csv
import os
import pandas as pd


def readingPDF():  # função que irá extrair as tabelas do pdf e exportar como .csv
    source = os.path.join(os.getcwd(), "second_challenge\\tables.csv")
    check = os.path.exists(source)
    fields = []

    # checa se o arquivo já existe, se sim ele irá pular para a proxima função
    if check == True:
        return True
    else:
        pdf_path = "second_challenge\Anexo_I.pdf"
        # abrindo arquivo em modo leitura lendo os binários
        # tables = tabula.read_pdf(pdf_path, stream=True, pages="all")
        print("Aguarde...\n")
        tabula.convert_into(
            pdf_path, "second_challenge\\tables.csv", output_format="csv", pages="all"
        )
        print("Arquivo processado com sucesso!")


# esta função irá ler o csv e substituir os valores indicados por outros
def manipulateCSV():
    df = pd.read_csv(
        "second_challenge\\tables.csv",
        encoding="latin1",
        on_bad_lines="skip",
    )

    df.drop_duplicates(inplace=True, keep=False)  # removendo linhas duplicadas

    df["AMB"] = df["AMB"].map({"AMB": "Seg. Ambulatorial"})
    df["OD"] = df["OD"].map({"OD": "Seg. Odontológica"})

    df.to_csv("second_challenge\\formatted.csv", index=False, encoding="latin1")


readingPDF()
manipulateCSV()
