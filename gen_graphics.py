import os
import json
import argparse
import matplotlib.pyplot as plt

def analysis(n, neighborhood_sizes, times_to_run):

    info = {}

    for ns in neighborhood_sizes:
        info[ns] = {}
        for t in times_to_run:
            info[ns][t] = {}
            info[ns][t] = []
    
    # Ruta de la carpeta results/n
    results_dir = f"./results/{n}"

    # Verificar si la carpeta existe
    if not os.path.exists(results_dir):
        print(f"La carpeta {results_dir} no existe.")
        return

    for filename in os.listdir(results_dir):
        
        if filename.endswith(".json"):
            filepath = os.path.join(results_dir, filename)
            try:
                with open(filepath, "r") as json_file:
                    
                    data = json.load(json_file)
                    real_optima = data["real_optima"]
                    neighborhood_size = data["neighborhood_size"]

                    del data["real_optima"]
                    del data["neighborhood_size"]

                    keys = sorted(data.keys())

                    if real_optima != 0:

                        first_iter = True

                        for key in keys:

                            if first_iter:
                                for t in times_to_run:
                                    
                                    normalized_error = abs(data[key] - real_optima)/real_optima
                                    info[neighborhood_size][t].append(normalized_error)
                                    first_iter = False
                            else:

                                for t in times_to_run:
                                    if  int(key) < t:
                                        normalized_error = abs(data[key] - real_optima)/real_optima
                                        info[neighborhood_size][t][len(info[neighborhood_size][t]) - 1] = normalized_error
                    else:
                        
                        first_iter = True

                        for key in keys:

                            if first_iter:
                                for t in times_to_run:
                                    
                                    normalized_error = abs(data[key])
                                    info[neighborhood_size][t].append(normalized_error)
                                    first_iter = False
                            else:

                                for t in times_to_run:
                                    if  int(key) < t:
                                        normalized_error = abs(data[key])
                                        info[neighborhood_size][t][len(info[neighborhood_size][t]) - 1] = normalized_error


            except json.JSONDecodeError:
                print(f"Error al leer el archivo JSON: {filepath}")
    
    return info

def generate_plots(info, neighborhood_sizes, times_to_run, n):
    # Crear la figura y los subplots con disposición de 3x2
    fig, axes = plt.subplots(3, 2, figsize=(14, 18), sharey=True)
    fig.suptitle(f"Performance Analysis for n = {n}", fontsize=16, y=0.98)
    
    # Aplanar el array de ejes para facilitar la iteración
    axes = axes.flatten()
    
    # Definir colores para los boxplots
    colors = ['lightblue', 'lightgreen', 'salmon', 'khaki', 'lightcyan', 'plum']
    
    for idx, (ax, t) in enumerate(zip(axes, times_to_run)):
        # Preparar datos para el subplot
        x = neighborhood_sizes
        y = [info[ns][t] for ns in neighborhood_sizes]  # Arrays de errores normalizados

        # Calcular la media de errores normalizados
        means = [sum(errors) / len(errors) if errors else 0 for errors in y]

        # Crear el boxplot coloreado
        boxplot = ax.boxplot(y, positions=x, widths=0.6, patch_artist=True)
        
        # Colorear los boxplots
        for box, color in zip(boxplot['boxes'], colors[:len(x)]):
            box.set(facecolor=color)
        
        # Cambiar el color de la línea a azul
        ax.plot(x, means, marker="o", color="blue", label="Mean", linewidth=2)
        
        # Añadir el valor exacto de la media como texto
        for i, (xi, yi) in enumerate(zip(x, means)):
            ax.annotate(f"{yi:.8f}", (xi, yi), 
                      textcoords="offset points", 
                      xytext=(0, 10), 
                      ha='center', 
                      fontsize=8)
        
        ax.grid(True, linestyle='--', alpha=0.7)

        # Configurar el subplot
        ax.set_title(f"Time = {t} seconds")
        ax.set_xticks(x)
        ax.legend()

        # Ajustar la posición del título del eje x para evitar solapamientos
        ax.xaxis.set_label_coords(0.5, -0.15)

    # Ocultar subplots vacíos si hay menos tiempos que subplots
    for i in range(len(times_to_run), len(axes)):
        axes[i].set_visible(False)

    # Etiqueta del eje Y compartido para la primera columna
    for i in range(0, len(axes), 2):
        if i < len(times_to_run):
            axes[i].set_ylabel("Normalized Error")

    # Aumentar el espacio entre subplots
    plt.subplots_adjust(hspace=2, wspace=0.2)
    
    # Guardar la figura en alta resolución
    plt.tight_layout(rect=[0, 0, 1, 0.95])  # Ajustar para el título
    # Guardar con alta calidad
    plt.savefig(f"performance_analysis_n_{n}.png", 
                dpi=400,                     # Resolución muy alta
                bbox_inches='tight',         # Ajuste de bordes
                format='png',                # Formato explícito
                transparent=False,           # Fondo opaco
                facecolor='white',           # Color de fondo blanco
                edgecolor='none',            # Sin borde
                pad_inches=0.2)                 # Máxima calidad (aunque este parámetro es más para JPEG)
    

