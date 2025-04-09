#!/bin/bash

# Verifica que se hayan pasado los argumentos necesarios
if [ "$#" -ne 4 ]; then
    echo "Uso: $0 <n> <time_to_run> <start_instance> <end_instance>"
    exit 1
fi

n=$1
time_to_run=$2
start_instance=$3
end_instance=$4
neighborhood_sizes=(2 3 4 5 6)

# Crea la carpeta de resultados si no existe
mkdir -p ./results/$n

# Número máximo de trabajos en paralelo
max_parallel_jobs=6

# Función para controlar el número de trabajos en paralelo
function run_in_parallel {
    while [ "$(jobs | wc -l)" -ge "$max_parallel_jobs" ]; do
        # Espera a que haya espacio para más procesos
        sleep 1
    done
    # Ejecuta el comando en segundo plano
    "$@" &
}

# Itera sobre las instancias del rango especificado
for counter in $(seq $start_instance $end_instance); do
    for neighborhood_size in "${neighborhood_sizes[@]}"; do
        # Define el nombre del archivo de salida
        output_file=./results/$n/${counter}_${neighborhood_size}_${n}.json

        # Verifica si el archivo ya existe
        if [ -f "$output_file" ]; then
            echo "El archivo $output_file ya existe. Saltando..."
            continue
        fi

        # Ejecuta el comando en paralelo y redirige la salida al archivo correspondiente
        run_in_parallel ./analysis $n $counter $neighborhood_size $time_to_run > "$output_file"
    done
done

# Espera a que todos los procesos en segundo plano terminen
wait