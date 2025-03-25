# Simulation Results Summary

## Convergence Comparison Across Scenarios

### Average Convergence Rounds

| Agent Size | No Signal - History Based | No Signal - Reward Based | Mandatory Signal - History Based | Mandatory Signal - Reward Based | Optional Signal - History Based | Optional Signal - Reward Based |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 18.5 | 20.5 | 21.0 | 11.5 | 21.5 | 17.0 |
| 3 | 45.5 | 26.5 | 41.5 | 14.0 | 53.5 | 26.0 |
| 4 | 77.5 | 48.5 | 115.5 | 41.0 | 73.5 | 41.0 |
| 6 | 293.5 | 70.5 | 373.0 | 59.5 | 615.0 | 73.5 |
| 8 | 3054.0 | 137.5 | 2381.5 | 104.5 | 1744.5 | 152.5 |
| 10 | 7100.5 | 186.5 | 15484.0 | 128.5 | 10132.0 | 327.5 |
| 16 | 97108.5 | 434.0 | 96615.0 | 492.0 | 82809.5 | 1674.0 |
| 20 | 100000.0 | 770.0 | 100000.0 | 620.5 | 95729.5 | 2044.0 |

### Convergence Rate

| Agent Size | No Signal - History Based | No Signal - Reward Based | Mandatory Signal - History Based | Mandatory Signal - Reward Based | Optional Signal - History Based | Optional Signal - Reward Based |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 3 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 4 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 6 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 8 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 10 | 1.00 | 1.00 | 0.95 | 1.00 | 1.00 | 1.00 |
| 16 | 0.05 | 1.00 | 0.05 | 1.00 | 0.25 | 1.00 |
| 20 | 0.00 | 1.00 | 0.00 | 1.00 | 0.05 | 1.00 |

### Blue Choice Convergence Rate

| Agent Size | No Signal - History Based | No Signal - Reward Based | Mandatory Signal - History Based | Mandatory Signal - Reward Based | Optional Signal - History Based | Optional Signal - Reward Based |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 0.60 | 0.65 | 0.50 | 0.40 | 0.45 | 0.40 |
| 3 | 0.60 | 0.45 | 0.50 | 0.60 | 0.35 | 0.55 |
| 4 | 0.50 | 0.45 | 0.45 | 0.50 | 0.45 | 0.55 |
| 6 | 0.40 | 0.55 | 0.55 | 0.45 | 0.45 | 0.50 |
| 8 | 0.45 | 0.40 | 0.70 | 0.40 | 0.55 | 0.50 |
| 10 | 0.40 | 0.55 | 0.42 | 0.45 | 0.55 | 0.55 |
| 16 | 0.00 | 0.55 | 1.00 | 0.60 | 0.60 | 0.70 |
| 20 | 0.00 | 0.45 | 0.00 | 0.65 | 1.00 | 0.50 |

## Signal Condition Comparison

### No Signal

Average performance across different strategies and agent sizes:

- Fastest convergence with 2 agents (average 19.5 rounds)
- Slowest convergence with 20 agents (average 50385.0 rounds)

#### History Based Strategy

Three-agent group performance:
- Average convergence rounds: 45.5
- Convergence rate: 1.00
- Blue choice rate: 0.60

#### Reward Based Strategy

Three-agent group performance:
- Average convergence rounds: 26.5
- Convergence rate: 1.00
- Blue choice rate: 0.45

### Mandatory Signal

Average performance across different strategies and agent sizes:

- Fastest convergence with 2 agents (average 16.2 rounds)
- Slowest convergence with 20 agents (average 50310.2 rounds)

#### History Based Strategy

Three-agent group performance:
- Average convergence rounds: 41.5
- Convergence rate: 1.00
- Blue choice rate: 0.50

#### Reward Based Strategy

Three-agent group performance:
- Average convergence rounds: 14.0
- Convergence rate: 1.00
- Blue choice rate: 0.60

### Optional Signal

Average performance across different strategies and agent sizes:

- Fastest convergence with 2 agents (average 19.2 rounds)
- Slowest convergence with 20 agents (average 48886.8 rounds)

#### History Based Strategy

Three-agent group performance:
- Average convergence rounds: 53.5
- Convergence rate: 1.00
- Blue choice rate: 0.35

#### Reward Based Strategy

Three-agent group performance:
- Average convergence rounds: 26.0
- Convergence rate: 1.00
- Blue choice rate: 0.55


## Strategy Comparison

### History Based

Average performance across different signal conditions and agent sizes:

- Highest convergence rate with 2 agents (average 1.00)
- Lowest convergence rate with 20 agents (average 0.02)

### Reward Based

Average performance across different signal conditions and agent sizes:

- Highest convergence rate with 2 agents (average 1.00)
- Lowest convergence rate with 2 agents (average 1.00)


## Key Observations

1. Overall, groups with 2 agents converge fastest, while groups with 20 agents converge slowest.

2. Among signal conditions, Optional Signal has the most positive impact on convergence speed, while Mandatory Signal is least conducive to rapid convergence.

3. In strategy comparison, Reward Based performs better overall with faster convergence.

