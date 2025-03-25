#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <chrono>
#include <thread>
#include <cstdlib>
#include <unistd.h>

using namespace std;

vector<int> obtener_pids_apache() {
    vector<int> pids;
    FILE* fp = popen("pidof apache2", "r");
    if (!fp) {
        cerr << "Error al ejecutar pidof" << endl;
        exit(EXIT_FAILURE);
    }
    char buffer[1024];
    if (fgets(buffer, sizeof(buffer), fp) != nullptr) {
        string result(buffer);
        size_t pos = 0;
        while ((pos = result.find(" ")) != string::npos) {
            pids.push_back(stoi(result.substr(0, pos)));
            result.erase(0, pos + 1);
        }
        if (!result.empty()) {
            pids.push_back(stoi(result));
        }
    }
    pclose(fp);
    return pids;
}

float obtener_uso_cpu(int pid) {
    string stat_path = "/proc/" + to_string(pid) + "/stat";
    ifstream stat_file(stat_path);
    if (!stat_file.is_open()) {
        return 0.0;
    }

    string line;
    getline(stat_file, line);
    stat_file.close();

    int utime, stime;
    sscanf(line.c_str(), "%*d %*s %*c %*d %*d %*d %*d %*d %*u %*u %*u %*u %*u %d %d", &utime, &stime);
    return (utime + stime) / sysconf(_SC_CLK_TCK);
}

int main() {
    vector<int> pids = obtener_pids_apache();
    vector<float> cpu_usages;
    float intervalo = 0.5;
    int duracion_total = 10;
    float precio_kwh = 0.1305;

    auto tiempo_inicio = chrono::steady_clock::now();
    while (chrono::duration_cast<chrono::seconds>(chrono::steady_clock::now() - tiempo_inicio).count() < duracion_total) {
        float uso_total = 0.0;
        for (int pid : pids) {
            uso_total += obtener_uso_cpu(pid);
        }
        cpu_usages.push_back(uso_total);
        this_thread::sleep_for(chrono::milliseconds(static_cast<int>(intervalo * 1000)));
    }

    float promedio_cpu = 0.0;
    for (float uso : cpu_usages) {
        promedio_cpu += uso;
    }
    promedio_cpu /= cpu_usages.size();
    cout << "Uso promedio de CPU por segundo: " << promedio_cpu << "%\n";

    float consumo_w = (promedio_cpu / 1600) * 115;
    cout << "Consumo aproximado de CPU: " << consumo_w << " W\n";

    float precio_ws = precio_kwh / 3600000;
    float coste_por_segundo = consumo_w * precio_ws;
    float coste_por_hora = coste_por_segundo * 3600;
    float coste_total = coste_por_segundo * duracion_total;

    cout << "Coste aproximado de la medición: " << coste_total << " euros\n";
    cout << "Coste aproximado por segundo: " << coste_por_segundo << " euros\n";
    cout << "Coste aproximado por hora: " << coste_por_hora << " euros\n";

    return 0;
}

