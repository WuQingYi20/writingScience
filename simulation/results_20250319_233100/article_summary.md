# Simulation Results Summary

## Convergence Comparison Across Scenarios

### Average Convergence Rounds

| Agent Size | No Signal - History Based | No Signal - Reward Based | Mandatory Signal - History Based | Mandatory Signal - Reward Based | Optional Signal - History Based | Optional Signal - Reward Based |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 19.0 | 16.5 | 12.5 | 10.5 | 12.5 | 12.5 |
| 3 | 64.5 | 33.0 | 21.0 | 16.0 | 15.5 | 21.0 |
| 4 | 91.5 | 37.0 | 22.5 | 18.5 | 32.5 | 21.0 |
| 6 | 358.0 | 102.5 | 71.0 | 36.5 | 74.5 | 58.0 |
| 8 | 2939.0 | 141.0 | 10175.0 | 69.0 | 165.0 | 64.0 |
| 10 | 19110.5 | 118.5 | 45062.5 | 88.5 | 682.5 | 177.5 |
| 16 | 95783.5 | 371.0 | 80020.0 | 286.5 | 11363.5 | 506.0 |
| 20 | 100000.0 | 814.0 | 100000.0 | 372.0 | 49385.5 | 746.5 |

### Convergence Rate

| Agent Size | No Signal - History Based | No Signal - Reward Based | Mandatory Signal - History Based | Mandatory Signal - Reward Based | Optional Signal - History Based | Optional Signal - Reward Based |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 3 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 4 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 6 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 8 | 1.00 | 1.00 | 0.90 | 1.00 | 1.00 | 1.00 |
| 10 | 0.95 | 1.00 | 0.55 | 1.00 | 1.00 | 1.00 |
| 16 | 0.05 | 1.00 | 0.20 | 1.00 | 1.00 | 1.00 |
| 20 | 0.00 | 1.00 | 0.00 | 1.00 | 0.70 | 1.00 |

### Blue Choice Convergence Rate

| Agent Size | No Signal - History Based | No Signal - Reward Based | Mandatory Signal - History Based | Mandatory Signal - Reward Based | Optional Signal - History Based | Optional Signal - Reward Based |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 0.50 | 0.35 | 0.55 | 0.25 | 0.45 | 0.45 |
| 3 | 0.40 | 0.45 | 0.50 | 0.45 | 0.55 | 0.55 |
| 4 | 0.45 | 0.50 | 0.55 | 0.50 | 0.55 | 0.35 |
| 6 | 0.60 | 0.40 | 0.60 | 0.50 | 0.55 | 0.30 |
| 8 | 0.45 | 0.55 | 0.56 | 0.55 | 0.40 | 0.65 |
| 10 | 0.47 | 0.45 | 0.09 | 0.45 | 0.45 | 0.25 |
| 16 | 0.00 | 0.70 | 0.50 | 0.20 | 0.60 | 0.55 |
| 20 | 0.00 | 0.45 | 0.00 | 0.55 | 0.64 | 0.40 |

## Signal Condition Comparison

### No Signal

Average performance across different strategies and agent sizes:

- Fastest convergence with 2 agents (average 17.8 rounds)
- Slowest convergence with 20 agents (average 50407.0 rounds)

#### History Based Strategy

Three-agent group performance:
- Average convergence rounds: 64.5
- Convergence rate: 1.00
- Blue choice rate: 0.40

#### Reward Based Strategy

Three-agent group performance:
- Average convergence rounds: 33.0
- Convergence rate: 1.00
- Blue choice rate: 0.45

### Mandatory Signal

Average performance across different strategies and agent sizes:

- Fastest convergence with 2 agents (average 11.5 rounds)
- Slowest convergence with 20 agents (average 50186.0 rounds)

#### History Based Strategy

Three-agent group performance:
- Average convergence rounds: 21.0
- Convergence rate: 1.00
- Blue choice rate: 0.50

#### Reward Based Strategy

Three-agent group performance:
- Average convergence rounds: 16.0
- Convergence rate: 1.00
- Blue choice rate: 0.45

### Optional Signal

Average performance across different strategies and agent sizes:

- Fastest convergence with 2 agents (average 12.5 rounds)
- Slowest convergence with 20 agents (average 25066.0 rounds)

#### History Based Strategy

Three-agent group performance:
- Average convergence rounds: 15.5
- Convergence rate: 1.00
- Blue choice rate: 0.55

#### Reward Based Strategy

Three-agent group performance:
- Average convergence rounds: 21.0
- Convergence rate: 1.00
- Blue choice rate: 0.55


## Strategy Comparison

### History Based

Average performance across different signal conditions and agent sizes:

- Highest convergence rate with 2 agents (average 1.00)
- Lowest convergence rate with 20 agents (average 0.23)

### Reward Based

Average performance across different signal conditions and agent sizes:

- Highest convergence rate with 2 agents (average 1.00)
- Lowest convergence rate with 2 agents (average 1.00)


## Key Observations

1. Overall, groups with 2 agents converge fastest, while groups with 20 agents converge slowest.

2. Among signal conditions, Optional Signal has the most positive impact on convergence speed, while Mandatory Signal is least conducive to rapid convergence.

3. In strategy comparison, Reward Based performs better overall with faster convergence.

