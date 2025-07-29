
import socket
import random

# ------------------- CAPA DE APLICACIÓN -------------------

def generar_string_aleatorio(longitud):
    return ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ ') for _ in range(longitud))

# ------------------- CAPA DE PRESENTACIÓN -------------------

def ascii_to_bin(texto):
    return ''.join(format(ord(c), '08b') for c in texto)

# ------------------- CAPA DE ENLACE: Hamming -------------------

def calcular_r_para_m(m):
    for r in range(1, m + 10):
        if m + r + 1 <= 2 ** r:
            return r
    raise ValueError("No se puede encontrar un valor de r válido para m =", m)

def posicion_es_potencia_de_2(pos):
    return (pos & (pos - 1)) == 0

def hamming_emisor_general(data_bits):
    if any(b not in '01' for b in data_bits):
        raise ValueError("La entrada debe ser binaria.")
    m = len(data_bits)
    r = calcular_r_para_m(m)
    n = m + r
    resultado = ['x'] * n

    j = 0
    for i in range(1, n + 1):
        if not posicion_es_potencia_de_2(i):
            resultado[i - 1] = data_bits[j]
            j += 1

    for i in range(r):
        pos = 2 ** i
        suma = 0
        for j in range(1, n + 1):
            if j & pos:
                if resultado[j - 1] != 'x':
                    suma ^= int(resultado[j - 1])
        resultado[pos - 1] = str(suma)

    return ''.join(resultado)

# ------------------- CAPA DE ENLACE: Fletcher -------------------

def fletcher16_emisor(data_bits):
    sum1 = 0
    sum2 = 0
    for b in data_bits:
        sum1 = (sum1 + int(b)) % 255
        sum2 = (sum2 + sum1) % 255
    return data_bits + format(sum2, '08b') + format(sum1, '08b')

# ------------------- CAPA DE RUIDO -------------------

def aplicar_ruido(bits, probabilidad=0.01):
    return ''.join(str(int(b) ^ 1) if random.random() < probabilidad else b for b in bits)

# ------------------- MAIN -------------------

def main():
    # Parámetros
    algoritmo = "hamming"  # opciones: 'hamming', 'fletcher'
    probabilidad_error = 0.01
    cantidad_mensajes = 5
    longitud_mensaje = 10

    for i in range(cantidad_mensajes):
        print(f"\n--- Mensaje {i+1} ---")
        mensaje = generar_string_aleatorio(longitud_mensaje)
        print("Mensaje original:", mensaje)
        binario = ascii_to_bin(mensaje)

        if algoritmo == "hamming":
            codificado = hamming_emisor_general(binario)
        elif algoritmo == "fletcher":
            codificado = fletcher16_emisor(binario)
        else:
            raise ValueError("Algoritmo no reconocido.")

        print("Binario codificado:", codificado)
        con_ruido = aplicar_ruido(codificado, probabilidad_error)
        print("Con ruido aplicado:", con_ruido)

if __name__ == "__main__":
    main()

