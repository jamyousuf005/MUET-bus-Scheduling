# Mathematical Model & Queuing Formulation

## 1. Introduction & Theoretical Framing
Transit operations at Mehran University of Engineering and Technology (MUET), Jamshoro, represent a multi-server, bulk-service queuing system operating under time-dependent arrival distributions. Traditional steady-state queuing formulations (e.g., standard Kendall notation $M/M/c$) assume homogeneous Poisson arrivals and independent exponential service times with single-passenger service. However, campus Point buses transport large batches ($C=55$) simultaneously across correlated highway corridors subject to non-stationary demand surges.

To bridge theoretical rigor and empirical realism, this model establishes analytical formulations for:
1. Non-Homogeneous Poisson Arrival Processes ($M(t)$)
2. Batch-Service Capacity Queues ($M(t)/G^{[C]}/c$)
3. Little's Law Generalization for Transit Systems
4. Fleet Conservation and Turnaround Equations

---

## 2. Arrival Rate Formulation: Non-Homogeneous Poisson Process (NHPP)
Passenger arrivals at terminal $i \in \{\text{STC}, \text{Main Gate}\}$ are governed by an inhomogeneous Poisson counting process $\{N_i(t), t \ge 0\}$ with continuous-time deterministic intensity function $\lambda_i(t)$:

$$P(N_i(t + \Delta t) - N_i(t) = k) = \frac{[\Lambda_i(t, t+\Delta t)]^k e^{-\Lambda_i(t, t+\Delta t)}}{k!}$$

where cumulative intensity $\Lambda_i(t_1, t_2)$ is defined as:
$$\Lambda_i(t_1, t_2) = \int_{t_1}^{t_2} \lambda_i(\tau) d\tau$$

In our simulation framework, $\lambda_i(t)$ is discretized across 5 operational time windows:
$$\lambda_i(t) = \sum_{w=1}^{5} \lambda_{i, w} \cdot \mathbf{1}_{\{t \in \mathcal{W}_w\}}$$

---

## 3. Batch Service Mechanism & Boarding Dynamics
Each bus $b \in \mathcal{B}$ has a maximum legal seating capacity of $C = 55$. 

When a bus initiates boarding at terminal $i$ for route $r$ at time $t_d$, the number of boarded passengers $P_{\text{boarded}}$ is bounded by:
$$P_{\text{boarded}} = \min(Q_i(r, t_d), C)$$

where $Q_i(r, t_d)$ is the instantaneous queue length for route $r$ at time $t_d$.

The boarding duration $T_{\text{board}}$ is a sum of independent uniform random variables representing individual passenger step-in delays:
$$T_{\text{board}} = \sum_{k=1}^{P_{\text{boarded}}} \tau_k, \quad \tau_k \sim \mathcal{U}(1.5, 3.0) \text{ seconds}$$

---

## 4. Corridor Transit Time and Traffic Delay Modeling
The round-trip transit duration $T_{\text{trip}}(r)$ along route $r$ is modeled as:
$$T_{\text{trip}}(r) = 2 \cdot T_{\text{base}}(r) + \Delta T_{\text{traffic}} + T_{\text{alight}}$$

where:
- $T_{\text{base}}(r)$: Deterministic free-flow travel time between terminal and destination.
- $\Delta T_{\text{traffic}}$: Non-negative stochastic congestion delay sampled from a Log-normal distribution:
  $$\Delta T_{\text{traffic}} \sim \text{Lognormal}(\mu_{\text{traffic}}, \sigma_{\text{traffic}})$$
  $$\mathbb{E}[\Delta T] = \exp\left(\mu + \frac{\sigma^2}{2}\right), \quad \operatorname{Var}(\Delta T) = \left(e^{\sigma^2} - 1\right) e^{2\mu + \sigma^2}$$
- $T_{\text{alight}} = P_{\text{boarded}} \times 1.0 \text{ sec}$: Egress delay at destination stops.

---

## 5. System Conservation & Little's Law
At any arbitrary simulation timestamp $t$, the total passenger volume generated $N_{\text{total}}(t)$ satisfies the conservation identity:
$$N_{\text{total}}(t) = Q_{\text{STC}}(t) + Q_{\text{MG}}(t) + P_{\text{transit}}(t) + N_{\text{completed}}(t)$$

By Little's Law, under stationary intervals, the long-term expected queue length $L_q$ and expected waiting time $W_q$ relate as:
$$L_q = \lambda \cdot W_q$$

In discrete event simulation, the empirical average waiting time is calculated as:
$$W_q = \frac{1}{|\mathcal{P}_{\text{boarded}}|} \sum_{p \in \mathcal{P}_{\text{boarded}}} \left( t_{\text{board}, p} - t_{\text{arrive}, p} \right)$$

---

## 6. Fleet Conservation & Utilization Formulation
The total fleet size $B = 25$ is strictly conserved at all times:
$$\sum_{b=1}^{B} \left( \mathbf{1}_{\{S_b(t) = \text{IDLE}\}} + \mathbf{1}_{\{S_b(t) = \text{BOARDING}\}} + \mathbf{1}_{\{S_b(t) = \text{IN\_TRANSIT}\}} \right) = B, \quad \forall t$$

Fleet utilization $\rho_{\text{fleet}}$ over simulation horizon $T_{\text{sim}}$ is computed as:
$$\rho_{\text{fleet}} = \frac{\sum_{b=1}^{B} T_{\text{active}, b}}{B \cdot T_{\text{sim}}} \times 100\%$$
where $T_{\text{active}, b}$ denotes time spent in BOARDING and IN_TRANSIT states.

