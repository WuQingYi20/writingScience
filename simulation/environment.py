import random
import matplotlib.pyplot as plt
import numpy as np
from enum import Enum
from typing import List, Dict, Tuple, Optional, Any, Set


class SignalCondition(Enum):
    NO_SIGNAL = "No Signal"        # Players cannot send signals
    MANDATORY_SIGNAL = "Mandatory Signal"  # Players must send a signal (Red/Blue)
    OPTIONAL_SIGNAL = "Optional Signal"    # Players can choose to send a signal or not


class Strategy(Enum):
    HISTORY_BASED = "History Based"  # Frequency-based learning from history
    REWARD_BASED = "Reward Based"    # Reinforcement learning with reward updating


# Base Agent Class 
class Agent:
    def __init__(self, name: str):
        self.name = name
        # History tracking
        self.interaction_history = []  # List of interaction results
        self.signal_history = []       # List of signals sent
        self.choice_history = []       # List of final choices made

    def decide_signal(self, condition: SignalCondition) -> Optional[str]:
        """Decide what signal to send based on the communication condition"""
        raise NotImplementedError("Subclasses must implement this method")
        
    def decide_final_choice(self, opponent_signal: Optional[str], own_signal: Optional[str]) -> str:
        """Decide final choice (Red/Blue) based on signals"""
        raise NotImplementedError("Subclasses must implement this method")
        
    def update(self, own_signal: Optional[str], opponent_signal: Optional[str], 
               final_choice: str, opponent_choice: str, success: bool) -> None:
        """Update agent's internal state based on interaction outcome"""
        raise NotImplementedError("Subclasses must implement this method")


# History-Based Agent Implementation
class HistoryBasedAgent(Agent):
    def __init__(self, name: str):
        super().__init__(name)
        # Pseudocounts for initial beliefs
        self.PSEUDO_COUNT = 2.0
        # Counters for blue/red choices
        self.total_count = 2 * self.PSEUDO_COUNT
        self.blue_count = self.PSEUDO_COUNT
        
        # For optional signal condition
        # 初始状态：0.5概率不发送信号，0.25概率发送红色，0.25概率发送蓝色
        self.no_signal_count = 2 * self.PSEUDO_COUNT  # 初始不发送信号的计数
        self.signal_blue_count = self.PSEUDO_COUNT    # 初始发送蓝色信号的计数
        self.signal_red_count = self.PSEUDO_COUNT     # 初始发送红色信号的计数
        
        # 信号选择的总计数
        self.signal_choice_total = self.no_signal_count + self.signal_blue_count + self.signal_red_count
        
        # 信号效果的追踪
        self.no_signal_success_count = self.PSEUDO_COUNT
        self.blue_signal_success_count = self.PSEUDO_COUNT / 2
        self.red_signal_success_count = self.PSEUDO_COUNT / 2
    
    def get_blue_ratio(self) -> float:
        """Return probability of choosing Blue"""
        return self.blue_count / self.total_count
    
    def decide_signal(self, condition: SignalCondition) -> Optional[str]:
        if condition == SignalCondition.NO_SIGNAL:
            # No signal allowed
            signal = None
        elif condition == SignalCondition.MANDATORY_SIGNAL:
            # Must send a signal based on historical preference
            blue_ratio = self.get_blue_ratio()
            signal = "Blue" if random.random() < blue_ratio else "Red"
        else:  # OPTIONAL_SIGNAL
            # 计算三种选择的概率
            no_signal_prob = self.no_signal_count / self.signal_choice_total
            blue_signal_prob = self.signal_blue_count / self.signal_choice_total
            # red_signal_prob = self.signal_red_count / self.signal_choice_total
            
            # 根据概率决定是否发信号及信号颜色
            rand = random.random()
            if rand < no_signal_prob:
                signal = None
            elif rand < no_signal_prob + blue_signal_prob:
                signal = "Blue"
            else:
                signal = "Red"
        
        self.signal_history.append(signal)
        return signal
    
    def decide_final_choice(self, opponent_signal: Optional[str], own_signal: Optional[str]) -> str:
        # 在纯协调博弈中，如果对方发送了信号而自己没有，应始终跟随对方的信号
        if own_signal is None and opponent_signal is not None:
            choice = opponent_signal  # 始终跟随对方的信号
        # 如果自己发送了信号而对方没有，则选择自己的信号
        elif own_signal is not None and opponent_signal is None:
            choice = own_signal
        # 如果双方都发送了信号
        elif own_signal is not None and opponent_signal is not None:
            # 如果信号一致，则选择该信号
            if own_signal == opponent_signal:
                choice = own_signal
            # 如果信号不一致，则基于历史概率选择
            else:
                blue_ratio = self.get_blue_ratio()
                choice = "Blue" if random.random() < blue_ratio else "Red"
        # 如果双方都没有发送信号，则基于历史概率选择
        else:
            blue_ratio = self.get_blue_ratio()
            choice = "Blue" if random.random() < blue_ratio else "Red"
            
        self.choice_history.append(choice)
        return choice
    
    def update(self, own_signal: Optional[str], opponent_signal: Optional[str], 
               final_choice: str, opponent_choice: str, success: bool) -> None:
        # History-Based策略：更新基于频率统计
        
        # 1. 更新选择统计
        self.total_count += 1
        if final_choice == "Blue":
            self.blue_count += 1
        
        # 2. 更新信号选择的频率统计
        self.signal_choice_total += 1
        if own_signal is None:
            # 没有发送信号
            self.no_signal_count += 1
            if success:
                self.no_signal_success_count += 1
        elif own_signal == "Blue":
            # 发送蓝色信号
            self.signal_blue_count += 1
            if success:
                self.blue_signal_success_count += 1
        else:  # Red
            # 发送红色信号
            self.signal_red_count += 1
            if success:
                self.red_signal_success_count += 1
        
        # 3. 对于不同的信号条件，学习调整
        if own_signal is None and opponent_signal is not None:
            # 对方发信号自己不发：学习跟随
            if success and opponent_signal == final_choice:
                # 成功跟随后，增加该颜色的偏好
                if final_choice == "Blue":
                    self.blue_count += 0.5  # 加强蓝色倾向
                    self.total_count += 0.5
                else:
                    self.blue_count += 0  # 加强红色倾向
                    self.total_count += 0.5
        
        # 记录交互结果
        self.interaction_history.append({
            "own_signal": own_signal,
            "opponent_signal": opponent_signal,
            "own_choice": final_choice,
            "opponent_choice": opponent_choice,
            "success": success
        })


