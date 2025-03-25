import psutil

# Solicita al usuario el PID del proceso a monitorizar
pid = int(input("Ingresa el PID del proceso: "))

try:
    proceso = psutil.Process(pid)
except psutil.NoSuchProcess:
    print("No se encontró ningún proceso con ese PID.")
    exit()

cpu_usages = []  # Lista para almacenar los porcentajes de uso de CPU

print("Monitorizando el proceso con PID:", pid)
print("La medición se realizará durante 10 segundos.")

# Realiza 10 mediciones (una por cada segundo)
for i in range(10):
    uso_cpu = proceso.cpu_percent(interval=1)
    cpu_usages.append(uso_cpu)
    
    # Obtiene la memoria residente y la convierte a MB
    memoria = proceso.memory_info().rss / (1024 * 1024)
    
    print(f"Segundo {i+1}: Uso de CPU: {uso_cpu:.4f}% | Uso de memoria: {memoria:.4f} MB")

# Calcula y muestra el promedio de uso de CPU
promedio_cpu = sum(cpu_usages) / len(cpu_usages)
print(f"\nUso promedio de CPU por segundo: {promedio_cpu:.4f}%")
