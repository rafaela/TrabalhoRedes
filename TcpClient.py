#coding: utf-8

from TcpServer import *
from socket import *

arquivos = open('arquivo_configuracao.txt', 'r')
texto = arquivos.read()
arquivos.close()

listServerName = texto.split('\n')

serverPort = 13000

while(True):
	pesquisaArquivo = raw_input('Digite o Arquivo A Ser Pesquisado ou sair para finalizar o programa:')

	if(pesquisaArquivo == "sair"):
		break

	listHashRecebidos = []
	for ip in listServerName:
		if ip == '':
			continue
		clientSocket = socket(AF_INET, SOCK_STREAM)
		clientSocket.connect((ip, serverPort))
		clientSocket.send(pesquisaArquivo.encode('utf-8'))
		listHashRecebidos.append('download:'+ clientSocket.recv(1024).decode('utf-8'))
		clientSocket.close()
	
	achou = False
	for indice,hash in enumerate(listHashRecebidos):
		if(not hash.__contains__("None")):
			achou = True
			print("{} {}".format(indice,hash))

	if achou == True:
		while(True):
			text =  raw_input('digite o indice do hash na qual deseja fazer o download do arquivo: ')
			if(text.isdigit()):
				if(int(text) < 0 or int (text) > len(listHashRecebidos)):	
					print('indice Incorreto!')
				else:
					break
			else:
				if(text.isdigit() == False):
					print('indice Incorreto!')
				else: 	
					break			
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

		dados = clientSocket.recv(4096)

		# Le os dados
		while(dados):
			# Escreve os dados do arquivo
			arquivo.write(dados)			

			# Recebe os dados do arquivo
			dados = clientSocket.recv(4096)
		
		# Fecha o arquivo
		arquivo.close()

		# Finaliza a conexao
		clientSocket.close()


		print("Transferencia concluida!")

		
	else:
		print('Arquivo não encontrado')



