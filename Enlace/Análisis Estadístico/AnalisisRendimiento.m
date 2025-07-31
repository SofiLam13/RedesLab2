data_hamming = readtable('resultados_hamming_16bits.csv');

archivos_fletcher = {
    'resultados_fletcher_16bits.csv'
    'resultados_fletcher_8y16bits1.csv'
    'resultados_fletcher_8y16bits2.csv'
    'resultados_fletcher_8y16bits3.csv'
    'resultados_fletcher_8y16bits4.csv'
    'resultados_fletcher_8y16bits5.csv'
    'resultados_fletcher_8y16bits6.csv'
    'resultados_fletcher_8y16bits7.csv'
    'resultados_fletcher_8y16bits8.csv'
    'resultados_fletcher_8y16bits9.csv'
    'resultados_fletcher_8y16bits10.csv'
};

data_fletcher = table();
for i = 1:length(archivos_fletcher)
    temp = readtable(archivos_fletcher{i});
    data_fletcher = [data_fletcher; temp];
end

% ------------------ HISTOGRAMAS DE ERROR ------------------

figure;
histogram(data_hamming.probabilidad_error, 20, 'FaceColor', 'b');
title('Distribución de la Probabilidad de Error - Hamming');
xlabel('Probabilidad de error');
ylabel('Frecuencia');

figure;
histogram(data_fletcher.probabilidad_error, 20, 'FaceColor', 'r');
title('Distribución de la Probabilidad de Error - Fletcher');
xlabel('Probabilidad de error');
ylabel('Frecuencia');

% ------------------ TIEMPOS PROMEDIO ------------------

prom_hamming = mean(data_hamming.tiempo_ms);
prom_fletcher = mean(data_fletcher.tiempo_ms);

fprintf('⏱ Tiempo promedio Hamming: %.3f ms\n', prom_hamming);
fprintf('⏱ Tiempo promedio Fletcher: %.3f ms\n', prom_fletcher);

% ------------------ PIE CHARTS ------------------

% Hamming
val_ham = [sum(~data_hamming.validez), sum(data_hamming.validez)];
figure;
pie(val_ham);
title('Validación de mensajes Hamming');
legend({'Incorrectos', 'Correctos'});

% Fletcher
val_flet = [sum(~data_fletcher.validez), sum(data_fletcher.validez)];
figure;
pie(val_flet);
title('Validación de mensajes Fletcher');
legend({'Incorrectos', 'Correctos'});

% ------------------ COMPARACIÓN DE RENDIMIENTO ------------------

% Porcentaje de éxito
porcentaje_hamming = 100 * sum(data_hamming.validez) / height(data_hamming);
porcentaje_fletcher = 100 * sum(data_fletcher.validez) / height(data_fletcher);

% Gráfico de barras comparando tiempo promedio y porcentaje de éxito
figure;
subplot(1,2,1);
bar([prom_hamming prom_fletcher]);
set(gca, 'XTickLabel', {'Hamming', 'Fletcher'});
ylabel('Tiempo promedio [ms]');
title('Comparación de Tiempo');

subplot(1,2,2);
bar([porcentaje_hamming porcentaje_fletcher]);
set(gca, 'XTickLabel', {'Hamming', 'Fletcher'});
ylabel('Porcentaje de mensajes válidos [%]');
title('Porcentaje de Éxito');

