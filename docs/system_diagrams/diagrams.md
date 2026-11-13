# System Diagrams: Architecture, State Transitions, and Lifecycles

This document describes the architectural topology and state transitions of the MUET Point Bus Scheduling Discrete Event Simulation system.

## 1. System Architecture Diagram

```mermaid
graph TD
    subgraph Data Layer
        CFG[config/settings.py]
        CSV1[data/buses.csv]
        CSV2[data/routes.csv]
        CSV3[data/schedules.csv]
        CSV4[data/passenger_demand.csv]
    end

    subgraph Simulation Core [SimPy Engine]
        ENV[simpy.Environment]
        PG[Passenger Generator: NHPP Poisson Process]
        BO[Bus Operations Controller]
        STC[BusStop: STC Terminal FIFO Queue]
        MG[BusStop: Main Gate FIFO Queue]
    end

    subgraph Scheduling Algorithms
        A1[Algorithm 1: Fixed Schedule Baseline]
        A2[Algorithm 2: Demand-Based Headway]
        A3[Algorithm 3: Dynamic Queue Threshold]
        A4[Algorithm 4: Traffic-Aware Adaptive]
    end

    subgraph Evaluation & Visualization
        MET[SimulationMetrics Collector]
        EXP[Scenario Analysis: 7 Scenarios x 5 Replications]
        VIS[Matplotlib Visualizer: 9 Figures]
        REP[Statistical Summary & LaTeX Report]
    end

    CFG --> CSV1 & CSV2 & CSV3 & CSV4
    CSV1 & CSV2 & CSV3 & CSV4 --> BO
    ENV --> PG & BO
    PG -->|Generate Passengers| STC & MG
    A1 & A2 & A3 & A4 -->|Dispatch Triggers| BO
    BO -->|Boarding & Transit Loops| ENV
    BO --> MET
    MET --> EXP --> VIS & REP
```

## 2. Bus State Transition Diagram

A Point bus can only transition between distinct deterministic states, guaranteeing no capacity violations or overlapping trips.

```mermaid
stateDiagram-v2
    [*] --> IDLE : Initial Fleet Allocation
    
    IDLE --> BOARDING : Dispatch Triggered (Algorithm)
    note right of BOARDING : Passengers board up to capacity 55\nTime: 1.5 - 3.0s per passenger
    
    BOARDING --> IN_TRANSIT : All Passengers Boarded & Doors Close
    note right of IN_TRANSIT : Route base transit time + \nLognormal Traffic Delay
    
    IN_TRANSIT --> IDLE : Bus Completes Round Trip at Origin Terminal
    note left of IDLE : Ready for next trip assignment
    
    IDLE --> MAINTENANCE : Mechanical Breakdown / Service
    MAINTENANCE --> IDLE : Restored to Fleet
```

## 3. Passenger Flowchart

```mermaid
flowchart TD
    Start([Passenger Arrives at Campus]) --> Gen[NHPP Process assigns arrival time & route]
    Gen --> JoinQ[Join FIFO Terminal Queue at STC or Main Gate]
    JoinQ --> WaitBus{Bus Arrives for Target Route?}
    WaitBus -- No --> InQueue[Wait in Queue]
    InQueue --> WaitBus
    WaitBus -- Yes --> CheckSeat{Bus Has Available Seats?}
    CheckSeat -- Yes --> Board[Board Bus: Record Waiting Time W = t_board - t_arrive]
    Board --> Transit[Travel to Destination]
    Transit --> Alight([Alight at Destination Stop])
    CheckSeat -- No --> LeftBehind[Mark Passenger Left Behind]
    LeftBehind --> InQueue
```

## 4. Bus Lifecycle Flowchart

```mermaid
flowchart TD
    BStart([Bus Parked at Depot / Terminal]) --> BCheck{Dispatch Triggered by Scheduler?}
    BCheck -- No --> BIdle[Remain in IDLE state, accumulate idle time]
    BIdle --> BCheck
    BCheck -- Yes --> BReserve[Synchronously reserve bus]
    BReserve --> BBoard[Pop passengers up to 55 from FIFO queue]
    BBoard --> BTime[Boarding delay = sum of passenger boarding times]
    BTime --> BDepart[Depart Terminal: Status = IN_TRANSIT]
    BDepart --> BDelay[Sample Highway Traffic Delay ~ Lognormal]
    BDelay --> BTravel[Simulate Round-trip transit time]
    BTravel --> BReturn[Return to Origin Terminal]
    BReturn --> BReset[Empty onboard passengers, status = IDLE, increment trip count]
    BReset --> BCheck
```

