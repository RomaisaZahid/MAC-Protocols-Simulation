import random
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Core Metrics Engine
# -----------------------------
def calculate_metrics(success, collisions, attempts, delays, user_success, SIM_TIME, NUM_USERS):
    throughput = success / SIM_TIME
    collision_rate = collisions / attempts if attempts > 0 else 0
    utilization = success / attempts if attempts > 0 else 0
    avg_delay = np.mean(delays) if delays else 1.0
    fairness = (sum(user_success) ** 2) / (NUM_USERS * sum([x**2 for x in user_success]) + 1e-9)
    return throughput, collision_rate, utilization, avg_delay, fairness

# -----------------------------
# Protocol Simulation Logic
# -----------------------------
def run_simulation(protocol_name, NUM_USERS, SIM_TIME, PACKET_GEN_PROB):
    success = collisions = attempts = 0
    user_success = [0]*NUM_USERS
    delays = []
    
    if protocol_name == "Pure ALOHA":
        busy_until = -1
        for t in range(SIM_TIME):
            transmitting = [i for i in range(NUM_USERS) if random.random() < PACKET_GEN_PROB]
            attempts += len(transmitting)
            for user in transmitting:
                if len(transmitting) > 1 or t <= busy_until:
                    collisions += 1
                    delays.append(random.randint(5, 15))
                else:
                    success += 1
                    user_success[user] += 1
                    delays.append(1)
                    busy_until = t + 1

    elif protocol_name == "Slotted ALOHA":
        for t in range(SIM_TIME):
            transmitting = [i for i in range(NUM_USERS) if random.random() < PACKET_GEN_PROB]
            attempts += len(transmitting)
            if len(transmitting) == 1:
                success += 1
                user_success[transmitting[0]] += 1
                delays.append(1)
            elif len(transmitting) > 1:
                collisions += len(transmitting)
                for _ in transmitting: delays.append(random.randint(2, 8))

    elif protocol_name == "CSMA/CD":
        channel_busy = False
        for t in range(SIM_TIME):
            if not channel_busy:
                transmitting = [i for i in range(NUM_USERS) if random.random() < PACKET_GEN_PROB]
                attempts += len(transmitting)
                if len(transmitting) == 1:
                    success += 1
                    user_success[transmitting[0]] += 1
                    delays.append(1)
                    channel_busy = True
                elif len(transmitting) > 1:
                    collisions += len(transmitting)
                    for _ in transmitting: delays.append(random.randint(2, 5))
            else: channel_busy = False

    elif protocol_name == "CSMA/CA":
        backoff = [0]*NUM_USERS
        for t in range(SIM_TIME):
            transmitting = []
            for i in range(NUM_USERS):
                if backoff[i] > 0:
                    backoff[i] -= 1
                    continue
                if random.random() < PACKET_GEN_PROB: transmitting.append(i)
            attempts += len(transmitting)
            if len(transmitting) == 1:
                success += 1
                user_success[transmitting[0]] += 1
                delays.append(1)
            elif len(transmitting) > 1:
                collisions += len(transmitting)
                for i in transmitting:
                    backoff[i] = random.randint(1, 10)
                    delays.append(backoff[i])

    elif protocol_name == "TDMA":
        for t in range(SIM_TIME):
            user = t % NUM_USERS
            if random.random() < PACKET_GEN_PROB:
                attempts += 1
                success += 1
                user_success[user] += 1
                delays.append(NUM_USERS / 2)

    elif protocol_name == "FDMA":
        for t in range(SIM_TIME):
            for i in range(NUM_USERS):
                if random.random() < (PACKET_GEN_PROB / NUM_USERS):
                    attempts += 1
                    success += 1
                    user_success[i] += 1
                    delays.append(1)

    elif protocol_name == "CDMA":
        for t in range(SIM_TIME):
            transmitting = [i for i in range(NUM_USERS) if random.random() < PACKET_GEN_PROB]
            attempts += len(transmitting)
            if len(transmitting) <= 4:
                success += len(transmitting)
                for i in transmitting:
                    user_success[i] += 1
                    delays.append(1)
            else:
                collisions += len(transmitting)
                for _ in transmitting: delays.append(2)
        return calculate_metrics(success/3, collisions, attempts, delays, user_success, SIM_TIME, NUM_USERS)

    return calculate_metrics(success, collisions, attempts, delays, user_success, SIM_TIME, NUM_USERS)

