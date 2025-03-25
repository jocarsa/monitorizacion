import psutil
import time

# Solicita al usuario el PID del proceso a monitorizar
pid = int(input("Ingresa el PID del proceso: "))

try:
    proceso = psutil.Process(pid)
except psutil.NoSuchProcess:
    print("No se encontró ningún proceso con ese PID.")
    exit()

cpu_usages = []         # Lista para almacenar los porcentajes de uso de CPU
intervalo = 0.1         # Intervalo de muestreo en segundos
duracion_total = 10     # Duración total en segundos
cantidad_muestras = int(duracion_total / intervalo)

# Llamada de calentamiento para inicializar la medición
proceso.cpu_percent(interval=None)

# Se realizan las mediciones sin imprimir cada muestra
for _ in range(cantidad_muestras):
    uso_cpu = proceso.cpu_percent(interval=intervalo)
    cpu_usages.append(uso_cpu)

# Calcula y muestra el promedio de uso de CPU con 4 decimales
promedio_cpu = sum(cpu_usages) / len(cpu_usages)
print(f"Uso promedio de CPU por segundo: {promedio_cpu:.4f}%")

# Calcular el consumo en vatios (considerando el 100% como 1600%)
consumo_w = (promedio_cpu / 1600) * 115
print(f"Consumo aproximado de CPU: {consumo_w:.4f} W")