def gen_plots_of_reached_optima(info, neighborhood_sizes, times_to_run, n):
       # Crear la figura y los subplots con disposición de 3x2
    fig, axes = plt.subplots(3, 2, figsize=(14, 18), sharey=True)
    fig.suptitle(f"Reached global optima for n = {n}", fontsize=16, y=0.98)
    
    # Aplanar el array de ejes para facilitar la iteración
    axes = axes.flatten()
    
    for idx, (ax, t) in enumerate(zip(axes, times_to_run)):
        # Preparar datos para el subplot
        x = neighborhood_sizes
        y = [info[ns][t] for ns in neighborhood_sizes]  # Arrays de errores normalizados

        freqs = [sum(1 for error in reached if error == 0) / len(reached) if reached else 0 for reached in y]
        
        # Cambiar el color de la línea a azul
        ax.plot(x, freqs, marker="o", color="blue", linewidth=2)
        
        # Añadir el valor exacto de la media como texto
        for i, (xi, yi) in enumerate(zip(x, freqs)):
            ax.annotate(f"{yi:.8f}", (xi, yi), 
                      textcoords="offset points", 
                      xytext=(0, 10), 
                      ha='center', 
                      fontsize=8)
        
        ax.grid(True, linestyle='--', alpha=0.7)

        # Configurar el subplot
        ax.set_title(f"Time = {t} seconds")
        ax.set_xticks(x)

        # Ajustar la posición del título del eje x para evitar solapamientos
        ax.xaxis.set_label_coords(0.5, -0.15)

    # Ocultar subplots vacíos si hay menos tiempos que subplots
    for i in range(len(times_to_run), len(axes)):
        axes[i].set_visible(False)

    # Etiqueta del eje Y compartido para la primera columna
    for i in range(0, len(axes), 2):
        if i < len(times_to_run):
            axes[i].set_ylabel("Normalized Error")

    # Aumentar el espacio entre subplots
    plt.subplots_adjust(hspace=2, wspace=0.2)
    
    # Guardar la figura en alta resolución
    plt.tight_layout(rect=[0, 0, 1, 0.95])  # Ajustar para el título
    # Guardar con alta calidad
    plt.savefig(f"reached_optima_n_{n}.png", 
                dpi=400,                     # Resolución muy alta
                bbox_inches='tight',         # Ajuste de bordes
                format='png',                # Formato explícito
                transparent=False,           # Fondo opaco
                facecolor='white',           # Color de fondo blanco
                edgecolor='none',            # Sin borde
                pad_inches=0.2)                 # Máxima calidad (aunque este parámetro es más para JPEG)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Procesa los archivos JSON en results/n.")
    parser.add_argument("--n", type=int, default=40, help="El valor de n para navegar por results/n (por defecto: 40)")
    args = parser.parse_args()

    neighborhood_sizes = [2,3,4,5,6]

    times_to_run = {
        40: [5,10,15,20,40,60],
        100: [10,30,60,120,300,600]
    }
    
    info = analysis(args.n, neighborhood_sizes, times_to_run[args.n])

    generate_plots(info, neighborhood_sizes, times_to_run[args.n], args.n)

    gen_plots_of_reached_optima(info, neighborhood_sizes, times_to_run[args.n], args.n)