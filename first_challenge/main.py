from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
import requests
import os
from bs4 import BeautifulSoup
import re
import shutil


def getContent(url):  # função que que irá tratar os possíveis erros na requisição
    try:
        page = urlopen(url)
    except HTTPError:
        print(
            "\033[31mHouve um erro ao obter a página. Por favor, verifique a URL fornecida.\033[m"
        )
        return False
    except URLError:
        print(
            "\033[31mO servidor não foi encontrado. Verifique se a URL está correta.\033[m"
        )
        return False
    try:
        bs = BeautifulSoup(page.read(), "lxml")
        content = bs
    except AttributeError:
        print("\033[31mA tag não foi encontrada.\033[m")
        return False
    return content


def getURL():  # função que irá filtrar e adicionar os links dos pdfs numa lista
    pdfs = []
    content = getContent(
        "https://www.gov.br/ans/pt-br/assuntos/consumidor/o-que-o-seu-plano-de-saude-deve-cobrir-1/o-que-e-o-rol-de-procedimentos-e-evento-em-saude"
    )

    if content == None:
        print("O conteudo não foi encontrado")
        return None

    for link in content.find_all("a", attrs={"href": re.compile("^https://")}):
        filter = link.get("href")
        if "pdf" in filter and "Anexo" in link.text:
            pdfs.append(filter)
    return pdfs


def saveFiles():  # esta função irá pegar os links da função anterior e salvar os arquivos em si
    urls = getURL()
    parent = r"first_challenge"
    folder = "PDFs"
    os.chdir("first_challenge")
    path = os.path.join(os.getcwd(), folder)

    try:
        os.mkdir(path, mode=0o666)
    except FileExistsError:
        print("A pasta que você tentou criar já existe")

    for url in urls:
        file_name_start = url.rfind("/") + 1
        file_name = url[file_name_start:]
        response = requests.get(url, stream=True)

        if response.status_code == requests.codes.OK:
            with open(os.path.join(path, file_name), "wb") as new_file:
                new_file.write(response.content)
        else:
            response.raise_for_status()
    print(f"Download finalizado. Arquivos salvos em \033[31m{path}\033[m")

    anexo1 = os.path.join(
        path, "Anexo_I_Rol_2021RN_465.2021_RN473_RN478_RN480_RN513_RN536.pdf"
    )

    shutil.make_archive("PDFs", "zip", path)  # compress the folder
    print("Pasta comprimida com sucesso!")

    dst = "D:\Documents\dev\intuitive\\second_challenge\\Anexo_I.pdf"

    shutil.move(anexo1, dst)  # moving Anexo I to second_challenge, before delete it
    shutil.rmtree(path)  # removing original folder (descompressed)


saveFiles()
