# MUET Point Scheduling Optimization: Comparative Performance Summary

Generated from Monte Carlo replications across 7 operational scenarios.

| Scenario | Algorithm | Mean Wait Time (min) | Wait Time Improvement (%) | Passengers Left Behind | Left Behind Reduction (%) | Fleet Utilization (%) | Trips Completed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1_Normal_Demand | demand_based | 37.61 | 43.97 | 3457.6 | 19.86 | 64.64 | 125.4 |
| 1_Normal_Demand | dynamic_queue | 21.92 | 67.34 | 2027.4 | 53.01 | 70.94 | 140.0 |
| 1_Normal_Demand | fixed_schedule | 67.13 | 0.0 | 4314.6 | 0.0 | 42.36 | 76.0 |
| 1_Normal_Demand | traffic_aware | 26.25 | 60.89 | 2520.4 | 41.58 | 73.74 | 145.0 |
| 2_High_Morning_Demand | demand_based | 66.59 | 38.5 | 5313.8 | -1.92 | 65.23 | 125.8 |
| 2_High_Morning_Demand | dynamic_queue | 29.75 | 72.53 | 3051.6 | 41.47 | 75.73 | 149.0 |
| 2_High_Morning_Demand | fixed_schedule | 108.29 | 0.0 | 5213.8 | 0.0 | 42.41 | 76.0 |
| 2_High_Morning_Demand | traffic_aware | 36.24 | 66.54 | 3489.0 | 33.08 | 77.49 | 150.8 |
| 3_High_Afternoon_Demand | demand_based | 42.5 | 38.39 | 5597.0 | 0.05 | 64.4 | 124.8 |
| 3_High_Afternoon_Demand | dynamic_queue | 25.15 | 63.55 | 3861.8 | 31.03 | 70.19 | 137.8 |
| 3_High_Afternoon_Demand | fixed_schedule | 68.98 | 0.0 | 5599.6 | 0.0 | 42.39 | 76.0 |
| 3_High_Afternoon_Demand | traffic_aware | 28.24 | 59.06 | 4072.2 | 27.28 | 73.05 | 143.0 |
| 4_Unexpected_Traffic_Congestion | demand_based | 51.56 | 23.18 | 4249.4 | 1.51 | 70.89 | 109.8 |
| 4_Unexpected_Traffic_Congestion | dynamic_queue | 27.76 | 58.65 | 2728.0 | 36.77 | 77.23 | 118.0 |
| 4_Unexpected_Traffic_Congestion | fixed_schedule | 67.13 | 0.0 | 4314.6 | 0.0 | 50.94 | 73.2 |
| 4_Unexpected_Traffic_Congestion | traffic_aware | 31.77 | 52.67 | 2893.4 | 32.94 | 79.28 | 121.8 |
| 5_Sudden_Surge_Demand | demand_based | 112.44 | 19.09 | 10286.0 | -14.5 | 68.69 | 117.4 |
| 5_Sudden_Surge_Demand | dynamic_queue | 55.6 | 59.99 | 7607.6 | 15.31 | 83.64 | 140.6 |
| 5_Sudden_Surge_Demand | fixed_schedule | 138.97 | 0.0 | 8983.2 | 0.0 | 47.6 | 75.0 |
| 5_Sudden_Surge_Demand | traffic_aware | 59.14 | 57.45 | 7152.0 | 20.38 | 84.04 | 142.2 |
| 6_Uneven_Terminal_Demand | demand_based | 51.71 | 14.43 | 4454.0 | -15.81 | 64.84 | 126.2 |
| 6_Uneven_Terminal_Demand | dynamic_queue | 28.42 | 52.97 | 3030.2 | 21.21 | 66.55 | 131.2 |
| 6_Uneven_Terminal_Demand | fixed_schedule | 60.43 | 0.0 | 3845.8 | 0.0 | 42.3 | 76.0 |
| 6_Uneven_Terminal_Demand | traffic_aware | 31.58 | 47.74 | 2807.6 | 27.0 | 71.51 | 141.0 |
| 7_Reduced_Fleet_Maintenance | demand_based | 64.8 | 3.46 | 4594.6 | -6.49 | 74.83 | 103.2 |
| 7_Reduced_Fleet_Maintenance | dynamic_queue | 32.25 | 51.96 | 2870.6 | 33.47 | 81.51 | 113.4 |
| 7_Reduced_Fleet_Maintenance | fixed_schedule | 67.13 | 0.0 | 4314.6 | 0.0 | 58.83 | 76.0 |
| 7_Reduced_Fleet_Maintenance | traffic_aware | 37.0 | 44.89 | 3270.8 | 24.19 | 82.51 | 114.4 |


### Metric Interpretations:
- **Wait Time Improvement (%):** Percentage reduction in average student wait time relative to Baseline.
- **Left Behind Reduction (%):** Percentage reduction in students stranded when a bus fills up.
- **Fleet Utilization (%):** Proportion of available fleet capacity actively engaged in revenue passenger service.