# Reward-Based Agent Implementation 
class RewardBasedAgent(Agent):
    def __init__(self, name: str):
        super().__init__(name)
        # Learning rate parameters
        self.ALPHA = 0.2  # Success update rate
        self.BETA = 0.2   # Failure update rate
        
        # Decision parameters
        self.p_choice_blue = 0.5  # 选择Blue的概率
        
        # 发送信号的相关参数
        self.p_send_signal = 0.5   # 发送信号的概率 (初始50%不发送信号)
        self.p_signal_blue = 0.5   # 如果发送信号，选择Blue的概率 (初始蓝色和红色各25%)
    
    def decide_signal(self, condition: SignalCondition) -> Optional[str]:
        if condition == SignalCondition.NO_SIGNAL:
            signal = None
        elif condition == SignalCondition.MANDATORY_SIGNAL:
            signal = "Blue" if random.random() < self.p_signal_blue else "Red"
        else:  # OPTIONAL_SIGNAL
            # 先决定是否发送信号
            if random.random() < self.p_send_signal:
                # 发送信号，再决定发送什么颜色
                signal = "Blue" if random.random() < self.p_signal_blue else "Red"
            else:
                signal = None
        
        self.signal_history.append(signal)
        return signal
    
    def decide_final_choice(self, opponent_signal: Optional[str], own_signal: Optional[str]) -> str:
        # 如果没有信号交换，决策基于选择偏好
        if own_signal is None and opponent_signal is None:
            choice = "Blue" if random.random() < self.p_choice_blue else "Red"
        # 如果只有对手发送了信号，在纯协调博弈中应始终跟随对手的信号
        elif own_signal is None and opponent_signal is not None:
            choice = opponent_signal  # 始终跟随
        # 如果只有自己发送了信号
        elif own_signal is not None and opponent_signal is None:
            choice = own_signal  # 始终坚持自己的信号
        # 如果双方都发送了信号
        else:
            if own_signal == opponent_signal:
                # 信号匹配，按照信号选择
                choice = own_signal
            else:
                # 信号冲突，直接使用p_choice_blue决定是选择蓝色还是红色
                choice = "Blue" if random.random() < self.p_choice_blue else "Red"
        
        self.choice_history.append(choice)
        return choice
    
    def update(self, own_signal: Optional[str], opponent_signal: Optional[str], 
               final_choice: str, opponent_choice: str, success: bool) -> None:
        # Reward-Based策略：基于成功/失败更新概率
        
        # 1. 直接更新p_choice_blue（全局选择偏好）
        if success:
            if final_choice == "Blue":
                self.p_choice_blue = self.p_choice_blue + self.ALPHA * (1 - self.p_choice_blue)
            else:  # Red
                self.p_choice_blue = self.p_choice_blue - self.ALPHA * self.p_choice_blue
        else:
            if final_choice == "Blue":
                self.p_choice_blue = self.p_choice_blue - self.BETA * self.p_choice_blue
            else:  # Red
                self.p_choice_blue = self.p_choice_blue + self.BETA * (1 - self.p_choice_blue)
        
        # 2. 更新信号发送概率
        if success:
            if own_signal is not None:  # 发送了信号且成功
                self.p_send_signal = self.p_send_signal + self.ALPHA * (1 - self.p_send_signal)
            else:  # 没发送信号且成功
                self.p_send_signal = self.p_send_signal - self.ALPHA * self.p_send_signal
        else:  # 不成功
            if own_signal is not None:  # 发送了信号但失败
                self.p_send_signal = self.p_send_signal - self.BETA * self.p_send_signal
            else:  # 没发送信号且失败
                self.p_send_signal = self.p_send_signal + self.BETA * (1 - self.p_send_signal)
        
        # 3. 如果发送了信号，更新信号颜色选择概率
        if own_signal is not None:
            if success:
                if own_signal == "Blue":
                    self.p_signal_blue = self.p_signal_blue + self.ALPHA * (1 - self.p_signal_blue)
                else:  # Red
                    self.p_signal_blue = self.p_signal_blue - self.ALPHA * self.p_signal_blue
            else:
                if own_signal == "Blue":
                    self.p_signal_blue = self.p_signal_blue - self.BETA * self.p_signal_blue
                else:  # Red
                    self.p_signal_blue = self.p_signal_blue + self.BETA * (1 - self.p_signal_blue)
        
        # 4. 特殊情况：信号冲突时的更新
        if (own_signal is not None and opponent_signal is not None and 
            own_signal != opponent_signal):
            # 信号冲突情况下的学习增强
            if success:
                # 如果冲突中选择成功，强化这种选择
                if final_choice == own_signal:
                    # 强化依赖自己信号的倾向
                    adj = self.ALPHA * 1.5  # 增强学习率
                    if own_signal == "Blue":
                        self.p_choice_blue = self.p_choice_blue + adj * (1 - self.p_choice_blue)
                    else:
                        self.p_choice_blue = self.p_choice_blue - adj * self.p_choice_blue
        
        # 确保所有概率都在[0,1]范围内
        self.p_send_signal = max(0.0, min(1.0, self.p_send_signal))
        self.p_signal_blue = max(0.0, min(1.0, self.p_signal_blue))
        self.p_choice_blue = max(0.0, min(1.0, self.p_choice_blue))
        
        # 记录交互结果
        self.interaction_history.append({
            "own_signal": own_signal,
            "opponent_signal": opponent_signal,
            "own_choice": final_choice,
            "opponent_choice": opponent_choice,
            "success": success
        })


