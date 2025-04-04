def cifrado_cesar(texto, desplazamiento):
    resultado = ""
    for caracter in texto:
        if caracter.isalpha():
            base = ord('a') if caracter.islower() else ord('A')
            resultado += chr((ord(caracter) - base + desplazamiento) % 26 + base)
        else:
            resultado += caracter
    return resultado


if __name__ == "__main__":
    texto = input("Ingresa el texto a cifrar: ").lower()

    while True:
        try:
            desplazamiento = int(input("Ingresa el desplazamiento (número entero): "))
            break
        except ValueError:
            print("Por favor, ingresa un número válido.")

    resultado = cifrado_cesar(texto, desplazamiento)
    print("Texto cifrado:", resultado)
