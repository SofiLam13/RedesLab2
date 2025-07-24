#include <stdio.h>
#include <string.h>

int verificarChecksum(char *trama, int longitud) {
    unsigned int sum1 = 0, sum2 = 0;
    int i;

    for (i = 0; i < longitud - 2; i++) {
        sum1 = (sum1 + trama[i]) % 255;
        sum2 = (sum2 + sum1) % 255;
    }

    unsigned int recv_sum1 = (unsigned char)trama[longitud - 2];
    unsigned int recv_sum2 = (unsigned char)trama[longitud - 1];

    printf("Calculado: sum1 = %d, sum2 = %d\n", sum1, sum2);
    printf("Recibido : sum1 = %d, sum2 = %d\n", recv_sum1, recv_sum2);

    if (sum1 == recv_sum1 && sum2 == recv_sum2) {
        printf("Trama válida. No se detectaron errores.\n");
        return 0;
    } else {
        printf("Error detectado en la trama. Se descarta.\n");
        return 1;
    }
}

int main() {
    char trama[102];
    printf("Ingrese la trama completa con checksum: ");
    scanf("%s", trama);
    verificarChecksum(trama, strlen(trama));
    return 0;
}
