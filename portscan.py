#!/usr/bin/python3

import sys, socket
import ipaddress
from threading import Thread

def port_scan(host_info, porta, family):

    with socket.socket(family, socket.SOCK_STREAM) as s:
        s.settimeout(1)
    
        if family == socket.AF_INET:
            x = s.connect_ex((host_info[0], int(porta)))
        elif family == socket.AF_INET6:
            x = s.connect_ex((host_info[0], int(porta), host_info[2], host_info[3]))
        if x == 0:
            return 1
        return 0
    
def thread(lista_portas, host_info, family):
    for p in lista_portas:
        if port_scan(host_info, p, family):
            try:
                service = socket.getservbyport(int(p), "tcp")
                print(f"{p}/tcp - Aberta - {service}")
            except OSError:   
                print(f"{p}/tcp - Aberta - unknown")

def main():

    ip_rede = input("Digite o ip ou rede que deseja analisar: ").strip()

    if len(ip_rede.split("/")) > 1:
        net = ipaddress.ip_network(ip_rede)
        print(f"Escaneando rede {ip_rede}")

        for ip in net.hosts():
            info = socket.getaddrinfo(str(ip), None) # Pega ipv6 e ipv4
            family = info[0][0]
            host_info = info[0][4]

            if port_scan(host_info, 80, family):
                print(f"IP {host_info[0]} is live")

    else:
        portas = input("Digite as portas separadas por virgula ou um intervalo separado por hifen: ")

        try:
            info = socket.getaddrinfo(ip_rede, None) # Pega ipv6 e ipv4
            family = info[0][0]
            host_info = info[0][4]
        except socket.gaierror:
            print(f"Host inválido, tente novamente")
            sys.exit(1)

        portas = portas.strip()
        print(f"Escaneando portas do host {host_info[0]}")
        print("PORTA - STATUS - SERVICO")

        threads = []
        lista_portas = []

        if len(portas.split("-")) <= 1:
            lista_portas = portas.split(",")         
        else:
            portas = portas.split("-")
            inicio = int(portas[0])
            fim = int(portas[1])
            lista_portas = range(inicio, fim+1)

        n = len(lista_portas)//10
        resto = len(lista_portas)%10 
        
        for i in range(n):
            threads.append(Thread(target=thread(lista_portas[i*10:(i+1)*10], host_info, family)))
        if resto != 0:
            threads.append(Thread(target=thread(lista_portas[n*10:n*10+resto], host_info, family)))

        for t in threads:
            t.start()
        for t in threads:
            t.join()


if __name__ == "__main__":
    main()