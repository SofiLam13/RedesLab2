#define _WINSOCK_DEPRECATED_NO_WARNINGS
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <winsock2.h>

#pragma comment(lib, "ws2_32.lib")

#define PUERTO 65432
#define BUFFER_SIZE 4096

// ------------------ DECLARACIONES ------------------
void binario_a_ascii(char *binario, char *resultado);
int corregir_hamming(char *trama);
void extraer_datos(char *bloque, char *out);
char *procesar_hamming(char *trama, char *resultado);
int verificar_fletcher(char *trama, int block_size);

// ------------------ FUNCIONES AUXILIARES ------------------
void binario_a_ascii(char *binario, char *resultado) {
    int len = strlen(binario);
    for (int i = 0; i < len; i += 8) {
        char byte[9] = {0};
        strncpy(byte, &binario[i], 8);
        resultado[i / 8] = strtol(byte, NULL, 2);
    }
    resultado[len / 8] = '\0';
}

int corregir_hamming(char *trama) {
    int posError = 0;
    for (int i = 0; i < 3; i++) {
        int pos = 1 << i;
        int parity = 0;
        for (int j = 1; j <= 7; j++) {
            if ((j & pos) && trama[7 - j] == '1') parity ^= 1;
        }
        if (parity) posError += pos;
    }
    if (posError > 0 && posError <= 7) {
        trama[7 - posError] = trama[7 - posError] == '0' ? '1' : '0';
    }
    return posError;
}

void extraer_datos(char *bloque, char *out) {
    out[0] = bloque[2];
    out[1] = bloque[4];
    out[2] = bloque[5];
    out[3] = bloque[6];
    out[4] = '\0';
}

char *procesar_hamming(char *trama, char *resultado) {
    char datos_bin[2048] = "";
    int len = strlen(trama);
    for (int i = 0; i < len; i += 7) {
        char bloque[8] = {0};
        strncpy(bloque, &trama[i], 7);
        corregir_hamming(bloque);
        char extraidos[5] = {0};
        extraer_datos(bloque, extraidos);
        strcat(datos_bin, extraidos);
    }
    binario_a_ascii(datos_bin, resultado);
    return resultado;
}

int verificar_fletcher(char *trama, int block_size) {
    int mod = (1 << block_size) - 1;
    int checksum_bits = 2 * block_size;
    int total_len = strlen(trama);

    if (total_len <= checksum_bits) {
        printf("Trama muy corta. Debe ser mayor a %d bits.\n", checksum_bits);
        return 0;
    }

    int data_len = total_len - checksum_bits;

    char datos[data_len + 1];
    strncpy(datos, trama, data_len);
    datos[data_len] = '\0';

    char checksum_str[checksum_bits + 1];
    strncpy(checksum_str, trama + data_len, checksum_bits);
    checksum_str[checksum_bits] = '\0';

    int num_blocks = data_len / block_size;
    int sum1 = 0, sum2 = 0;
    for (int i = 0; i < num_blocks; i++) {
        char bloque[block_size + 1];
        strncpy(bloque, datos + i * block_size, block_size);
        bloque[block_size] = '\0';
        int valor = strtol(bloque, NULL, 2);
        sum1 = (sum1 + valor) % mod;
        sum2 = (sum2 + sum1) % mod;
    }

    int recibido = strtol(checksum_str, NULL, 2);
    int calculado = (sum2 << block_size) | sum1;

    printf("🔍 Calculado: %d, Recibido: %d\n", calculado, recibido);

    if (calculado == recibido) {
        return 1;
    } else {
        return 0;
    }
}

// ------------------ MAIN ------------------
int main() {
    WSADATA wsa;
    SOCKET server_fd, cliente;
    struct sockaddr_in addr;
    char buffer[BUFFER_SIZE] = {0};

    WSAStartup(MAKEWORD(2, 2), &wsa);
    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    addr.sin_family = AF_INET;
    addr.sin_port = htons(PUERTO);
    addr.sin_addr.s_addr = INADDR_ANY;

    bind(server_fd, (struct sockaddr*)&addr, sizeof(addr));
    listen(server_fd, 1);
    printf("📡 Esperando conexión en el puerto %d...\n", PUERTO);

    while (1) {
        cliente = accept(server_fd, NULL, NULL);
        int bytes = recv(cliente, buffer, BUFFER_SIZE - 1, 0);
        if (bytes <= 0) {
            closesocket(cliente);
            continue;
        }
        buffer[bytes] = '\0';

        char algoritmo[16] = {0}, block_size_str[8] = {0}, trama[2048] = {0};
        sscanf(buffer, "%[^|]|%[^|]|%s", algoritmo, block_size_str, trama);

        char resultado[2048] = {0};
        if (strcmp(algoritmo, "hamming") == 0) {
            procesar_hamming(trama, resultado);
            char mensaje[256] = {0};
            sprintf(mensaje, "correcta|%s", resultado);
            send(cliente, mensaje, strlen(mensaje), 0);
        } else if (strcmp(algoritmo, "fletcher") == 0) {
            int bs = atoi(block_size_str);
            char mensaje[256] = {0};
            if (verificar_fletcher(trama, bs)) {
                int checksum_bits = 2 * bs;
                int total_len = strlen(trama);
                int data_len = total_len - checksum_bits;
                char datos_bin[data_len + 1];
                strncpy(datos_bin, trama, data_len);
                datos_bin[data_len] = '\0';
                binario_a_ascii(datos_bin, resultado);
                sprintf(mensaje, "correcta|%s", resultado);
            } else {
                sprintf(mensaje, "error_detectado|");
            }
            send(cliente, mensaje, strlen(mensaje), 0);
        } else {
            char error_msg[] = "algoritmo_desconocido|";
            send(cliente, error_msg, strlen(error_msg), 0);
        }

        closesocket(cliente);
        memset(buffer, 0, sizeof(buffer));
    }
    closesocket(server_fd);
    WSACleanup();
    return 0;
}
