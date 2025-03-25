# Agent Simulation Environment

This project contains a multi-agent simulation environment for studying agent coordination behavior under different signal conditions and strategies.

## Environment Setup

### Using Conda

1. Make sure you have Conda installed ([Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/products/distribution))

2. Create conda environment using the provided `environment.yml` file:

```bash
conda env create -f environment.yml
```

3. Activate the environment:

```bash
conda activate agent_simulation
```

## Running Simulations

### Run All Scenarios

To run all scenarios and generate comparison charts:

```bash
python simulation/run_simulations.py
```

### Custom Run Options

You can customize the run using command line arguments:

```bash
# Specify different agent sizes
python simulation/run_simulations.py --agent-sizes 2 4 6 8 10

# Run a single scenario
python simulation/run_simulations.py --single-scenario --num-agents 3 --signal-condition MANDATORY_SIGNAL --strategy HISTORY_BASED

# Increase the number of runs per scenario
python simulation/run_simulations.py --runs-per-scenario 50
```

### Parameters

- `--agent-sizes`: List of agent sizes to simulate
- `--runs-per-scenario`: Number of runs per scenario
- `--max-rounds`: Maximum rounds per simulation
- `--single-scenario`: Run only a single scenario
- `--signal-condition`: Signal condition (NO_SIGNAL, MANDATORY_SIGNAL, OPTIONAL_SIGNAL)
- `--strategy`: Agent strategy (HISTORY_BASED, REWARD_BASED)
- `--num-agents`: Number of agents when running a single scenario

## Simulation Scenarios

The environment supports the following combination scenarios:

1. Signal Conditions:
   - No Signal: Agents cannot send signals
   - Mandatory Signal: Agents must send either red or blue signal
   - Optional Signal: Agents can choose whether to send a signal

2. Agent Strategies:
   - History Based: Agents learn based on historical frequencies
   - Reward Based: Agents update decision probabilities through reinforcement learning

## Output Results

After running, the system generates three charts:

1. `convergence_rounds.png`: Average rounds needed for convergence across scenarios
2. `convergence_rates.png`: Convergence rates for each scenario
3. `blue_convergence_rates.png`: Rate of convergence to blue choice in each scenario