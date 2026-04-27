import socket

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(("127.0.0.1", 9999)) #Endereço de loopback e porta aberta que vai enviar o banner em bytes
servidor.listen(1)

conn, addr = servidor.accept()
conn.send(b"FakeService 1.0 - Banner de teste\n") #codifica em bytes e envia
conn.close()