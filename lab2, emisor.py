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

def guardar_a_archivo(nombre, contenido):
    with open(nombre, "w") as f:
        f.write(contenido)
    print(f"Trama guardada en el archivo: {nombre}")

def main():
    print("=== EMISOR DE TRAMAS ===")
    print("1. Hamming generalizado")
    print("2. Fletcher Checksum")
    opcion = input("Selecciona el algoritmo (1 o 2): ")

    if opcion == '1':
        datos = input("Ingrese bits de datos (por ejemplo: 101101): ")
        codificado = hamming_emisor_general(datos)
        print("Trama Hamming codificada:", codificado)
        guardar_a_archivo("hamming_output.txt", codificado)

    elif opcion == '2':
        datos = input("Ingrese bits de datos (por ejemplo: 11010110): ")
        bsize = int(input("Tamaño de bloque (8, 16 o 32): "))
        codificado = fletcher_emisor_general(datos, block_size=bsize)
        print("Trama con Fletcher Checksum:", codificado)
        guardar_a_archivo("fletcher_output.txt", codificado)

    else:
        print("Opción inválida.")

if __name__ == "__main__":
    main()
