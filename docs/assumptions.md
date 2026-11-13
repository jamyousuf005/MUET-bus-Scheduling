# Assumptions and Limitations Document

**Project:** MUET Point Bus Scheduling Optimization Using Discrete Event Simulation  
**Institution:** Department of Software Engineering, Mehran University of Engineering and Technology, Jamshoro  
**Course:** Simulation & Modelling (22SW II & III)  
**Instructor:** Engr. Umar Farooq  

---

## 1. Transparency on Data Sources
In strict accordance with academic integrity and engineering ethical standards, **no proprietary or confidential internal MUET records are presented as empirically verified data**. Historical logbooks and passenger tap counts from the MUET Transport Section are not released publicly.

Therefore, this research utilizes **empirically grounded synthetic data models** parameterized from:
1. Field observations of campus transit operations at MUET Jamshoro.
2. Standard transport geography metrics along the Jamshoro–Hyderabad corridor (M-9 motorways, Indus Highway, Qasimabad, Latifabad).
3. Published peer-reviewed academic literature on university shuttle operations and discrete event queuing models.

All operational parameters are fully decoupled and consolidated in `config/settings.py` and `data/*.csv`, enabling seamless replacement with empirical telemetry whenever made available by the administration.

---

## 2. Centralized Model Assumptions

### 2.1 Fleet Constraints
- **Fleet Size Conservation:** A fixed fleet of 25 buses is modeled. **Zero additional buses are purchased** in optimization algorithms, adhering strictly to the PBL problem statement.
- **Bus Seating Capacity:** 55 seats per single-deck university Point bus. In strict compliance with safety modeling, overcrowding beyond seating capacity is disallowed ($Occupancy \le 100\%$).
- **Trip Exclusivity:** A bus cannot accept overlapping trips or be present in two locations concurrently.
- **Terminal Distribution:** Buses start and terminate at designated campus hubs (STC Terminal and Main Gate).

### 2.2 Passenger Behavior & Queuing Dynamics
- **Arrival Process:** Modeled as a Non-Homogeneous Poisson Process (NHPP) with piecewise constant arrival rates $\lambda_i(t)$ reflecting sharp peak surges (08:00–09:00 AM and 14:00–15:30 PM) and off-peak mid-day lulls.
- **Queue Discipline:** Strict First-In-First-Out (FIFO) ordering per destination route.
- **Boarding Time:** Stochastic, sampled uniformly from $\mathcal{U}(1.5, 3.0)$ seconds per passenger.
- **Alighting Time:** Deterministic egress at destination estimated at $1.0$ second per passenger.
- **Left Behind Logic:** When a bus reaches its 55-seat capacity, all remaining passengers in the queue are marked as *left behind* and must wait for subsequent dispatches.

### 2.3 Traffic and Highway Delays
- **Corridor Travel Times:** Base round-trip travel times are parameterized from route distances (e.g., Qasimabad: 35 min one-way, Latifabad: 45 min one-way).
- **Stochastic Highway Delays:** Delays caused by the Jamshoro Toll Plaza, highway roadwork, and city bottlenecks are modeled using a Log-normal distribution:
  $$\Delta T_{\text{traffic}} \sim \text{Lognormal}(\mu, \sigma)$$
  ensuring strictly positive, right-skewed transit delay distributions.

---

## 3. Modeling Limitations

1. **Walking and Inter-terminal Transfers:** Passengers are assumed to arrive directly at their primary terminal (STC or Main Gate). Microscopic pedestrian walking dynamics between departments and terminals are not simulated.
2. **Standing Capacity:** In real-world peak operations, students sometimes stand in aisles. For safety evaluation and level-of-service optimization, this simulation enforces legal seating capacity (55 passengers).
3. **Driver Shift Regulations:** The model assumes driver availability matches bus availability without modeling individual driver labor union rest breaks.

