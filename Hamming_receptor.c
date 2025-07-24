#include <stdio.h>
#include <string.h>
#include <math.h>

int detectarYCorregirHamming(char *trama) {
    int n = strlen(trama);
    int r = 0, i, j, posError = 0;

    // Calcular cuántos bits de paridad hay (r) según longitud n
    while ((int)pow(2, r) < n + 1) r++;

    for (i = 0; i < r; i++) {
        int pos = (int)pow(2, i);
        int parity = 0;
        for (j = pos; j <= n; j++) {
            if ((j >> i) & 1) {
                parity ^= (trama[n - j] - '0');
            }
        }
        if (parity) {
            posError += pos;
        }
    }

    if (posError) {
        printf("Se detectó y corrigió un error en la posición %d\n", posError);
        trama[n - posError] = (trama[n - posError] == '0') ? '1' : '0';
        printf("Trama corregida: %s\n", trama);
        return 1;
    } else {
        printf("No se detectaron errores. Trama válida: %s\n", trama);
        return 0;
    }
}

int main() {
    char trama[40];
    printf("Ingrese la trama recibida (bits con paridad): ");
    scanf("%s", trama);
    detectarYCorregirHamming(trama);
    return 0;
}
