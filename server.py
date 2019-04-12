import socket
import threading
import sys
import os
import time
import stat
import magic
from datetime import datetime
from datetime import date

mime = magic.Magic(mime=True)
weekDays = ("Mon","Tue","Wed","Thu","Fri","Sat","Sun")

#le o diretorio onde o servidor pesquesara os arquivos
diretorio = sys.argv[1]

#le a porta onde vai ser iniciado
try:
    porta = sys.argv[2]
except:
    porta = 80 #se nao informou a porta, a porta 80 sera definida

bind_ip = '127.0.0.1' #endereco
bind_port = int(porta) #porta

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)  # max backlog of connections

print 'Listening on {}:{}'.format(bind_ip, bind_port) #aguarda a conexao

def handle_client_connection(client_socket):
    request = client_socket.recv(4296)
    print 'Received\r\n{}'.format(request) #mostra a requisicao
    achou = False
    resposta = str(request)
    line = resposta.split()
    nome = line[1].split('/')
    if(line[0] == "GET"):
        dir = os.listdir(diretorio)
        for file in dir:
            if(str(file) == nome[1]):
                arq = nome[1];
                achou = True
                break
            else:
                achou = False

        if(achou == False):
            resposta = "HTTP/1.1 404 Not Found"

    else:
        resposta = "Metodo nao implementado"

    if(achou == True):
        now = datetime.now()
        data = date(year=now.year, month=now.month, day=now.day)
        f = open(arq,'rb')
        filePath = diretorio + '/' + arq
        fileStatsObj = os.stat ( filePath )
        modificationTime = time.ctime( fileStatsObj [ stat.ST_MTIME ] )
        st = os.stat(arq)
        tamanho = st.st_size
        tipo =  mime.from_file(arq)
        resposta = "HTTP/1.1 200 OK\r\nConnection: close\r\nDate: {}, {}/{}/{} {}:{}:{} {}\r\nServer: Matheus/1.0.0\n\rLast-Modfied: {}\n\rContent-Lenght: {}\r\nContent-Type: {}\n\r".format(data.weekday(), now.day, now.month, now.year, now.hour, now.minute, now.second, now.tzinfo, modificationTime, tamanho, tipo)
        client_socket.send(resposta)
        l = f.read(1024)
        while (l):
            client_socket.send(l)
            l = f.read(1024)
        f.close()
    else:
        client_socket.send(resposta)

    client_socket.close()
    print "Fim de conexao"

while True:
    client_sock, address = server.accept()
    print 'Accepted connection from {}:{}'.format(address[0], address[1])
    client_handler = threading.Thread(
        target=handle_client_connection,
        args=(client_sock,)  # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
    )
    client_handler.start()
