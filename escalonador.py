class Scheduling_Algorithms:
    def __init__(self, file_path):
        self.load_file(file_path)
    
    def load_file(self, file_path):
        self.processes = []
        with open(file_path, 'r') as arquive:
            for line in arquive:
                arrival, burst = map(int, line.split())
                
                self.processes.append((arrival, burst))
                
        self.processes.sort(key=lambda x: x[0]) 
        self.processes_quantity = len(self.processes)
        

    
    def return_average(self, method_name, turnaround_times, response_times, waiting_times):
        average_turnaround_time = sum(turnaround_times) / self.processes_quantity
        average_response_time = sum(response_times) / self.processes_quantity
        average_waiting_time = sum(waiting_times) / self.processes_quantity

        processes_average_times = (
            round(average_turnaround_time, 1),
            round(average_response_time, 1),
            round(average_waiting_time, 1)
        )
        
        output = f'{method_name} {processes_average_times[0]} {processes_average_times[1]} {processes_average_times[2]}'
        return output
    
    def FCFS(self):
        
        completation_times = [0] * self.processes_quantity
        turnaround_times = [0] * self.processes_quantity
        response_times = [0] * self.processes_quantity
        waiting_times = [0] * self.processes_quantity
        
        for i in range(self.processes_quantity):
            arrival_time, burst_time = self.processes[i]
            
            if i == 0:
                completation_times[i] = arrival_time + burst_time
            else:
                if arrival_time > completation_times[i-1]:
                    completation_times[i] = arrival_time + burst_time
                else:
                    completation_times[i] = completation_times[i-1] + burst_time
        
            turnaround_times[i] = completation_times[i] - arrival_time
            waiting_times[i] = turnaround_times[i] - burst_time
            response_times[i] = waiting_times[i]
        
        print(self.return_average('FCFS', turnaround_times, waiting_times, response_times))
    
    def SJF(self):
        # Inicializando as listas para armazenar os tempos
        completion_times = [0] * self.processes_quantity
        turnaround_times = [0] * self.processes_quantity
        response_times = [0] * self.processes_quantity
        waiting_times = [0] * self.processes_quantity

        # Lista para verificar quais processos já foram completados
        completed = [False] * self.processes_quantity

        current_time = 0
        completed_count = 0

        while completed_count < self.processes_quantity:
            # Selecionar o processo com o menor burst time que já tenha chegado
            shortest_index = None
            shortest_burst = float('inf')

            for i in range(self.processes_quantity):
                arrival_time, burst_time = self.processes[i]
                if not completed[i] and arrival_time <= current_time and burst_time < shortest_burst:
                    shortest_burst = burst_time
                    shortest_index = i

            if shortest_index is None:
                # Se nenhum processo foi encontrado, incrementar o tempo
                current_time += 1
            else:
                # Processar o processo selecionado
                arrival_time, burst_time = self.processes[shortest_index]
                start_time = current_time
                completion_times[shortest_index] = start_time + burst_time
                current_time += burst_time

                turnaround_times[shortest_index] = completion_times[shortest_index] - arrival_time
                waiting_times[shortest_index] = turnaround_times[shortest_index] - burst_time
                response_times[shortest_index] = waiting_times[shortest_index]

                completed[shortest_index] = True
                completed_count += 1

        print(self.return_average('SJF', turnaround_times, response_times, waiting_times))

    
    def RoundRobin2(self):
        quantum = 2
        current_time = 0
        completion_times = [0] * self.processes_quantity
        turnaround_times = [0] * self.processes_quantity
        response_times = [-1] * self.processes_quantity  # Inicializando com -1 para identificar o primeiro acesso
        waiting_times = [0] * self.processes_quantity

        remaining_burst_times = [bt for _, bt in self.processes]
        process_queue = []

        while len(process_queue) > 0 or any(bt > 0 for bt in remaining_burst_times):
            # Adiciona processos que chegaram ao tempo atual à fila
            for i in range(self.processes_quantity):
                if self.processes[i][0] <= current_time and i not in process_queue and remaining_burst_times[i] > 0:
                    process_queue.append(i)

            if process_queue:
                i = process_queue.pop(0)
                arrival_time, burst_time = self.processes[i]

                if response_times[i] == -1:
                    response_times[i] = current_time - arrival_time

                if remaining_burst_times[i] <= quantum:
                    current_time += remaining_burst_times[i]
                    remaining_burst_times[i] = 0
                    completion_times[i] = current_time
                else:
                    current_time += quantum
                    remaining_burst_times[i] -= quantum
                    process_queue.append(i)

                # Calcula turnaround e waiting times após o processo terminar
                if remaining_burst_times[i] == 0:
                    turnaround_times[i] = completion_times[i] - arrival_time
                    waiting_times[i] = turnaround_times[i] - burst_time
            else:
                current_time += 1  # Avança o tempo para o próximo processo

        print(self.return_average('RR', turnaround_times, response_times, waiting_times))

        
    def run(self):
        #self.FCFS()
        #
        # self.SJF()
        self.RoundRobin2()
        
scheduling = Scheduling_Algorithms('test.txt')
scheduling.run()
