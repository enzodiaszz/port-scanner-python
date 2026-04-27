##Esse arquivo roda um Port Scanner (Retorna as portas abertas dentro de um range) e um banner grabber (Retorna o banner de identificação das portas abertas) e gera um relatório com as principais informações das portas.

import socket, json, requests

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
        vulnerabilidades = []
        if banner != "sem banner":
            servico = banner.split()[0].split("-")[0]
            api_url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={servico}"
            try:
                resposta = requests.get(api_url)
                dados = resposta.json()
                if len(dados["vulnerabilities"]) > 0:                
                    for item in dados["vulnerabilities"]:
                        id_cve = item["cve"]["id"]
                        descricao = item["cve"]["descriptions"][0]["value"]
                        vulnerabilidades.append({"id": id_cve, "descricao": descricao})
            except:
                pass
        portas_abertas.append({"porta": porta, "banner": banner, "vulnerabilidades": vulnerabilidades})
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