class Environment:
    def __init__(self, 
                 num_agents: int, 
                 signal_condition: SignalCondition, 
                 strategy: Strategy):
        self.num_agents = num_agents
        self.signal_condition = signal_condition
        self.strategy = strategy
        
        # Create agents based on the strategy
        if strategy == Strategy.HISTORY_BASED:
            self.agents = [HistoryBasedAgent(f"Agent {i+1}") for i in range(num_agents)]
        else:  # REWARD_BASED
            self.agents = [RewardBasedAgent(f"Agent {i+1}") for i in range(num_agents)]
        
        # Track rounds and convergence
        self.rounds = 0
        self.converged = False
        self.convergence_choice = None  # The choice agents converged to
        
        # Track statistics
        self.interaction_stats = {
            "success_rate": [],  # Success rate per round
            "blue_choices": []   # Percentage of Blue choices per round
        }
    
    def _get_rotation_matchups(self):
        """Return rotation matchups"""
        n = self.num_agents
        
        if n == 3:
            # Special handling for three-person groups
            sitting_out = self.rounds % 3  # Player sitting out in rotation
            agents_playing = [agent for i, agent in enumerate(self.agents) if i != sitting_out]
            return [(agents_playing[0], agents_playing[1])]
        
        elif n % 2 == 0:  # Even number of players
            # Use rotation matching algorithm
            # First player is fixed, others rotate
            # For example with 4 players:
            # Round 1: (0,1), (2,3)
            # Round 2: (0,2), (1,3)
            # Round 3: (0,3), (1,2)
            # ...then cycle
            
            rotation_step = (self.rounds - 1) % (n - 1)
            matchups = []
            
            # First player fixed as 0
            fixed_agent = self.agents[0]
            
            # Calculate who matches with first player this round
            # Rotating player numbers from 1 to n-1
            rotation_idx = (rotation_step + 1) % (n - 1) + 1  # Get index from 1 to n-1
            matchups.append((fixed_agent, self.agents[rotation_idx]))
            
            # Pair remaining players in sequence
            remaining = [i for i in range(1, n) if i != rotation_idx]
            for i in range(0, len(remaining), 2):
                if i + 1 < len(remaining):
                    matchups.append((self.agents[remaining[i]], self.agents[remaining[i+1]]))
            
            return matchups
            
        else:  # Odd number of players (except 3)
            # Ensure each player sits out once every 3 rounds
            sitting_out = self.rounds % n  # Player sitting out in rotation
            active_agents = [agent for i, agent in enumerate(self.agents) if i != sitting_out]
            
            # Match remaining even number of players in rotation
            matchups = []
            n_active = len(active_agents)
            
            # If 2 players remain after sitting out, match them directly
            if n_active == 2:
                matchups.append((active_agents[0], active_agents[1]))
            else:
                # Otherwise use similar rotation algorithm as even case
                rotation_step = (self.rounds - 1) % (n_active - 1)
                
                # First player fixed
                fixed_agent = active_agents[0]
                
                # Calculate who matches with first player this round
                rotation_idx = (rotation_step + 1) % (n_active - 1) + 1
                matchups.append((fixed_agent, active_agents[rotation_idx]))
                
                # Pair remaining players in sequence
                remaining = [i for i in range(1, n_active) if i != rotation_idx]
                for i in range(0, len(remaining), 2):
                    if i + 1 < len(remaining):
                        matchups.append((active_agents[remaining[i]], active_agents[remaining[i+1]]))
            
            return matchups
    
    def run_round(self):
        """Run a single round of interactions"""
        self.rounds += 1
        
        # 使用轮换匹配代替随机匹配
        matchups = self._get_rotation_matchups()
        
        # Process each matchup
        successes = 0
        blue_count = 0
        
        for agent1, agent2 in matchups:
            # Step 1: Agents decide signals
            signal1 = agent1.decide_signal(self.signal_condition)
            signal2 = agent2.decide_signal(self.signal_condition)
            
            # Step 2: Agents make final choices
            choice1 = agent1.decide_final_choice(signal2, signal1)
            choice2 = agent2.decide_final_choice(signal1, signal2)
            
            # Step 3: Determine success
            success = (choice1 == choice2)
            if success:
                successes += 1
            
            # Count Blue choices for statistics
            if choice1 == "Blue":
                blue_count += 1
            if choice2 == "Blue":
                blue_count += 1
            
            # Step 4: Agents update based on outcome
            agent1.update(signal1, signal2, choice1, choice2, success)
            agent2.update(signal2, signal1, choice2, choice1, success)
        
        # Update statistics
        if matchups:  # Avoid division by zero if no matchups
            success_rate = successes / len(matchups)
            blue_ratio = blue_count / (len(matchups) * 2)  # 2 agents per matchup
            
            # For odd number of players (except 3-person groups), adjust statistics based on sitting out
            if self.num_agents % 2 != 0 and self.num_agents != 3:
                # Since only (n-1)/2 pairs interact each round, overall efficiency is (n-1)/n
                # To maintain fair comparison, multiply by adjustment factor 3/2
                adjustment_factor = self.num_agents / (self.num_agents - 1) * (3/2)
                success_rate *= adjustment_factor
            
            self.interaction_stats["success_rate"].append(success_rate)
            self.interaction_stats["blue_choices"].append(blue_ratio)
        
        # Check for convergence
        self._check_convergence()
    
    def _check_convergence(self):
        """Check if all agents have converged to the same choice"""
        # Only check every 10 rounds to avoid excessive checking
        if self.rounds % 10 != 0:
            return False
            
        # Get last choices of all agents who have made choices
        last_choices = [agent.choice_history[-1] for agent in self.agents 
                        if agent.choice_history]
        
        # If all agents have made at least one choice and all choices are the same
        if (len(last_choices) == self.num_agents and 
            all(choice == last_choices[0] for choice in last_choices)):
            self.converged = True
            self.convergence_choice = last_choices[0]
            return True
        
        return False
    
    def run_simulation(self, max_rounds=100000):
        """Run the simulation until convergence or max rounds"""
        while not self.converged and self.rounds < max_rounds:
            self.run_round()
        
        return self.rounds, self.converged, self.convergence_choice
    
    def print_status(self):
        """Print the current status of the simulation"""
        if self.converged:
            print(f"Converged after {self.rounds} rounds to {self.convergence_choice}")
        else:
            print(f"Did not converge after {self.rounds} rounds")
        
        # Print agent statistics based on strategy
        if self.strategy == Strategy.HISTORY_BASED:
            for agent in self.agents:
                print(f"{agent.name}: Blue Ratio = {agent.get_blue_ratio():.2f}")
        else:  # REWARD_BASED
            for agent in self.agents:
                print(f"{agent.name}: p_choice_blue = {agent.p_choice_blue:.2f}, " +
                      f"p_signal_blue = {agent.p_signal_blue:.2f}")


