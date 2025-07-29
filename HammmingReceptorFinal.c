#include <stdio.h>
#include <string.h>
#include <math.h>

// Extrae los 4 bits de datos desde un bloque Hamming(7,4)
// Las posiciones de datos están en bits 3, 5, 6, 7 (1-indexado)
void extraer_datos(char *bloque, char *datos) {
    datos[0] = bloque[2]; // bit 3
    datos[1] = bloque[4]; // bit 5
    datos[2] = bloque[5]; // bit 6
    datos[3] = bloque[6]; // bit 7
    datos[4] = '\0';
}

// Corrige un bloque Hamming(7,4)
int corregir_hamming(char *trama) {
    int posError = 0;

    for (int i = 0; i < 3; i++) {
        int pos = 1 << i;
        int parity = 0;
        for (int j = 1; j <= 7; j++) {
            if ((j & pos) && trama[7 - j] == '1') {
                parity ^= 1;
            }
        }
        if (parity) posError += pos;
    }

    if (posError > 0 && posError <= 7) {
        trama[7 - posError] = (trama[7 - posError] == '0') ? '1' : '0';
        printf("Error corregido en posición %d del bloque.\n", posError);
        return 1;
    } else if (posError == 0) {
        return 0;
    } else {
        return -1;
    }
}

// Convierte una cadena binaria a texto ASCII
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

int main() {
    char trama[1024];
    char datos_binarios[1024] = "";
    char texto[128];

    printf("Ingrese la trama recibida (concatenación de bloques Hamming de 7 bits):\n");
    scanf("%s", trama);

    int len = strlen(trama);
    if (len % 7 != 0) {
        printf("Longitud de trama inválida. Debe ser múltiplo de 7.\n");
        return 1;
    }

    for (int i = 0; i < len; i += 7) {
        char bloque[8] = {0};  // +1 para el '\0'
        strncpy(bloque, &trama[i], 7);

        corregir_hamming(bloque);

        char datos[5];
        extraer_datos(bloque, datos);
        strcat(datos_binarios, datos);
    }

    binario_a_ascii(datos_binarios, texto);
    printf("Mensaje decodificado: %s\n", texto);

    return 0;
}

