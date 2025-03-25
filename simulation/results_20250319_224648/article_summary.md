# Simulation Results Summary

## Convergence Comparison Across Scenarios

### Average Convergence Rounds

| Agent Size | No Signal - History Based | No Signal - Reward Based | Mandatory Signal - History Based | Mandatory Signal - Reward Based | Optional Signal - History Based | Optional Signal - Reward Based |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 19.0 | 21.0 | 12.0 | 13.5 | 12.0 | 10.5 |
| 3 | 28.5 | 31.5 | 22.5 | 18.0 | 26.0 | 23.5 |
| 4 | 103.5 | 52.0 | 31.0 | 28.5 | 35.5 | 31.5 |
| 6 | 435.5 | 72.0 | 181.0 | 58.5 | 59.5 | 30.5 |
| 8 | 2708.5 | 110.0 | 5131.0 | 110.5 | 137.5 | 145.0 |
| 10 | 9819.0 | 191.5 | 40262.5 | 188.5 | 479.0 | 194.5 |
| 16 | 92895.0 | 445.0 | 90128.0 | 617.5 | 13126.0 | 823.0 |
| 20 | 98844.5 | 647.5 | 95051.5 | 747.0 | 26800.5 | 1017.5 |

### Convergence Rate

| Agent Size | No Signal - History Based | No Signal - Reward Based | Mandatory Signal - History Based | Mandatory Signal - Reward Based | Optional Signal - History Based | Optional Signal - Reward Based |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 3 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 4 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 6 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 8 | 1.00 | 1.00 | 0.95 | 1.00 | 1.00 | 1.00 |
| 10 | 1.00 | 1.00 | 0.60 | 1.00 | 1.00 | 1.00 |
| 16 | 0.15 | 1.00 | 0.10 | 1.00 | 0.95 | 1.00 |
| 20 | 0.05 | 1.00 | 0.05 | 1.00 | 0.95 | 1.00 |

### Blue Choice Convergence Rate

| Agent Size | No Signal - History Based | No Signal - Reward Based | Mandatory Signal - History Based | Mandatory Signal - Reward Based | Optional Signal - History Based | Optional Signal - Reward Based |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 0.30 | 0.50 | 0.45 | 0.50 | 0.45 | 0.70 |
| 3 | 0.75 | 0.50 | 0.40 | 0.40 | 0.30 | 0.40 |
| 4 | 0.55 | 0.55 | 0.55 | 0.50 | 0.65 | 0.55 |
| 6 | 0.45 | 0.30 | 0.60 | 0.45 | 0.60 | 0.55 |
| 8 | 0.50 | 0.55 | 0.42 | 0.50 | 0.70 | 0.35 |
| 10 | 0.45 | 0.60 | 0.42 | 0.50 | 0.45 | 0.70 |
| 16 | 0.33 | 0.50 | 0.50 | 0.50 | 0.42 | 0.55 |
| 20 | 1.00 | 0.35 | 1.00 | 0.60 | 0.53 | 0.45 |

## Signal Condition Comparison

### No Signal

Average performance across different strategies and agent sizes:

- Fastest convergence with 2 agents (average 20.0 rounds)
- Slowest convergence with 20 agents (average 49746.0 rounds)

#### History Based Strategy

Three-agent group performance:
- Average convergence rounds: 28.5
- Convergence rate: 1.00
- Blue choice rate: 0.75

#### Reward Based Strategy

Three-agent group performance:
- Average convergence rounds: 31.5
- Convergence rate: 1.00
- Blue choice rate: 0.50

### Mandatory Signal

Average performance across different strategies and agent sizes:

- Fastest convergence with 2 agents (average 12.8 rounds)
- Slowest convergence with 20 agents (average 47899.2 rounds)

#### History Based Strategy

Three-agent group performance:
- Average convergence rounds: 22.5
- Convergence rate: 1.00
- Blue choice rate: 0.40

#### Reward Based Strategy

Three-agent group performance:
- Average convergence rounds: 18.0
- Convergence rate: 1.00
- Blue choice rate: 0.40

### Optional Signal

Average performance across different strategies and agent sizes:

- Fastest convergence with 2 agents (average 11.2 rounds)
- Slowest convergence with 20 agents (average 13909.0 rounds)

#### History Based Strategy

Three-agent group performance:
- Average convergence rounds: 26.0
- Convergence rate: 1.00
- Blue choice rate: 0.30

#### Reward Based Strategy

Three-agent group performance:
- Average convergence rounds: 23.5
- Convergence rate: 1.00
- Blue choice rate: 0.40


## Strategy Comparison

### History Based

Average performance across different signal conditions and agent sizes:

- Highest convergence rate with 2 agents (average 1.00)
- Lowest convergence rate with 20 agents (average 0.35)

### Reward Based

Average performance across different signal conditions and agent sizes:

- Highest convergence rate with 2 agents (average 1.00)
- Lowest convergence rate with 2 agents (average 1.00)


## Key Observations

1. Overall, groups with 2 agents converge fastest, while groups with 20 agents converge slowest.

2. Among signal conditions, Optional Signal has the most positive impact on convergence speed, while Mandatory Signal is least conducive to rapid convergence.

3. In strategy comparison, Reward Based performs better overall with faster convergence.

