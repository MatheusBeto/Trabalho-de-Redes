import socket
import sys

entrada = sys.argv[1]
try:
    entrada2 = sys.argv[2]
except:
    entrada2 = 80

divisao = entrada.split("/")

hostname = divisao[0]
divisao[0] = ""
pagina = "/".join(divisao)
print pagina

port = int(entrada2)

print "hostname: {}".format(hostname)
print "pagina: {}".format(pagina)
print "prot: {}".format(port)

# create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
iphost =  socket.gethostbyname(hostname)

# connect the client
client.connect((iphost, port))

requisicao = "GET {} HTTP/1.1\r\nHost: {}\r\nConnection: keep-alive\r\nUser-agent: Matheus/1.0.0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3\r\nAccept-language: pt-BR\r\n".format(pagina, hostname)

print requisicao
client.send(requisicao)

# receive the response data (4096 is recommended buffer size)
response = client.recv(4096)


with open('received_file.html', 'wb') as f:
    while True:
        data = client.recv(1024)
        if not data:
            break
            # write data to a file
        f.write(data)
f.close()


print response
client.close()
