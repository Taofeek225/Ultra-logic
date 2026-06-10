import simpy
import random
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# --- PARAMETERS ---
LAMBDA = 0.9  # Arrival rate
MU = 1.0      # Service rate
SIM_TIME = 10000
NUM_REPLICATIONS = 5

def customer(env, name, server, wait_times):
    """Customer arrives, is served, and leaves."""
    arrival_time = env.now
    
    with server.request() as request:
        yield request
        # Time spent waiting in queue
        wait_times.append(env.now - arrival_time)
        
        # Service time (exponential distribution)
        service_duration = random.expovariate(MU)
        yield env.timeout(service_duration)

def setup(env, server, wait_times):
    """Generates customers according to Poisson process."""
    i = 0
    while True:
        yield env.timeout(random.expovariate(LAMBDA))
        i += 1
        env.process(customer(env, f'Customer {i}', server, wait_times))

# --- RUNNING REPLICATIONS ---
replication_results = []

print(f"{'Rep':<5} | {'Avg Wait Time':<15} | {'Server Utilization':<18}")
print("-" * 45)

for r in range(NUM_REPLICATIONS):
    random.seed(r + 42) # Ensure reproducibility
    env = simpy.Environment()
    server = simpy.Resource(env, capacity=1)
    wait_times = []
    
    env.process(setup(env, server, wait_times))
    env.run(until=SIM_TIME)
    
    avg_wait = np.mean(wait_times)
    utilization = (len(wait_times) * (1/MU)) / SIM_TIME
    
    replication_results.append(avg_wait)
    print(f"{r+1:<5} | {avg_wait:<15.4f} | {utilization:<18.4f}")

# --- STATISTICS & ANALYSIS ---
mean_wait = np.mean(replication_results)
std_err = stats.sem(replication_results)
ci_95 = stats.t.interval(0.95, len(replication_results)-1, loc=mean_wait, scale=std_err)

# Theoretical Values
theoretical_wait = LAMBDA / (MU * (MU - LAMBDA))
theoretical_util = LAMBDA / MU

print("\n--- FINAL ANALYSIS ---")
print(f"Experimental Mean Wait Time: {mean_wait:.4f}")
print(f"Theoretical Mean Wait Time:  {theoretical_wait:.4f}")
print(f"95% Confidence Interval:     ({ci_95[0]:.4f}, {ci_95[1]:.4f})")
print(f"Theoretical Utilization:     {theoretical_util:.4f}")

# --- PARAMETER for Exercise 2 ---
LAMBDA_EX2 = 1.8  # Busy arrival rate for Exercise 2
MU = 1.0          
SIM_TIME = 10000  
random.seed(42)   

def run_multiserver(c):
    """Simulates an M/M/c queue and returns the average waiting time (W_q)."""
    # Check if the system is stable (capacity > arrival rate)
    if LAMBDA_EX2 >= c * MU:
        # For unstable systems
        print(f"Server Count c={c} is unstable. Wait will grow indefinitely.")
        return 500  # Use a capped value for plotting, as 'inf' won't graph
    
    env = simpy.Environment()
    server = simpy.Resource(env, capacity=c)
    wait_times = []

    def customer(env):
        arrival_time = env.now
        with server.request() as request:
            yield request
            # Record time spent in queue
            wait_times.append(env.now - arrival_time)
            # Service duration is exponentially distributed
            yield env.timeout(random.expovariate(MU))

    def setup(env):
        while True:
            # Arrivals are exponentially distributed
            yield env.timeout(random.expovariate(LAMBDA_EX2))
            env.process(customer(env))

    env.process(setup(env))
    env.run(until=SIM_TIME)
    
    # Return the average waiting time (W_q)
    return np.mean(wait_times)

# --- EXECUTION: Test 1, 2, and 3 servers ---
servers = [1, 2, 3]
total_costs = []

print(f"{'Servers (c)':<12} | {'Total Cost':<12}")
print("-" * 30)

for c in servers:
    w_q = run_multiserver(c)
    # --- COST FORMULA: 50c + 10 * lambda * Wq ---
    cost = (50 * c) + (10 * LAMBDA_EX2 * w_q)
    total_costs.append(cost)
    
    # Cap the cost for unstable c=1 so the graph is readable
    if c == 1:
        print(f"{c:<12} | {'UNSTABLE':<12}")
    else:
        print(f"{c:<12} | {cost:<12.2f}")

# --- PLOTTING: Cost Optimization ---
plt.figure(figsize=(10, 6))

# Plot a bar chart
bars = plt.bar(servers, total_costs, color=['#e74c3c', '#27ae60', '#2980b9'])

# Add labels to the axes
plt.xlabel('Number of Servers (c)', fontsize=12)
plt.ylabel('Total Operating Cost ($)', fontsize=12)
plt.title('Cost Optimization: Servers vs. Total Cost (Exercise 2)', fontsize=14)

# Set the x-axis ticks to show 1, 2, 3 clearly
plt.xticks(servers)

# Label the unstable configuration
bars[0].set_edgecolor('black')
plt.text(1, bars[0].get_height() + 20, 'Unstable', ha='center', fontweight='bold', color='red')

# Annotate each bar with the cost value (except the capped unstable one)
for i, cost in enumerate(total_costs):
    if servers[i] != 1:
        plt.text(servers[i], cost + 5, f'${cost:.2f}', ha='center', va='bottom', fontsize=10)

plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Save the plot for your report
plt.savefig('optimization_plot.png', dpi=300)
print("\nPlot saved as 'optimization_plot.png'. Ready for report inclusion.")
plt.show()