import socket
import struct

def decodificar_cesar(texto, desplazamiento):
    resultado = ""
    for caracter in texto:
        if caracter.isalpha():
            base = ord('a') if caracter.islower() else ord('A')
            resultado += chr((ord(caracter) - base - desplazamiento) % 26 + base)
        else:
            resultado += caracter
    return resultado

def escuchar_paquetes_icmp(cantidad_caracteres_esperados):
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    print("🕵️ Escuchando ICMP Echo Requests...")

    mensaje = ""
    recibidos = 0

    while recibidos < cantidad_caracteres_esperados:
        paquete, _ = sock.recvfrom(1024)

        icmp_offset = 20
        icmp_payload = paquete[icmp_offset + 8:]

        if icmp_payload:
            try:
                caracter = icmp_payload.decode(errors="ignore")[0]  # Solo el primer carácter
                print(f"[{recibidos}] Recibido carácter: '{caracter}'")
                mensaje += caracter
                recibidos += 1
            except IndexError:
                continue

    print("✅ Mensaje completo recibido.\n")
    return mensaje

def es_palabra_reconocida(palabra):
    palabras_comunes = {
        "hola", "con", "todo", "respeto", "mensaje", "este", "es", "un", "de", "en", "el",
        "la", "seguridad", "criptografia", "redes", "respetuosamente"
    }
    return palabra in palabras_comunes

def determinar_mas_probable(opciones):
    puntuaciones = []
    for texto in opciones:
        palabras = texto.split()
        score = sum(1 for palabra in palabras if es_palabra_reconocida(palabra))
        puntuaciones.append(score)

    mejor_indice = puntuaciones.index(max(puntuaciones))
    return mejor_indice

def mostrar_descifrados(mensaje):
    opciones = [decodificar_cesar(mensaje, i) for i in range(26)]
    mejor_opcion = determinar_mas_probable(opciones)

    for i, opcion in enumerate(opciones):
        if i == mejor_opcion:
            print(f"[{i}] {opcion}  <-- ✅ Posible mensaje real")
        else:
            print(f"[{i}] {opcion}")

if __name__ == "__main__":
    try:
        cantidad = int(input("¿Cuántos caracteres esperas recibir (incluyendo espacios)?: "))
        mensaje = escuchar_paquetes_icmp(cantidad)
        print("\n🔓 Posibles decodificaciones del mensaje recibido:")
        mostrar_descifrados(mensaje)
    except KeyboardInterrupt:
        print("\n🛑 Recepción interrumpida.")
