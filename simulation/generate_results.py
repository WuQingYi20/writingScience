import json
import csv
import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from environment import (
    SignalCondition, 
    Strategy, 
    Environment, 
    run_all_scenarios
)

def generate_detailed_results(agent_sizes=[2, 3, 4, 6, 8, 10, 16, 20], 
                             runs_per_scenario=20, 
                             max_rounds=100000):
    """Run all scenarios and save detailed results to json and csv files"""
    
    # Create directory for saving results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = f"results_{timestamp}"
    os.makedirs(results_dir, exist_ok=True)
    
    # Record run parameters
    config = {
        "agent_sizes": agent_sizes,
        "runs_per_scenario": runs_per_scenario,
        "max_rounds": max_rounds,
        "timestamp": timestamp
    }
    
    # Save configuration
    with open(f"{results_dir}/config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    # Run all scenarios
    print("Running all 6 scenarios...")
    results = run_all_scenarios(agent_sizes, runs_per_scenario, max_rounds)
    
    # Save complete results to JSON file
    with open(f"{results_dir}/full_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    # Create CSV table data
    print("\nGenerating CSV reports...")
    
    # Create a separate CSV for each metric
    metrics = ["avg_rounds", "convergence_rate", "blue_convergence_rate"]
    
    for metric in metrics:
        csv_filename = f"{results_dir}/{metric}.csv"
        with open(csv_filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            
            # Write header
            scenarios = list(results.keys())
            header = ["Agent Size"] + scenarios
            writer.writerow(header)
            
            # Write data rows
            for size in agent_sizes:
                row = [size]
                for scenario in scenarios:
                    row.append(results[scenario][size][metric])
                writer.writerow(row)
    
    # Generate results summary for article reference
    generate_article_summary(results, results_dir, agent_sizes)
    
    # Plot and save charts
    plot_and_save_charts(results, results_dir, agent_sizes)
    
    print(f"\nAll results have been saved to directory: {results_dir}")
    return results_dir

def generate_article_summary(results, results_dir, agent_sizes):
    """Generate a summary of results for article reference"""
    
    summary_file = f"{results_dir}/article_summary.md"
    
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write("# Simulation Results Summary\n\n")
        
        # All scenarios comparison
        f.write("## Convergence Comparison Across Scenarios\n\n")
        
        # Create table: average convergence rounds for different agent sizes across scenarios
        f.write("### Average Convergence Rounds\n\n")
        f.write("| Agent Size |")
        scenarios = list(results.keys())
        for scenario in scenarios:
            f.write(f" {scenario} |")
        f.write("\n")
        
        f.write("| --- |")
        for _ in scenarios:
            f.write(" --- |")
        f.write("\n")
        
        for size in agent_sizes:
            f.write(f"| {size} |")
            for scenario in scenarios:
                value = results[scenario][size]["avg_rounds"]
                f.write(f" {value:.1f} |")
            f.write("\n")
        
        # Convergence rate table
        f.write("\n### Convergence Rate\n\n")
        f.write("| Agent Size |")
        for scenario in scenarios:
            f.write(f" {scenario} |")
        f.write("\n")
        
        f.write("| --- |")
        for _ in scenarios:
            f.write(" --- |")
        f.write("\n")
        
        for size in agent_sizes:
            f.write(f"| {size} |")
            for scenario in scenarios:
                value = results[scenario][size]["convergence_rate"]
                f.write(f" {value:.2f} |")
            f.write("\n")
            
        # Blue convergence rate table
        f.write("\n### Blue Choice Convergence Rate\n\n")
        f.write("| Agent Size |")
        for scenario in scenarios:
            f.write(f" {scenario} |")
        f.write("\n")
        
        f.write("| --- |")
        for _ in scenarios:
            f.write(" --- |")
        f.write("\n")
        
        for size in agent_sizes:
            f.write(f"| {size} |")
            for scenario in scenarios:
                value = results[scenario][size]["blue_convergence_rate"]
                f.write(f" {value:.2f} |")
            f.write("\n")
        
        # Signal condition analysis
        f.write("\n## Signal Condition Comparison\n\n")
        for condition in SignalCondition:
            cond_name = condition.value
            f.write(f"### {cond_name}\n\n")
            
            # Calculate averages under this condition
            f.write("Average performance across different strategies and agent sizes:\n\n")
            
            # Filter scenarios for this condition
            condition_scenarios = [s for s in scenarios if cond_name in s]
            
            # Convergence rounds
            avg_rounds_by_size = {}
            for size in agent_sizes:
                values = [results[s][size]["avg_rounds"] for s in condition_scenarios]
                avg_rounds_by_size[size] = sum(values) / len(values)
            
            # Find fastest and slowest convergence
            min_rounds = min(avg_rounds_by_size.items(), key=lambda x: x[1])
            max_rounds = max(avg_rounds_by_size.items(), key=lambda x: x[1])
            
            f.write(f"- Fastest convergence with {min_rounds[0]} agents (average {min_rounds[1]:.1f} rounds)\n")
            f.write(f"- Slowest convergence with {max_rounds[0]} agents (average {max_rounds[1]:.1f} rounds)\n\n")
            
            # Strategy comparison
            for strategy in Strategy:
                strat_name = strategy.value
                scenario = f"{cond_name} - {strat_name}"
                if scenario in scenarios:
                    f.write(f"#### {strat_name} Strategy\n\n")
                    
                    # Special analysis for three-agent groups
                    if 3 in agent_sizes:
                        three_agent_data = results[scenario][3]
                        f.write(f"Three-agent group performance:\n")
                        f.write(f"- Average convergence rounds: {three_agent_data['avg_rounds']:.1f}\n")
                        f.write(f"- Convergence rate: {three_agent_data['convergence_rate']:.2f}\n")
                        f.write(f"- Blue choice rate: {three_agent_data['blue_convergence_rate']:.2f}\n\n")
        
        # Strategy analysis
        f.write("\n## Strategy Comparison\n\n")
        for strategy in Strategy:
            strat_name = strategy.value
            f.write(f"### {strat_name}\n\n")
            
            # Calculate averages under this strategy
            f.write("Average performance across different signal conditions and agent sizes:\n\n")
            
            # Filter scenarios for this strategy
            strategy_scenarios = [s for s in scenarios if strat_name in s]
            
            # Convergence rate
            avg_conv_by_size = {}
            for size in agent_sizes:
                values = [results[s][size]["convergence_rate"] for s in strategy_scenarios]
                avg_conv_by_size[size] = sum(values) / len(values)
            
            # Find highest and lowest convergence rates
            max_conv = max(avg_conv_by_size.items(), key=lambda x: x[1])
            min_conv = min(avg_conv_by_size.items(), key=lambda x: x[1])
            
            f.write(f"- Highest convergence rate with {max_conv[0]} agents (average {max_conv[1]:.2f})\n")
            f.write(f"- Lowest convergence rate with {min_conv[0]} agents (average {min_conv[1]:.2f})\n\n")
            
        # Key observations
        f.write("\n## Key Observations\n\n")
        
        # Find average convergence rounds across scenarios
        avg_rounds_all = {}
        for size in agent_sizes:
            avg_rounds_all[size] = sum(results[s][size]["avg_rounds"] for s in scenarios) / len(scenarios)
        
        # Relationship between convergence difficulty and agent size
        size_rounds_sorted = sorted(avg_rounds_all.items(), key=lambda x: x[1])
        easiest_size = size_rounds_sorted[0][0]
        hardest_size = size_rounds_sorted[-1][0]
        
        f.write(f"1. Overall, groups with {easiest_size} agents converge fastest, while groups with {hardest_size} agents converge slowest.\n\n")
        
        # Impact of signal conditions on convergence
        signal_impact = {}
        for condition in SignalCondition:
            cond_name = condition.value
            condition_scenarios = [s for s in scenarios if cond_name in s]
            avg_rounds = 0
            count = 0
            for size in agent_sizes:
                for s in condition_scenarios:
                    avg_rounds += results[s][size]["avg_rounds"]
                    count += 1
            signal_impact[cond_name] = avg_rounds / count
        
        best_signal = min(signal_impact.items(), key=lambda x: x[1])
        worst_signal = max(signal_impact.items(), key=lambda x: x[1])
        
        f.write(f"2. Among signal conditions, {best_signal[0]} has the most positive impact on convergence speed, while {worst_signal[0]} is least conducive to rapid convergence.\n\n")
        
        # Impact of strategies on convergence
        strategy_impact = {}
        for strategy in Strategy:
            strat_name = strategy.value
            strategy_scenarios = [s for s in scenarios if strat_name in s]
            avg_rounds = 0
            count = 0
            for size in agent_sizes:
                for s in strategy_scenarios:
                    avg_rounds += results[s][size]["avg_rounds"]
                    count += 1
            strategy_impact[strat_name] = avg_rounds / count
        
        better_strategy = min(strategy_impact.items(), key=lambda x: x[1])
        worse_strategy = max(strategy_impact.items(), key=lambda x: x[1])
        
        f.write(f"3. In strategy comparison, {better_strategy[0]} performs better overall with faster convergence.\n\n")

def plot_and_save_charts(results, results_dir, agent_sizes):
    """Plot and save detailed charts"""
    
    scenarios = list(results.keys())
    
    # Create comparison charts directory
    charts_dir = f"{results_dir}/charts"
    os.makedirs(charts_dir, exist_ok=True)
    
    # 1. Convergence rounds comparison across all scenarios
    plt.figure(figsize=(12, 8))
    for scenario in scenarios:
        rounds_list = [results[scenario][size]["avg_rounds"] for size in agent_sizes]
        plt.plot(agent_sizes, rounds_list, marker='o', label=scenario)
    
    plt.xlabel("Number of Agents")
    plt.ylabel("Average Convergence Rounds")
    plt.title("Convergence Rounds Comparison Across Scenarios")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{charts_dir}/convergence_rounds_all.png", dpi=300)
    plt.close()
    
    # 2. Signal condition group comparison
    for condition in SignalCondition:
        cond_name = condition.value
        plt.figure(figsize=(10, 6))
        
        # Find scenarios for this condition
        condition_scenarios = [s for s in scenarios if cond_name in s]
        
        for scenario in condition_scenarios:
            rounds_list = [results[scenario][size]["avg_rounds"] for size in agent_sizes]
            plt.plot(agent_sizes, rounds_list, marker='o', label=scenario.replace(f"{cond_name} - ", ""))
        
        plt.xlabel("Number of Agents")
        plt.ylabel("Average Convergence Rounds")
        plt.title(f"Convergence Rounds Under {cond_name}")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"{charts_dir}/convergence_rounds_{cond_name.replace(' ', '_')}.png", dpi=300)
        plt.close()
    
    # 3. Strategy group comparison
    for strategy in Strategy:
        strat_name = strategy.value
        plt.figure(figsize=(10, 6))
        
        # Find scenarios for this strategy
        strategy_scenarios = [s for s in scenarios if strat_name in s]
        
        for scenario in strategy_scenarios:
            rounds_list = [results[scenario][size]["avg_rounds"] for size in agent_sizes]
            plt.plot(agent_sizes, rounds_list, marker='o', label=scenario.replace(f" - {strat_name}", ""))
        
        plt.xlabel("Number of Agents")
        plt.ylabel("Average Convergence Rounds")
        plt.title(f"Convergence Rounds Under {strat_name} Strategy")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"{charts_dir}/convergence_rounds_{strat_name.replace(' ', '_')}.png", dpi=300)
        plt.close()
    
    # 4. Special analysis for three-agent groups
    if 3 in agent_sizes:
        plt.figure(figsize=(8, 6))
        scenarios_sorted = sorted(scenarios)
        three_agent_rounds = [results[s][3]["avg_rounds"] for s in scenarios_sorted]
        
        # Use bar chart
        bars = plt.bar(range(len(scenarios_sorted)), three_agent_rounds, color='skyblue')
        plt.xticks(range(len(scenarios_sorted)), [s.replace(" - ", "\n") for s in scenarios_sorted], rotation=0)
        plt.ylabel("Average Convergence Rounds")
        plt.title("Three-Agent Group Performance Across Scenarios")
        plt.grid(True, axis='y')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{height:.1f}', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig(f"{charts_dir}/three_agents_comparison.png", dpi=300)
        plt.close()
    
    # 5. Convergence rate chart
    plt.figure(figsize=(12, 8))
    for scenario in scenarios:
        conv_rates = [results[scenario][size]["convergence_rate"] for size in agent_sizes]
        plt.plot(agent_sizes, conv_rates, marker='o', label=scenario)
    
    plt.xlabel("Number of Agents")
    plt.ylabel("Convergence Rate")
    plt.title("Convergence Rate Comparison Across Scenarios")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{charts_dir}/convergence_rates_all.png", dpi=300)
    plt.close()
    
    # 6. Blue choice rate chart
    plt.figure(figsize=(12, 8))
    for scenario in scenarios:
        blue_rates = [results[scenario][size]["blue_convergence_rate"] for size in agent_sizes]
        plt.plot(agent_sizes, blue_rates, marker='o', label=scenario)
    
    plt.xlabel("Number of Agents")
    plt.ylabel("Blue Choice Convergence Rate")
    plt.title("Blue Choice Convergence Rate Across Scenarios")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{charts_dir}/blue_convergence_rates_all.png", dpi=300)
    plt.close()

def main():
    print("Generating results for all 6 scenarios (3 signal conditions × 2 strategies)...")
    
    # Adjustable parameters
    agent_sizes = [2, 3, 4, 6, 8, 10, 16, 20]  # List of agent sizes
    runs_per_scenario = 20                    # Number of runs per scenario
    max_rounds = 100000                       # Maximum rounds per simulation
    
    # Run and generate results
    results_dir = generate_detailed_results(agent_sizes, runs_per_scenario, max_rounds)
    
    print(f"\nComplete! All results have been saved to directory: {results_dir}")
    print(f"Analysis report has been saved to: {results_dir}/article_summary.md")

if __name__ == "__main__":
    main() 