import argparse

class Scheduling_Algorithms:
    def __init__(self, file_path):
        # Inicializa a classe e carrega o arquivo de processos
        self.load_file(file_path)
    
    def load_file(self, file_path):
        # Carrega os processos do arquivo e os ordena pelo tempo de chegada
        self.processes = []
        with open(file_path, 'r') as arquive:
            for line in arquive:
                # Lê cada linha, separa o tempo de chegada e o burst time, e adiciona à lista de processos
                arrival, burst = map(int, line.split())
                self.processes.append((arrival, burst))
        
        # Ordena os processos pelo tempo de chegada
        self.processes.sort(key=lambda x: x[0]) 
        self.processes_quantity = len(self.processes)
        

    def return_average(self, method_name, turnaround_times, response_times, waiting_times):
        # Calcula os tempos médios de retorno, resposta e espera
        average_turnaround_time = sum(turnaround_times) / self.processes_quantity
        average_response_time = sum(response_times) / self.processes_quantity
        average_waiting_time = sum(waiting_times) / self.processes_quantity

        # Arredonda os valores médios para uma casa decimal
        processes_average_times = (
            round(average_turnaround_time, 1),
            round(average_response_time, 1),
            round(average_waiting_time, 1)
        )
        
        # Retorna uma string formatada com os tempos médios
        output = f'{method_name} {processes_average_times[0]} {processes_average_times[1]} {processes_average_times[2]}'
        return output
    
    def FCFS(self):
        # Implementação do algoritmo First-Come, First-Served
        completation_times = [0] * self.processes_quantity
        turnaround_times = [0] * self.processes_quantity
        response_times = [0] * self.processes_quantity
        waiting_times = [0] * self.processes_quantity
        
        for i in range(self.processes_quantity):
            arrival_time, burst_time = self.processes[i]
            
            if i == 0:
                # Para o primeiro processo, o tempo de conclusão é a soma do tempo de chegada e burst time
                completation_times[i] = arrival_time + burst_time
            else:
                # Para os processos subsequentes, verifica se há espera entre os processos
                if arrival_time > completation_times[i-1]:
                    completation_times[i] = arrival_time + burst_time
                else:
                    completation_times[i] = completation_times[i-1] + burst_time
        
            # Calcula os tempos de retorno, resposta e espera
            turnaround_times[i] = completation_times[i] - arrival_time
            waiting_times[i] = turnaround_times[i] - burst_time
            response_times[i] = waiting_times[i]
        
        # Imprime os tempos médios para o algoritmo FCFS
        print(self.return_average('FCFS', turnaround_times, waiting_times, response_times))
    
    def SJF(self):
        # Implementação do algoritmo Shortest Job First
        completion_times = [0] * self.processes_quantity
        turnaround_times = [0] * self.processes_quantity
        response_times = [0] * self.processes_quantity
        waiting_times = [0] * self.processes_quantity

        # Lista para verificar quais processos foram completados
        completed = [False] * self.processes_quantity

        current_time = 0
        completed_count = 0

        while completed_count < self.processes_quantity:
            # Seleciona o processo com o menor burst time que já tenha chegado
            shortest_index = None
            shortest_burst = float('inf')

            for i in range(self.processes_quantity):
                arrival_time, burst_time = self.processes[i]
                if not completed[i] and arrival_time <= current_time and burst_time < shortest_burst:
                    shortest_burst = burst_time
                    shortest_index = i

            if shortest_index is None:
                # Se nenhum processo foi encontrado, incrementa o tempo
                current_time += 1
            else:
                # Processa o processo selecionado
                arrival_time, burst_time = self.processes[shortest_index]
                start_time = current_time
                completion_times[shortest_index] = start_time + burst_time
                current_time += burst_time

                # Calcula os tempos de retorno, resposta e espera
                turnaround_times[shortest_index] = completion_times[shortest_index] - arrival_time
                waiting_times[shortest_index] = turnaround_times[shortest_index] - burst_time
                response_times[shortest_index] = waiting_times[shortest_index]

                completed[shortest_index] = True
                completed_count += 1

        # Imprime os tempos médios para o algoritmo SJF
        print(self.return_average('SJF', turnaround_times, response_times, waiting_times))

    
    def RoundRobin2(self):
        # Implementação do algoritmo Round Robin com quantum 2
        quantum = 2
        current_time = 0
        completion_times = [0] * self.processes_quantity
        turnaround_times = [0] * self.processes_quantity
        response_times = [-1] * self.processes_quantity # Inicia com -1 para identificar o primeiro acesso
        waiting_times = [0] * self.processes_quantity
        
        remaining_burst_times = [bt for _, bt in self.processes]
        process_queue = []
        
        while len(process_queue) > 0 or any(bt > 0 for bt in remaining_burst_times):
            # Adiciona processos que chegaram e ainda não foram adicionados à fila
            for i in range(self.processes_quantity):
                if self.processes[i][0] <= current_time and i not in process_queue and remaining_burst_times[i] > 0:
                    process_queue.append(i)
            
            if process_queue:
                i = process_queue.pop(0)
                arrival_time, burst_time = self.processes[i]
                
                if response_times[i] == -1:
                    # Define o tempo de resposta do processo
                    response_times[i] = current_time - arrival_time
                    
                if remaining_burst_times[i] <= quantum:
                    # Se o burst time é menor ou igual ao quantum, completa o processo
                    current_time += remaining_burst_times[i]
                    remaining_burst_times[i] = 0
                    completion_times[i] = current_time
                else:
                    # Caso contrário, executa o processo por quantum e adiciona de volta à fila
                    current_time += quantum
                    remaining_burst_times[i] -= quantum
                    for j in range(self.processes_quantity):
                        if self.processes[j][0] <= current_time and j not in process_queue and remaining_burst_times[j] > 0 and j != i:
                            process_queue.append(j)
                    process_queue.append(i)
                    
                if remaining_burst_times[i] == 0:
                    # Calcula os tempos de retorno e espera quando o processo é completado
                    turnaround_times[i] = completion_times[i] - arrival_time
                    waiting_times[i] = turnaround_times[i] - burst_time
                    
            else:
                # Se não há processos na fila, incrementa o tempo
                current_time += 1

        # Imprime os tempos médios para o algoritmo Round Robin
        print(self.return_average('RR', turnaround_times, response_times, waiting_times))

        
    def run(self):
        # Executa todos os algoritmos de escalonamento
        self.FCFS()
        self.SJF()
        self.RoundRobin2()
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scheduling Algorithms")
    parser.add_argument("file_path", help="Path to the input file containing process arrival and burst times")
    args = parser.parse_args()

    # Cria uma instância da classe Scheduling_Algorithms e executa os algoritmos
    scheduling = Scheduling_Algorithms(args.file_path)
    scheduling.run()