# ---------------------------------------------------------
# SECTION 1: Standard Simulation (Original Table)
# ---------------------------------------------------------
NUM_USERS_STD = 10
SIM_TIME_STD = 1000
PROB_STD = 0.15

print("\n" + "="*80)
print("SECTION 1: STANDARD PROTOCOL PERFORMANCE (Baseline: 10 Users, 0.15 Load)")
print("="*80)
header = f"{'Protocol':<15} | {'Thrput':<7} | {'Colis%':<8} | {'Util%':<7} | {'Delay':<7} | {'Fairness':<7}"
print(header)
print("-" * len(header))

protocols_list = ["Pure ALOHA", "Slotted ALOHA", "CSMA/CD", "CSMA/CA", "TDMA", "FDMA", "CDMA"]
final_utilization = []

for name in protocols_list:
    tr, cr, ut, dl, fr = run_simulation(name, NUM_USERS_STD, SIM_TIME_STD, PROB_STD)
    final_utilization.append(ut)
    print(f"{name:<15} | {tr:<7.3f} | {cr:<8.3f} | {ut:<7.3f} | {dl:<7.3f} | {fr:<7.3f}")

# ---------------------------------------------------------
# SECTION 2: Experimental Scenarios (Console Output)
# ---------------------------------------------------------
print("\n\n" + "="*80)
print("SECTION 2: EXPERIMENTAL SCENARIOS")
print("="*80)
nodes_list = [10, 50, 100]
load_list = [0.1, 0.5]

for nodes in nodes_list:
    for load in load_list:
        print(f"\nScenario: [Nodes: {nodes}] | [Offered Load: {load}]")
        sub_header = f"{'Protocol':<15} | {'Thrput':<7} | {'Colis%':<8} | {'Util%':<7} | {'Delay':<7}"
        print(sub_header)
        print("-" * len(sub_header))
        for proto in protocols_list:
            tr, cr, ut, dl, fr = run_simulation(proto, nodes, 500, load)
            print(f"{proto:<15} | {tr:<7.3f} | {cr:<8.3f} | {ut:<7.3f} | {dl:<7.3f}")

# ---------------------------------------------------------
# SECTION 3: Graph Generation (Matplotlib)
# ---------------------------------------------------------
print("\nGenerating Plots... Please check the Plots tab.")

offered_loads = np.linspace(0.01, 0.6, 10)
nodes_variation = [10, 30, 50, 70, 100]
random_protocols = ["Pure ALOHA", "Slotted ALOHA", "CSMA/CD", "CSMA/CA"]

# Plot 1 & 2: Throughput/Collision vs Offered Load
plt.figure(figsize=(12, 5))

# Graph 1: Throughput vs Offered Load
plt.subplot(1, 2, 1)
for proto in random_protocols:
    th_vals = [run_simulation(proto, 10, 500, l)[0] for l in offered_loads]
    plt.plot(offered_loads, th_vals, marker='o', label=proto)
plt.title("Throughput vs Offered Load")
plt.xlabel("Offered Load (Probability)")
plt.ylabel("Throughput")
plt.legend()
plt.grid(True)

# Graph 2: Collision Rate vs Offered Load
plt.subplot(1, 2, 2)
for proto in random_protocols:
    coll_vals = [run_simulation(proto, 10, 500, l)[1] for l in offered_loads]
    plt.plot(offered_loads, coll_vals, marker='s', label=proto)
plt.title("Collision Rate vs Offered Load")
plt.xlabel("Offered Load (Probability)")
plt.ylabel("Collision Rate")
plt.legend()
plt.grid(True)
plt.tight_layout()

# Graph 3: Throughput vs Number of Nodes
plt.figure(figsize=(8, 5))
for proto in protocols_list:
    th_nodes = [run_simulation(proto, n, 500, 0.2)[0] for n in nodes_variation]
    plt.plot(nodes_variation, th_nodes, marker='D', label=proto)
plt.title("Throughput vs Number of Nodes (Load=0.2)")
plt.xlabel("Number of Nodes")
plt.ylabel("Throughput")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()

# Graph 4: Channel Utilization Comparison (Bar Chart)
plt.figure(figsize=(10, 5))
plt.bar(protocols_list, final_utilization, color=['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink'])
plt.title("Channel Utilization Comparison (10 Users, 0.15 Load)")
plt.ylabel("Utilization %")
plt.ylim(0, 1.1)
for i, v in enumerate(final_utilization):
    plt.text(i, v + 0.02, f"{v:.2f}", ha='center')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()