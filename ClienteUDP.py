#coding: utf-8

from socket import *

listServerName = ['127.0.0.1','192.168.1.106']
serverPort = 13000

while(True):
    pesquisaArquivo = input('Digite o Arquivo A Ser Pesquisado:')

    if(pesquisaArquivo == "sair"):
        break

    listHashRecebidos = []
    for ip in listServerName:
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((ip, serverPort))
        clientSocket.send(pesquisaArquivo.encode('utf-8'))
        listHashRecebidos.append(clientSocket.recv(1024).decode('utf-8'))
    for indice,hash in enumerate(listHashRecebidos):
        print("{} {}".format(indice,hash))

    text = input('digite o indice do hash na qual deseja fazer o download do arquivo')
    ipEscolhido = listHashRecebidos[int(text)]

    clientSocket.connect((ipEscolhido, serverPort))
    clientSocket.send("download:{}".format(pesquisaArquivo))

clientSocket.close()
