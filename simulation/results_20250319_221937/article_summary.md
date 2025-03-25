# Simulation Results Summary

## Convergence Comparison Across Scenarios

### Average Convergence Rounds

| Agent Size | No Signal - History Based | No Signal - Reward Based | Mandatory Signal - History Based | Mandatory Signal - Reward Based | Optional Signal - History Based | Optional Signal - Reward Based |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 21.5 | 21.0 | 25.0 | 11.5 | 22.0 | 14.5 |
| 3 | 49.5 | 25.5 | 37.0 | 23.5 | 36.5 | 16.0 |
| 4 | 125.5 | 40.5 | 116.5 | 30.0 | 80.5 | 27.0 |
| 6 | 436.0 | 82.5 | 468.5 | 63.0 | 452.5 | 79.0 |
| 8 | 2090.0 | 172.5 | 2077.0 | 122.5 | 2645.5 | 138.5 |
| 10 | 9279.5 | 164.5 | 9137.0 | 160.5 | 17706.5 | 247.0 |
| 16 | 93010.0 | 438.0 | 91301.0 | 456.5 | 88163.0 | 531.5 |
| 20 | 96374.0 | 616.0 | 96331.5 | 650.0 | 100000.0 | 1630.0 |

### Convergence Rate

| Agent Size | No Signal - History Based | No Signal - Reward Based | Mandatory Signal - History Based | Mandatory Signal - Reward Based | Optional Signal - History Based | Optional Signal - Reward Based |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 3 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 4 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 6 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 8 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 10 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 16 | 0.20 | 1.00 | 0.15 | 1.00 | 0.25 | 1.00 |
| 20 | 0.05 | 1.00 | 0.05 | 1.00 | 0.00 | 1.00 |

### Blue Choice Convergence Rate

| Agent Size | No Signal - History Based | No Signal - Reward Based | Mandatory Signal - History Based | Mandatory Signal - Reward Based | Optional Signal - History Based | Optional Signal - Reward Based |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 0.40 | 0.30 | 0.50 | 0.75 | 0.45 | 0.60 |
| 3 | 0.35 | 0.55 | 0.45 | 0.30 | 0.60 | 0.60 |
| 4 | 0.45 | 0.35 | 0.55 | 0.60 | 0.55 | 0.60 |
| 6 | 0.40 | 0.60 | 0.45 | 0.55 | 0.45 | 0.40 |
| 8 | 0.40 | 0.60 | 0.40 | 0.70 | 0.40 | 0.40 |
| 10 | 0.55 | 0.50 | 0.45 | 0.30 | 0.50 | 0.40 |
| 16 | 0.25 | 0.65 | 1.00 | 0.30 | 0.60 | 0.70 |
| 20 | 0.00 | 0.45 | 1.00 | 0.55 | 0.00 | 0.50 |

## Signal Condition Comparison

### No Signal

Average performance across different strategies and agent sizes:

- Fastest convergence with 2 agents (average 21.2 rounds)
- Slowest convergence with 20 agents (average 48495.0 rounds)

#### History Based Strategy

Three-agent group performance:
- Average convergence rounds: 49.5
- Convergence rate: 1.00
- Blue choice rate: 0.35

#### Reward Based Strategy

Three-agent group performance:
- Average convergence rounds: 25.5
- Convergence rate: 1.00
- Blue choice rate: 0.55

### Mandatory Signal

Average performance across different strategies and agent sizes:

- Fastest convergence with 2 agents (average 18.2 rounds)
- Slowest convergence with 20 agents (average 48490.8 rounds)

#### History Based Strategy

Three-agent group performance:
- Average convergence rounds: 37.0
- Convergence rate: 1.00
- Blue choice rate: 0.45

#### Reward Based Strategy

Three-agent group performance:
- Average convergence rounds: 23.5
- Convergence rate: 1.00
- Blue choice rate: 0.30

### Optional Signal

Average performance across different strategies and agent sizes:

- Fastest convergence with 2 agents (average 18.2 rounds)
- Slowest convergence with 20 agents (average 50815.0 rounds)

#### History Based Strategy

Three-agent group performance:
- Average convergence rounds: 36.5
- Convergence rate: 1.00
- Blue choice rate: 0.60

#### Reward Based Strategy

Three-agent group performance:
- Average convergence rounds: 16.0
- Convergence rate: 1.00
- Blue choice rate: 0.60


## Strategy Comparison

### History Based

Average performance across different signal conditions and agent sizes:

- Highest convergence rate with 2 agents (average 1.00)
- Lowest convergence rate with 20 agents (average 0.03)

### Reward Based

Average performance across different signal conditions and agent sizes:

- Highest convergence rate with 2 agents (average 1.00)
- Lowest convergence rate with 2 agents (average 1.00)


## Key Observations

1. Overall, groups with 2 agents converge fastest, while groups with 20 agents converge slowest.

2. Among signal conditions, Mandatory Signal has the most positive impact on convergence speed, while Optional Signal is least conducive to rapid convergence.

3. In strategy comparison, Reward Based performs better overall with faster convergence.

