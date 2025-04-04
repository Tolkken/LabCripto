import socket
import os
import sys
import time
import struct
import random

def checksum(data):
    s = 0
    n = len(data) % 2
    for i in range(0, len(data) - n, 2):
        s += data[i] + (data[i+1] << 8)
    if n:
        s += data[-1]
    while s >> 16:
        s = (s & 0xFFFF) + (s >> 16)
    return ~s & 0xFFFF

def crear_paquete_icmp(id, seq, caracter):
    tipo = 8  # Echo request
    codigo = 0
    chksum = 0
    identificador = id
    secuencia = seq
    payload = caracter.encode()

    # Estructura sin checksum
    cabecera = struct.pack('!BBHHH', tipo, codigo, chksum, identificador, secuencia)
    chksum = checksum(cabecera + payload)

    # Estructura con checksum real
    cabecera = struct.pack('!BBHHH', tipo, codigo, chksum, identificador, secuencia)
    return cabecera + payload

def enviar_stealth_ping(destino, mensaje):
    print(f"Enviando datos a {destino} en modo stealth...")

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    except PermissionError:
        print("❌ Necesitas permisos de administrador. Ejecuta con 'sudo'.")
        sys.exit(1)

    identificador = os.getpid() & 0xFFFF

    for i, caracter in enumerate(mensaje):
        paquete = crear_paquete_icmp(identificador, i, caracter)
        sock.sendto(paquete, (destino, 1))
        print(f"[{i}] Enviado carácter: '{caracter}'")

        # 💤 Espera aleatoria entre 0.5 a 3 segundos para ser menos predecible
        delay = random.uniform(0.5, 3.0)
        time.sleep(delay)

    sock.close()
    print("✅ Mensaje completo enviado en modo stealth (con delays aleatorios).")

if __name__ == "__main__":
    destino = input("Ingresa la IP de destino (ej. 192.168.1.10): ")
    mensaje = input("Ingresa el mensaje cifrado a enviar: ")
    enviar_stealth_ping(destino, mensaje)
