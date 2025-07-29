#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Convierte binario a texto ASCII
void binario_a_ascii(char *binario, char *resultado) {
    int len = strlen(binario);
    for (int i = 0; i < len; i += 8) {
        char byte[9];
        strncpy(byte, &binario[i], 8);
        byte[8] = '\0';
        resultado[i / 8] = strtol(byte, NULL, 2);
    }
    resultado[len / 8] = '\0';
}

// Verifica Fletcher
int verificar_fletcher(char *trama, int block_size) {
    int mod = (1 << block_size) - 1;
    int checksum_bits = 2 * block_size;
    int total_len = strlen(trama);

    if (total_len <= checksum_bits) {
        printf("Trama muy corta. Debe ser mayor a %d bits.\n", checksum_bits);
        return 0;
    }

    int data_len = total_len - checksum_bits;

    // Separar trama en datos y checksum
    char datos[data_len + 1];
    strncpy(datos, trama, data_len);
    datos[data_len] = '\0';

    char checksum_str[checksum_bits + 1];
    strncpy(checksum_str, trama + data_len, checksum_bits);
    checksum_str[checksum_bits] = '\0';

    // Dividir datos en bloques
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

int main() {
    char trama[2048];
    char texto[256];
    int block_size;

    printf("Ingrese tamaño de bloque (8, 16 o 32): ");
    scanf("%d", &block_size);
    printf("Ingrese la trama recibida:\n");
    scanf("%s", trama);

    int checksum_bits = 2 * block_size;
    int total_len = strlen(trama);
    int data_len = total_len - checksum_bits;

    if (verificar_fletcher(trama, block_size)) {
        char datos_bin[data_len + 1];
        strncpy(datos_bin, trama, data_len);
        datos_bin[data_len] = '\0';
        binario_a_ascii(datos_bin, texto);
        printf("Mensaje decodificado: %s\n", texto);
    } else {
        printf("Error detectado. Trama inválida.\n");
    }

    return 0;
}


// 010000010100100001000001010010000100000101001000
// 010000010100100001000001010010000100000101001000

// 011000010110101001100001000000000110000101101010011000010000000001100001011010100110000100000000
// 011000010110101001100001000000000110000101101010011001010000000001100001011010100110000101000000

// 01100001011010000010101111001001
// 01100001011010000010111111001001