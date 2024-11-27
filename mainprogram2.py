from collections import deque

# Define the Process class to hold process information
class Process:
    def __init__(self, pid, arrival_time, service_time, priority=None):
        self.pid = pid
        self.arrival_time = arrival_time
        self.service_time = service_time
        self.remaining_time = service_time
        self.priority = priority
        self.response_time = None
        self.turnaround_time = None
        self.completion_time = None
        self.start_time = None
        self.waiting_time = None


# Simulate Round Robin
def round_robin(queue, quantum, current_time):
    executed_processes = []
    process_queue = deque(queue)
    while process_queue:
        process = process_queue.popleft()
        if process.start_time is None:
            process.start_time = current_time

        if process.remaining_time > quantum:
            current_time += quantum
            process.remaining_time -= quantum
            executed_processes.append((process.pid, current_time))
            process_queue.append(process)
        else:
            current_time += process.remaining_time
            process.remaining_time = 0
            process.completion_time = current_time
            executed_processes.append((process.pid, current_time))
    return executed_processes, current_time


# Simulate FCFS
def fcfs(queue, current_time):
    executed_processes = []
    for process in queue:
        if process.start_time is None:
            process.start_time = current_time
        current_time += process.remaining_time
        process.remaining_time = 0
        process.completion_time = current_time
        executed_processes.append((process.pid, current_time))
    return executed_processes, current_time


# Simulate LCFS
def lcfs(queue, current_time):
    executed_processes = []
    stack = list(queue[::-1]) # LCFS works like a stack
    while stack:
        process = stack.pop()
        if process.start_time is None:
            process.start_time = current_time
        current_time += process.remaining_time
        process.remaining_time = 0
        process.completion_time = current_time
        executed_processes.append((process.pid, current_time))
    return executed_processes, current_time


# Simulate Priority Queue
def priority_queue(queue, current_time):
    executed_processes = []
    queue = sorted(queue, key=lambda x: x.priority) # Sort by priority (lower is higher)
    for process in queue:
        if process.start_time is None:
            process.start_time = current_time
        current_time += process.remaining_time
        process.remaining_time = 0
        process.completion_time = current_time
        executed_processes.append((process.pid, current_time))
    return executed_processes, current_time


# Simulate Shortest Job First (SJF)
def shortest_job_first(queue, current_time):
    executed_processes = []
    queue = sorted(queue, key=lambda x: x.service_time) # Sort by service time
    for process in queue:
        if process.start_time is None:
            process.start_time = current_time
        current_time += process.remaining_time
        process.remaining_time = 0
        process.completion_time = current_time
        executed_processes.append((process.pid, current_time))
    return executed_processes, current_time


# Simulate Longest Job First (LJF)
def longest_job_first(queue, current_time):
    executed_processes = []
    queue = sorted(queue, key=lambda x: x.service_time, reverse=True) # Sort by service time descending
    for process in queue:
        if process.start_time is None:
            process.start_time = current_time
        current_time += process.remaining_time
        process.remaining_time = 0
        process.completion_time = current_time
        executed_processes.append((process.pid, current_time))
    return executed_processes, current_time


# MLFQ Simulation
def mlfq_simulation(processes, queues):
    current_time = 0
    gantt_chart = []
    remaining_processes = processes.copy()

    for idx, queue in enumerate(queues):
        algorithm, quantum = queue
        if algorithm == "RR":
            scheduled, current_time = round_robin(remaining_processes, quantum, current_time)
        elif algorithm == "FCFS":
            scheduled, current_time = fcfs(remaining_processes, current_time)
        elif algorithm == "LCFS":
            scheduled, current_time = lcfs(remaining_processes, current_time)
        elif algorithm == "Priority":
            scheduled, current_time = priority_queue(remaining_processes, current_time)
        elif algorithm == "SJF":
            scheduled, current_time = shortest_job_first(remaining_processes, current_time)
        elif algorithm == "LJF":
            scheduled, current_time = longest_job_first(remaining_processes, current_time)
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")

        gantt_chart.extend(scheduled)
        remaining_processes = [p for p in remaining_processes if p.remaining_time > 0]

    return gantt_chart


# Input and Execution
if __name__ == "__main__":
    # Input number of queues
    num_queues = int(input("Enter the number of queues: "))

    # Input queue algorithms and quantum times
    queues = []
    for i in range(num_queues):
        print(f"Queue {i + 1}:")
        algorithm = input("Enter scheduling algorithm (RR, FCFS, LCFS, Priority, SJF, LJF): ")
        quantum = 0
        if algorithm == "RR":
            quantum = int(input("Enter quantum time: "))
        queues.append((algorithm, quantum))

    # Input processes
    num_processes = int(input("Enter the number of processes: "))
    processes = []
    for i in range(num_processes):
        pid = f"P{i + 1}"
        arrival_time = int(input(f"Enter arrival time of process {pid}: "))
        service_time = int(input(f"Enter service time of process {pid}: "))
        priority = None
        if any(queue[0] == "Priority" for queue in queues):
            priority = int(input(f"Enter priority of process {pid} (lower is higher priority): "))
        processes.append(Process(pid, arrival_time, service_time, priority))

    # Run simulation
    gantt_chart = mlfq_simulation(processes, queues)

    # Calculate response time, turnaround time, and waiting time
    print("\nProcess Details:")
    print("PID\tAT\tST\tRT\tTAT\tWT\tCT\tPriority")
    for process in processes:
        process.turnaround_time = process.completion_time - process.arrival_time
        process.response_time = process.start_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.service_time
        priority_display = process.priority if process.priority is not None else "N/A"
        print(
            f"{process.pid}\t{process.arrival_time}\t{process.service_time}\t"
            f"{process.response_time}\t{process.turnaround_time}\t{process.waiting_time}\t"
            f"{process.completion_time}\t{priority_display}"
        )

    # Print Gantt Chart
    print("\nGantt Chart:")
    for pid, time in gantt_chart:
        print(f"| {pid} ", end="")
    print("|")
