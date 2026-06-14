# MAC-Protocols-Simulation
Simulation and Performance Analysis of MAC Protocols using Python.

# Simulation and Performance Analysis of Medium Access Control (MAC) Protocols

## 📌 Project Overview
This project provides a comprehensive discrete-time simulation environment developed in Python to evaluate and analyze the performance of various **Medium Access Control (MAC)** protocols. The simulation compares random access methods and controlled access methods based on performance metrics such as throughput, collision rate, channel utilization, average delay, and fairness.

### Protocols Simulated:
1. **Random Access Protocols:** Pure ALOHA, Slotted ALOHA, CSMA/CD, CSMA/CA
2. **Controlled Access Protocols:** TDMA, FDMA, CDMA

---

## 🛠️ Simulation Design & Methodology
The simulation operates in discrete time steps. At each interval, network nodes generate data packets based on a specific transmission probability (Offered Load). 

### Key Implementation Details:
* **Pure ALOHA:** Nodes transmit packets immediately upon generation, leading to substantial collision vulnerabilities under high traffic.
* **Slotted ALOHA:** Restricts packet transmissions to designated global time-slot boundaries, significantly mitigating partial overlaps.
* **CSMA/CD:** Integrates carrier sensing to check if the channel is idle before attempting transmission and handles active collision detection.
* **CSMA/CA:** Implements a strict random exponential backoff mechanism to actively avoid collisions on a shared medium.
* **TDMA & FDMA:** Eliminates collision threats completely by allocating dedicated time slots (TDMA) or distinct frequency bands (FDMA) statically to each user.
* **CDMA:** Simulates orthogonal code-space dividing where performance linearly scales downwards as concurrent active users cross predefined resource thresholds.

---

## 📊 Evaluation Metrics
The framework automatically logs and calculates the following performance factors:
* **Throughput:** Total successful transmissions normalized over total simulation time steps.
* **Collision Rate:** The ratio of collided packet attempts to the total transmission attempts.
* **Channel Utilization:** The percentage of successful attempts relative to total channel placement tryouts.
* **Average Delay:** Cumulative delays faced by backoff regimes or waiting lines.
* **Fairness Index:** Jain's Fairness Index checking equality in successful delivery among nodes.

---

## 📈 Key Insights & Results

### 1. Effect of Offered Load
* At low traffic loads (e.g., 0.1), random access protocols perform decently. However, as the offered load approaches 0.5, **Pure ALOHA, Slotted ALOHA, and CSMA/CD suffer a catastrophic performance drop** due to high collision overheads.
* **CSMA/CA maintains the highest efficiency** among random access protocols because its random backoff rules prevent complete network collapse.
* Controlled access protocols (**TDMA & FDMA**) remain highly stable; their throughput scales positively with traffic since they utilize predefined collision-free paths.

### 2. Network Scalability (10 vs 50 vs 100 Nodes)
* Random access methods perform poorly as the number of nodes scales up to 100, driving the collision rate towards 1.0 (100% loss).
* **TDMA and FDMA provide absolute resilience** against expanding node sizes in terms of collision rate. However, TDMA introduces a linear surge in average packets delay since nodes must wait longer for their assigned time turns.

---

