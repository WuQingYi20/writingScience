import argparse
from environment import (
    SignalCondition, 
    Strategy, 
    Environment, 
    run_all_scenarios, 
    plot_results
)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Run agent simulations with different communication conditions')
    
    parser.add_argument(
        '--agent-sizes', 
        type=int, 
        nargs='+', 
        default=[2, 3, 4, 6, 8, 10, 16, 20],
        help='List of agent population sizes to simulate'
    )
    
    parser.add_argument(
        '--runs-per-scenario', 
        type=int, 
        default=20,
        help='Number of simulations to run for each scenario'
    )
    
    parser.add_argument(
        '--max-rounds', 
        type=int, 
        default=100000,
        help='Maximum number of rounds to run for each simulation'
    )
    
    parser.add_argument(
        '--single-scenario', 
        action='store_true',
        help='Run only a single scenario instead of all'
    )
    
    parser.add_argument(
        '--signal-condition', 
        type=str, 
        choices=['NO_SIGNAL', 'MANDATORY_SIGNAL', 'OPTIONAL_SIGNAL'],
        default='MANDATORY_SIGNAL',
        help='Signal condition to use for single scenario run'
    )
    
    parser.add_argument(
        '--strategy', 
        type=str, 
        choices=['HISTORY_BASED', 'REWARD_BASED'],
        default='HISTORY_BASED',
        help='Agent strategy to use for single scenario run'
    )
    
    parser.add_argument(
        '--num-agents', 
        type=int, 
        default=4,
        help='Number of agents for single scenario run'
    )
    
    return parser.parse_args()

def run_single_scenario(args):
    """Run a single scenario and print detailed results"""
    signal_condition = getattr(SignalCondition, args.signal_condition)
    strategy = getattr(Strategy, args.strategy)
    
    print(f"Running simulation with:")
    print(f"  Signal Condition: {signal_condition.value}")
    print(f"  Strategy: {strategy.value}")
    print(f"  Number of Agents: {args.num_agents}")
    
    env = Environment(args.num_agents, signal_condition, strategy)
    rounds, converged, choice = env.run_simulation(args.max_rounds)
    
    print("\nResults:")
    print(f"  Converged: {converged}")
    if converged:
        print(f"  Rounds to Convergence: {rounds}")
        print(f"  Convergence Choice: {choice}")
    else:
        print(f"  Did not converge after {rounds} rounds")
    
    print("\nAgent States:")
    for agent in env.agents:
        if strategy == Strategy.HISTORY_BASED:
            print(f"  {agent.name}: Blue Ratio = {agent.get_blue_ratio():.2f}")
        else:
            print(f"  {agent.name}: p_choice_blue = {agent.p_choice_blue:.2f}, " +
                  f"p_signal_blue = {agent.p_signal_blue:.2f}, " +
                  f"p_follow_own = {agent.p_follow_own:.2f}")
    
    return env

def main():
    args = parse_arguments()
    
    if args.single_scenario:
        run_single_scenario(args)
    else:
        print("Running all scenarios...")
        results = run_all_scenarios(
            agent_sizes=args.agent_sizes,
            runs_per_scenario=args.runs_per_scenario,
            max_rounds=args.max_rounds
        )
        
        print("\nPlotting results...")
        plot_results(results)
        
        print("\nSimulation complete!")

if __name__ == "__main__":
    main() 