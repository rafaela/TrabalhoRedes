from socket import *
import os
import threading

serverPort = 13000
diretorioPadrao = "C:/Users/Guilherme Magnus/PycharmProjects/TrabalhoPraticoRedes/"

def iniciarServidor():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(10)

    print('The server is to recieve')

    while 1:
        connectionSocket, addr = serverSocket.accept()
        connectionSocket.settimeout(2)
        threading.Thread(target= ouvirSocket, args=(connectionSocket,)).start()

    connectionSocket.close()

def pesquisaArquivo( diretorioPadrao, buscaDownload ):
    for path, diretorio, arquivos in os.walk( diretorioPadrao):
        for fileName in arquivos:
            if fileName == buscaDownload:
             print("{}".format(fileName))
            else:
                print("Arquivo Não Encontrado")
                break


def ouvirSocket(connectionSocket):
    buscaDownload = connectionSocket.recv(1024)
    buscaDownload = buscaDownload.decode('utf-8')
    if (buscaDownload.__contains__('download:')):
        pesquisaArquivo(diretorioPadrao, buscaDownload)
    else:
        connectionSocket.send(buscaDownload.encode('utf-8'))

if __name__ == '__main__':
    iniciarServidor()