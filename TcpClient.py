#coding: utf-8
from TcpServer import *
from socket import *

listServerName = ['10.3.1.51']
serverPort = 13000

while(True):
    pesquisaArquivo = raw_input('Digite o Arquivo A Ser Pesquisado:')

    if(pesquisaArquivo == "sair"):
        break

    listHashRecebidos = []
    for ip in listServerName:
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((ip, serverPort))
        clientSocket.send(pesquisaArquivo.encode('utf-8'))
        listHashRecebidos.append('download:'+ clientSocket.recv(1024).decode('utf-8'))
        clientSocket.close()

    for indice,hash in enumerate(listHashRecebidos):
        print("{} {}".format(indice,hash))

    text = input('digite o indice do hash na qual deseja fazer o download do arquivo:')
    indiceHash = int(text)
    if indiceHash < 0 or indiceHash >= len(listHashRecebidos):
        continue

    hashEscolhido = listHashRecebidos[indiceHash]
    ipEscolhido = listServerName[indiceHash]
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((ipEscolhido, serverPort))
    clientSocket.send(hashEscolhido.encode('utf-8'))

    # Cria um nome do arquivo
    # OBS.: O tipo do arquivo deve ser o mesmo que o cliente está enviando. Sendo assim se
    # se ele enviar um arquivo .txt, deverá alterar o nome abaixo para o mesmo tipo.
    arquivo = open(diretorioPadrao+pesquisaArquivo, 'wb')

    # Le os dados
    while True:
        # Recebe os dados do arquivo
        dados = clientSocket.recv(4096)

        # Verifica se acabou a transferencia
        if not dados:
            break

        # Escreve os dados do arquivo
        arquivo.write(dados)

    print("Transferencia concluida!")

    # Fecha o arquivo
    arquivo.close()

    # Finaliza a conexao
    clientSocket.close()
