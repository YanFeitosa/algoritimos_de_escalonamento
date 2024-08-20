# Scheduling Algorithms

Este projeto implementa três algoritmos de escalonamento de processos em sistemas operacionais: **First-Come, First-Served (FCFS)**, **Shortest Job First (SJF)** e **Round Robin com quantum 2 (RR)**. O código lê os tempos de chegada e de execução (burst) dos processos a partir de um arquivo e calcula o tempo médio de retorno, resposta e espera para cada algoritmo.

## Funcionalidades

- **FCFS (First-Come, First-Served)**
  - Executa os processos na ordem de chegada.

- **SJF (Shortest Job First)**
  - Executa o processo com o menor tempo de burst primeiro.

- **Round Robin com quantum 2 (RR)**
  - Executa os processos por fatias de tempo de 2 unidades (quantum), alternando entre os processos até que todos sejam completados.

## Estrutura do Código

- **`__init__(file_path)`**: 
  - Carrega os processos a partir de um arquivo.
  
- **`load_file(file_path)`**: 
  - Lê os tempos de chegada e burst dos processos de um arquivo e ordena os processos pelo tempo de chegada.
  
- **`return_average(method_name, turnaround_times, response_times, waiting_times)`**: 
  - Calcula os tempos médios de retorno, resposta e espera e os retorna em um formato de string.
  
- **`FCFS()`**: 
  - Implementação do algoritmo First-Come, First-Served.
  
- **`SJF()`**: 
  - Implementação do algoritmo Shortest Job First.
  
- **`RoundRobin2()`**: 
  - Implementação do algoritmo Round Robin com quantum 2.
  
- **`run()`**: 
  - Executa todos os algoritmos implementados.

## Requisitos

- Python 3.x

## Como Usar

1. **Preparar o Arquivo de Entrada**: 
   - Crie um arquivo de texto onde cada linha contém dois números inteiros separados por espaço: o primeiro número representa o tempo de chegada do processo, e o segundo, o tempo de burst.
   - Exemplo de arquivo `input.txt`:
     ```
     0 4
     1 3
     2 1
     3 5
     ```

2. **Executar o Script**:
   - No terminal, execute o script com o caminho para o arquivo de entrada como argumento:
     ```bash
     python escalonador.py input.txt
     ```

3. **Saída**:
   - O script executará os três algoritmos e imprimirá no terminal os tempos médios de retorno, resposta e espera para cada algoritmo. Exemplo de saída:
     ```
     FCFS 5.0 2.5 1.5
     SJF 4.5 2.0 1.0
     RR 6.0 3.0 2.0
     ```