def run_all_scenarios(agent_sizes=[2, 3, 4, 6, 8, 10, 16, 20], 
                      runs_per_scenario=20, 
                      max_rounds=100000):
    """Run simulations for all combinations of conditions and strategies"""
    results = {}
    
    for signal_condition in SignalCondition:
        for strategy in Strategy:
            scenario_key = f"{signal_condition.value} - {strategy.value}"
            results[scenario_key] = {}
            
            print(f"\nRunning scenario: {scenario_key}")
            
            for size in agent_sizes:
                round_counts = []
                convergence_counts = 0
                blue_convergence = 0
                
                for run in range(runs_per_scenario):
                    env = Environment(size, signal_condition, strategy)
                    rounds, converged, choice = env.run_simulation(max_rounds)
                    
                    round_counts.append(rounds)
                    if converged:
                        convergence_counts += 1
                        if choice == "Blue":
                            blue_convergence += 1
                
                # Calculate statistics
                avg_rounds = sum(round_counts) / len(round_counts)
                convergence_rate = convergence_counts / runs_per_scenario
                blue_rate = blue_convergence / convergence_counts if convergence_counts > 0 else 0
                
                results[scenario_key][size] = {
                    "avg_rounds": avg_rounds,
                    "convergence_rate": convergence_rate,
                    "blue_convergence_rate": blue_rate
                }
                
                print(f"  Agent Size: {size}, Avg Rounds: {avg_rounds:.1f}, " +
                      f"Convergence Rate: {convergence_rate:.2f}, " +
                      f"Blue Convergence: {blue_rate:.2f}")
    
    return results


