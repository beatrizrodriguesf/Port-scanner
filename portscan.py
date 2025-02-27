#!/usr/bin/python3

import sys, socket, multiprocessing, argparse

def port_scan(host_info, porta, family):
    s = socket.socket(family, socket.SOCK_STREAM)
    s.settimeout(1)
    
    if family == socket.AF_INET:
        x = s.connect_ex((host_info[0], int(porta)))
    elif family == socket.AF_INET6:
        x = s.connect_ex((host_info[0], int(porta), host_info[2], host_info[3]))
    if x == 0:
        try:
            service = socket.getservbyport(int(porta), "tcp")
            print(f"Porta {porta} [TCP] aberta {service}")
        except OSError:   
            print(f"Porta {porta} [TCP] aberta")

def main():

    ip = input("Digite o ip que deseja analisar:")
    portas = input("Digite as portas separadas por virgula (deixe em branco para analisar todas):")

    try:
        info = socket.getaddrinfo(ip, None) # Pega ipv6 e ipv4
        family = info[0][0]
        host_info = info[0][4]
    except socket.gaierror:
        try:
            host_info = (socket.gethostbyname(ip), 0) # pega ipv4 pelo nome do dominio
            family = socket.AF_INET
        except socket.gaierror:
            print(f"Host inválido, tente novamente")
            sys.exit(1)

    portas = portas.strip()

    if portas != "":
        for p in portas.split(","):
            port_scan(host_info, p, family)
    else:
        for p in range(1, 65535):
            port_scan(host_info, p, family)


if __name__ == "__main__":
    main()