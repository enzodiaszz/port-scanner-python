##Esse arquivo roda um Port Scanner (Retorna as portas abertas dentro de um range) e um banner grabber (Retorna o banner de identificação das portas abertas) e gera um relatório com as principais informações das portas.

import socket, json

ip = input("Digite o IP:  ")
porta1 = int(input("Digite a primeira porta a ser varrida: "))
porta2 = int(input("Digite a última porta a ser varrida: "))
portas_abertas = []
bloqueadas = []
fechadas = []

for porta in range(porta1, porta2 + 1):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #cria socket IPV4, TCP/IP
    s.settimeout(1)
    try:
        s.connect((ip, porta))
        try:
            banner = s.recv(1024).decode(errors="ignore")
        except socket.timeout:
            banner = "sem banner"
        portas_abertas.append({"porta": porta, "banner": banner})
    except socket.timeout:
        bloqueadas.append(porta)
    except socket.error:
        fechadas.append(porta)
    
    s.close() #Fecha socket

if len(portas_abertas) > 0:
    print(f"Portas abertas: {portas_abertas}")
else:
    print("Não foi encontrada nenhuma porta aberta")

relatorio = {
    "ip": ip,
    "range": f"{porta1}-{porta2}",
    "portas_abertas": portas_abertas,
    "total_bloqueadas": len(bloqueadas),
    "total_fechadas": len(fechadas)
}

with open("relatorio.json", "w") as f:
    json.dump(relatorio, f, indent=4)