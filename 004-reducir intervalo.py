import psutil

# Solicita al usuario el PID del proceso a monitorizar
pid = int(input("Ingresa el PID del proceso: "))

try:
    proceso = psutil.Process(pid)
except psutil.NoSuchProcess:
    print("No se encontró ningún proceso con ese PID.")
    exit()

cpu_usages = []  # Lista para almacenar los porcentajes de uso de CPU
intervalo = 0.1   # Intervalo de muestreo en segundos
duracion_total = 10  # Duración total en segundos
cantidad_muestras = int(duracion_total / intervalo)

print(f"Monitorizando el proceso con PID {pid} durante {duracion_total} segundos con intervalos de {intervalo} s.")

for i in range(cantidad_muestras):
    # Se mide el uso de CPU durante el intervalo definido
    uso_cpu = proceso.cpu_percent(interval=intervalo)
    cpu_usages.append(uso_cpu)
    print(f"Muestra {i+1:03d}: Uso de CPU: {uso_cpu:.4f}%")

# Calcula y muestra el promedio de uso de CPU por segundo
promedio_cpu = sum(cpu_usages) / len(cpu_usages)
print(f"\nUso promedio de CPU por segundo: {promedio_cpu:.4f}%")
