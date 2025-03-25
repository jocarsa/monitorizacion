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

# Precio medio diario de la electricidad en €/kWh
precio_kwh = 0.1305  # Actualizado al 25 de marzo de 2025

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
print(f"Consumo promedio de CPU: {consumo_w:.4f} W")

# Calcular el coste en euros
precio_ws = precio_kwh / 3_600_000  # Convertir €/kWh a €/W·s
energia_total_ws = consumo_w * duracion_total  # Energía total en W·s
coste = energia_total_ws * precio_ws
print(f"Coste aproximado de la medición: {coste:.10f} euros")
