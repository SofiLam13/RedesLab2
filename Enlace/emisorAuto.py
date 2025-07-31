
import socket
import random
import csv
import time

def generar_mensaje():
    longitud = random.randint(3, 10)
    return ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=longitud))

def ascii_a_binario(mensaje):
    return ''.join(f'{ord(c):08b}' for c in mensaje)

def binario_a_ascii(bits):
    return ''.join(chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8))

def codificar_hamming(mensaje):
    binario = ascii_a_binario(mensaje)
    resultado = ''
    for i in range(0, len(binario), 4):
        datos = binario[i:i+4].ljust(4, '0')
        p1 = str(int(datos[0]) ^ int(datos[1]) ^ int(datos[3]))
        p2 = str(int(datos[0]) ^ int(datos[2]) ^ int(datos[3]))
        p3 = str(int(datos[1]) ^ int(datos[2]) ^ int(datos[3]))
        resultado += p1 + p2 + datos[0] + p3 + datos[1:]  # p1 p2 d0 p3 d1 d2 d3
    return resultado

def codificar_fletcher(mensaje, block_size):
    binario = ascii_a_binario(mensaje)
    mod = (1 << block_size) - 1
    bloques = [binario[i:i+block_size].ljust(block_size, '0') for i in range(0, len(binario), block_size)]
    sum1 = sum2 = 0
    for bloque in bloques:
        val = int(bloque, 2)
        sum1 = (sum1 + val) % mod
        sum2 = (sum2 + sum1) % mod
    check = f'{sum1:0{block_size}b}' + f'{sum2:0{block_size}b}'
    return ''.join(bloques) + check

def inyectar_error(trama, prob_error):
    if random.random() > prob_error:
        return trama, 0, -1
    pos = random.randint(0, len(trama)-1)
    modificada = list(trama)
    modificada[pos] = '1' if modificada[pos] == '0' else '0'
    return ''.join(modificada), 1, pos

def enviar_y_recibir(trama, algoritmo, block_size):
    HOST = "127.0.0.1"
    PORT = 65432
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        if algoritmo == 'fletcher':
            mensaje = f"{algoritmo}|{block_size}|{trama}"
        else:
            mensaje = f"{algoritmo}|-|{trama}"
        s.sendall(mensaje.encode())
        respuesta = s.recv(1024).decode('utf-8', errors='ignore')
    return respuesta.strip()

def ejecutar_pruebas(algoritmo, cantidad=1000, block_size=16):
    archivo = f'resultados_{algoritmo}_16bits.csv'
    with open(archivo, 'w', newline='') as csvfile:
        campos = ['algoritmo', 'mensaje', 'trama_binaria', 'trama_ruido', 'error_inyectado', 'bit_error', 'respuesta_receptor', 'validez', 'tiempo_ms', 'probabilidad_error']
        writer = csv.DictWriter(csvfile, fieldnames=campos)
        writer.writeheader()

        for _ in range(cantidad):
            mensaje = generar_mensaje()
            if algoritmo == 'hamming':
                trama = codificar_hamming(mensaje)
            else:
                trama = codificar_fletcher(mensaje, block_size)

            prob_error = round(random.uniform(0.0, 0.2), 3)
            trama_ruido, inyectado, bit_error = inyectar_error(trama, prob_error)

            inicio = time.time()
            respuesta = enviar_y_recibir(trama_ruido, algoritmo, block_size)
            fin = time.time()

            partes = respuesta.split('|')
            estado = partes[0]
            recibido = partes[1] if len(partes) > 1 else ''
            validez = int(mensaje == recibido)

            writer.writerow({
                'algoritmo': algoritmo,
                'mensaje': mensaje,
                'trama_binaria': trama,
                'trama_ruido': trama_ruido,
                'error_inyectado': inyectado,
                'bit_error': bit_error,
                'respuesta_receptor': estado,
                'validez': validez,
                'tiempo_ms': round((fin - inicio) * 1000, 2),
                'probabilidad_error': prob_error
            })

if __name__ == '__main__':
    ejecutar_pruebas("hamming", cantidad=1000)
    ejecutar_pruebas("fletcher", cantidad=1000, block_size=16)
