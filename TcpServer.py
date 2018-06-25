#coding: utf-8
from socket import *
import os
import threading
from hashlib import *

serverPort = 13000
diretorioPadrao = "./pasta_compartilhada/"
arquivosEncontrados = {}

def iniciarServidor():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(10)

    print('O servidor está conectado')

    while 1:
        connectionSocket, addr = serverSocket.accept()
        connectionSocket.settimeout(60)
        threading.Thread(target= ouvirSocket, args=(connectionSocket,)).start()

    connectionSocket.close()


def ouvirSocket(connectionSocket):
    buscaDownload = connectionSocket.recv(1024)
    buscaDownload = buscaDownload.decode('utf-8')

    if not buscaDownload.__contains__('download:'):
        arquivo = pesquisaArquivo(diretorioPadrao, buscaDownload)
        hash = criarHash(arquivo)
        hash = str(hash)
        arquivosEncontrados[hash] = arquivo
        connectionSocket.send(hash.encode('utf-8'))
    else:
        hash = buscaDownload.replace('download:', '')
        # acessa o dicionario de hash com o hash que quer fazer o download.
        arquivo = arquivosEncontrados[hash]
        arquivo = open(arquivo.name, 'rb')

        # Le os bytes de cada linha e envia para o servidor
        # Poderia pensar que o procedimento abaixo está criando varios pacotes e enviando um por um?
        for linha in arquivo.readlines():
            connectionSocket.send(linha)

        print("Arquivo enviado com sucesso!")

        # Fecha o arquivo
        arquivo.close()

        # Fecha a conexao com o servidor
        connectionSocket.close()



def pesquisaArquivo( diretorioPadrao, buscaDownload ):
    pathName = diretorioPadrao
    for path, diretorio, arquivos in os.walk(pathName):
        for fileName in arquivos:
            if fileName == buscaDownload:
                arquivo = open("{}{}".format(path, fileName), 'r')
                return arquivo
	print("Arquivo Não Encontrado")
	return None
                

def criarHash(arquivo):
    if(arquivo == None):
        return None

    conteudoArquivo = arquivo.read()
    arquivo.close()

    m = md5()
    m.update(conteudoArquivo)
    hashmd5 = m.hexdigest()

    return hashmd5

if __name__ == '__main__':
    iniciarServidor()
