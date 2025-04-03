import os
import json
import matplotlib.pyplot as plt
import numpy as np
from itertools import product



def gen_graphics(path, n):
    
    info = {}

    neighborhood_sizes = [2,3,4,5,6]
    times_to_run = [5,10,15,20, 40, 60] if n == 40 else [60, 120, 180, 240]

    for (run_time, neighborhood_size) in product(times_to_run, neighborhood_sizes):
        info.setdefault(run_time, {})
        info[run_time].setdefault(neighborhood_size, {})
        info[run_time][neighborhood_size]["performances"] = []
        info[run_time][neighborhood_size]["norm_relative_errors"] = []


    # Leer los archivos JSON y organizar los datos
    for file in os.listdir(path):
        file_dict = json.load(open(os.path.join(path, file)))
        run_time = file_dict["time_to_run"]
        neighborhood_size = file_dict["neighborhood_size"]

        if file_dict["real_optimal_value"] > 1: 
            info[run_time][neighborhood_size]["performances"].append(file_dict["real_optimal_value"]/file_dict["best_value"])


    rows = (len(info) + 1) // 2  # Número de filas necesarias para 2 columnas
    cols = 2  # Número de columnas
    fig, axes = plt.subplots(rows, cols, figsize=(12, 6 * rows), sharex=True)
    fig.suptitle(f"Performance Analysis for n = {n}", fontsize=16)

    if len(info) == 1:
        axes = [axes]  # Asegurarse de que `axes` sea iterable si hay un solo subplot
    
    axes = axes.flatten()  # Aplanar la matriz de ejes para facilitar la iteración

    for ax, (run_time, neighborhood_data) in zip(axes, sorted(info.items())):
        neighborhood_sizes = sorted(neighborhood_data.keys())
        performances = [
            [p for p in neighborhood_data[size]["performances"]] for size in neighborhood_sizes
        ]

        # Crear un boxplot para cada tamaño de vecindario
        ax.boxplot(
            performances,
            tick_labels=neighborhood_sizes,
            showmeans=True,
            patch_artist=True
        )
        ax.set_title(f"Run Time: {run_time} seconds")
        ax.set_xlabel("Neighborhood Size")
        ax.set_ylabel("Performance")

        ax.set_yscale("log")
        ax.set_ylim(bottom=(0.7 if n == 40 else 0.1), top=1)

        ax.grid(True, linestyle="--", alpha=0.7)

        # Calcular y graficar las medias
        means = [sum(p) / (len(p) + 1) for p in performances]
        ax.plot(
            range(1, len(neighborhood_sizes) + 1),
            means,
            marker='o',
            linestyle='-',
            color='darkblue',
            label='Mean'
        )

        # Agregar etiquetas con los valores exactos de las medias
        for i, mean in enumerate(means):
            ax.annotate(
                f"{mean:.4f}",  # Formato con 4 decimales
                (i + 1, mean),  # Coordenadas del punto
                textcoords="offset points",
                xytext=(0, 5),  # Desplazamiento en píxeles (x, y)
                ha='center',  # Alinear horizontalmente al centro
                fontsize=8  # Tamaño de la fuente
            )

        ax.legend()

    plt.tight_layout(rect=[0, 0, 1, 0.96], h_pad=4)  # Ajustar el diseño para evitar solapamientos
    plt.savefig(f"performance_analysis_n{n}.png", dpi=400)
    #plt.show()


# Ejemplo de uso
if __name__ == "__main__":
    
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--n", type=int)
    args = parser.parse_args()
    n = args.n
    # n = 40
    
    path = "./results/" + str(n)  +"/"  # Ruta a los archivos JSON
    gen_graphics(path, n)





