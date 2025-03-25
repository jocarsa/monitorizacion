import psutil
import time

# Solicita al usuario el PID del proceso a monitorizar
pid = int(input("Ingresa el PID del proceso: "))

try:
    proceso = psutil.Process(pid)
except psutil.NoSuchProcess:
    print("No se encontró ningún proceso con ese PID.")
    exit()

print("Monitorizando el proceso con PID:", pid)
print("Presiona Ctrl+C para detener.")

try:
    while True:
        # cpu_percent mide el uso de CPU en el intervalo dado (en este caso 1 segundo)
        uso_cpu = proceso.cpu_percent(interval=1)
        # Obtenemos la información de memoria; rss es la memoria residente en bytes
        memoria = proceso.memory_info().rss / (1024 * 1024)  # Convertir a MB
        
        print(f"Uso de CPU: {uso_cpu:.2f}% | Uso de memoria: {memoria:.2f} MB")
        # El intervalo ya está gestionado en cpu_percent, por lo que no es necesario otro time.sleep()
except KeyboardInterrupt:
    print("Monitoreo detenido.")
