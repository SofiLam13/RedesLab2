import socket
import random

# CAPA DE PRESENTACIÓN
def ascii_to_bin(text):
    return ''.join(format(ord(c), '08b') for c in text)

# CAPA DE ENLACE
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
            if j & pos and j != pos:
                suma ^= int(resultado[j - 1])
        resultado[pos - 1] = str(suma)

    return ''.join(resultado)

def fletcher_emisor_general(data, block_size=8):
    if block_size not in [8, 16, 32]:
        raise ValueError("El tamaño de bloque debe ser 8, 16 o 32")

    if len(data) % block_size != 0:
        data += '0' * (block_size - len(data) % block_size)

    blocks = [int(data[i:i+block_size], 2) for i in range(0, len(data), block_size)]
    sum1 = 0
    sum2 = 0
    mod = 2 ** block_size - 1

    for block in blocks:
        sum1 = (sum1 + block) % mod
        sum2 = (sum2 + sum1) % mod

    checksum = (sum2 << block_size) | sum1
    checksum_bits = format(checksum, f'0{2*block_size}b')
    return data + checksum_bits


# CAPA DE RUIDO
def aplicar_ruido(bits, prob=0.01):
    bits_ruidosos = []
    for bit in bits:
        if random.random() < prob:
            bits_ruidosos.append('0' if bit == '1' else '1')
        else:
            bits_ruidosos.append(bit)
    return ''.join(bits_ruidosos)


# CAPA DE TRANSMISIÓN, aqui ajustamos los parametros para mandarlo al código del receptor
def enviar_trama(trama_binaria, host='127.0.0.1', puerto=5000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, puerto))
        s.sendall(trama_binaria.encode())
        print("Trama enviada correctamente")


# CAPA DE APLICACIÓN 
def main():
    print("---EMISOR DE TRAMAS---")
    mensaje = input("Ingrese el mensaje a enviar: ")
    algoritmo = input("Seleccione algoritmo (hamming o fletcher): ")

    # Capa de presentación
    binario = ascii_to_bin(mensaje)
    print("ASCII binario:", binario)

    # Capa de enlace
    if algoritmo.lower() == 'hamming':
        codificada = ''.join([
            hamming_emisor_general(binario[i:i+4])
            for i in range(0, len(binario), 4)
        ])
    elif algoritmo.lower() == 'fletcher':
        block_size = int(input("Tamaño de bloque (8, 16 o 32): "))
        codificada = fletcher_emisor_general(binario, block_size=block_size)
    else:
        raise ValueError("Algoritmo no soportado")

    print("Trama con integridad:", codificada)

    # Capa de ruido
    prob_error = float(input("Probabilidad de error por bit (ej. 0.01): "))
    ruidosa = aplicar_ruido(codificada, prob=prob_error)
    print("Trama con ruido:", ruidosa)

    # Capa de transmisión, esta se encarga del socket, con este se conecta al codigo C
    #enviar_trama(ruidosa)

if __name__ == "__main__":
    main()

