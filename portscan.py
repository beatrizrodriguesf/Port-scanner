#!/usr/bin/python3

import sys, socket, multiprocessing, argparse
import ipaddress

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

def net_scan(addr):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)
    x = s.connect_ex((str(addr), 80))
    if x == 0:
        return 1
    else:
        return 0


def main():

    ip_rede = input("Digite o ip ou rede que deseja analisar:").strip()

    if len(ip_rede.split("/")) > 1:
        net = ipaddress.ip_network(ip_rede)
        for ip in net.hosts():
            if (net_scan(ip)):
                print(f"IP {ip} is live")
    else:
        portas = input("Digite as portas separadas por virgula (deixe em branco para analisar todas):")

        try:
            info = socket.getaddrinfo(ip_rede, None) # Pega ipv6 e ipv4
            family = info[0][0]
            host_info = info[0][4]
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