def plot_results(results):
    """Plot comparison charts of all scenarios"""
    agent_sizes = sorted(list(next(iter(results.values())).keys()))
    scenarios = list(results.keys())
    
    # Plot rounds to convergence
    plt.figure(figsize=(12, 8))
    for scenario in scenarios:
        rounds_list = [results[scenario][size]["avg_rounds"] for size in agent_sizes]
        plt.plot(agent_sizes, rounds_list, marker='o', label=scenario)
    
    plt.xlabel("Number of Agents")
    plt.ylabel("Average Rounds to Convergence")
    plt.title("Convergence Rounds vs. Agent Population Size")
    plt.legend()
    plt.grid(True)
    plt.savefig("convergence_rounds.png")
    plt.show()
    
    # Plot convergence rates
    plt.figure(figsize=(12, 8))
    for scenario in scenarios:
        conv_rates = [results[scenario][size]["convergence_rate"] for size in agent_sizes]
        plt.plot(agent_sizes, conv_rates, marker='o', label=scenario)
    
    plt.xlabel("Number of Agents")
    plt.ylabel("Convergence Rate")
    plt.title("Convergence Rate vs. Agent Population Size")
    plt.legend()
    plt.grid(True)
    plt.savefig("convergence_rates.png")
    plt.show()
    
    # Plot blue convergence rates
    plt.figure(figsize=(12, 8))
    for scenario in scenarios:
        blue_rates = [results[scenario][size]["blue_convergence_rate"] for size in agent_sizes]
        plt.plot(agent_sizes, blue_rates, marker='o', label=scenario)
    
    plt.xlabel("Number of Agents")
    plt.ylabel("Blue Convergence Rate")
    plt.title("Blue Convergence Rate vs. Agent Population Size")
    plt.legend()
    plt.grid(True)
    plt.savefig("blue_convergence_rates.png")
    plt.show()


def main():
    # Run simulations for all scenarios
    print("Running all scenarios...")
    results = run_all_scenarios()
    
    # Plot comparison charts
    print("\nPlotting results...")
    plot_results(results)
    
    print("\nSimulation complete!")


if __name__ == "__main__":
    main() 