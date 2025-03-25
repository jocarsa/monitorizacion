import psutil
import subprocess
import time

def obtener_pid_apache():
    try:
        # Usar pidof para obtener el PID de apache2
        pid = int(subprocess.check_output(["pidof", "apache2"]).decode().strip().split()[0])
        return pid
    except subprocess.CalledProcessError:
        print("No se encontró el proceso Apache.")
        exit()

pid = obtener_pid_apache()

try:
    proceso = psutil.Process(pid)
except psutil.NoSuchProcess:
    print("No se encontró ningún proceso con ese PID.")
    exit()

cpu_usages = []         # Lista para almacenar los porcentajes de uso de CPU
intervalo = 0.1         # Intervalo de muestreo en segundos
duracion_total = 10     # Duración total en segundos
cantidad_muestras = int(duracion_total / intervalo)

# Precio de la electricidad en €/kWh
precio_kwh = 0.1305

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

# Calcular el coste en euros
precio_ws = precio_kwh / 3600000  # Convertir €/kWh a €/W·s
coste_por_segundo = consumo_w * precio_ws
coste_por_hora = coste_por_segundo * 3600
coste_total = coste_por_segundo * duracion_total

print(f"Coste aproximado de la medición: {coste_total:.10f} euros")
print(f"Coste aproximado por segundo: {coste_por_segundo:.10f} euros")
print(f"Coste aproximado por hora: {coste_por_hora:.10f} euros")
