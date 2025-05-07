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
    def __init__(self, name: str, pseudo_count: float = 2.0, learning_step_follow: float = 0.5):
        super().__init__(name)
        # Pseudocounts for initial beliefs
        self.PSEUDO_COUNT = pseudo_count
        self.learning_step_follow = learning_step_follow
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
                    self.blue_count += self.learning_step_follow  # 加强蓝色倾向
                    self.total_count += self.learning_step_follow
                else:
                    self.blue_count += 0  # 加强红色倾向 # This implies red_count effectively increases as total_count does but blue_count doesn't
                    self.total_count += self.learning_step_follow
        
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
    def __init__(self, name: str, alpha: float = 0.2, beta: float = 0.2,
                 initial_p_choice_blue: float = 0.5,
                 initial_p_send_signal: float = 0.5,
                 initial_p_signal_blue: float = 0.5,
                 conflict_learning_boost: float = 1.5):
        super().__init__(name)
        # Learning rate parameters
        self.ALPHA = alpha
        self.BETA = beta
        self.conflict_learning_boost = conflict_learning_boost
        
        # Decision parameters
        self.p_choice_blue = initial_p_choice_blue  # 选择Blue的概率
        
        # 发送信号的相关参数
        self.p_send_signal = initial_p_send_signal   # 发送信号的概率 (初始50%不发送信号)
        self.p_signal_blue = initial_p_signal_blue   # 如果发送信号，选择Blue的概率 (初始蓝色和红色各25%)
    
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
                    adj = self.ALPHA * self.conflict_learning_boost  # 增强学习率
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
                 agent_configs: List[Dict[str, Any]], 
                 signal_condition: SignalCondition):
        self.agent_configs = agent_configs
        self.num_agents = len(agent_configs)
        self.signal_condition = signal_condition
        
        self.agents: List[Agent] = []
        for i, config in enumerate(agent_configs):
            agent_name = config.get("name", f"Agent {i+1}")
            strategy_type = config.get("strategy_type")
            params = config.get("params", {})

            if strategy_type == Strategy.HISTORY_BASED:
                self.agents.append(
                    HistoryBasedAgent(
                        name=agent_name,
                        pseudo_count=params.get("pseudo_count", 2.0),
                        learning_step_follow=params.get("learning_step_follow", 0.5)
                    )
                )
            elif strategy_type == Strategy.REWARD_BASED:
                self.agents.append(
                    RewardBasedAgent(
                        name=agent_name,
                        alpha=params.get("alpha", 0.2),
                        beta=params.get("beta", 0.2),
                        initial_p_choice_blue=params.get("initial_p_choice_blue", 0.5),
                        initial_p_send_signal=params.get("initial_p_send_signal", 0.5),
                        initial_p_signal_blue=params.get("initial_p_signal_blue", 0.5),
                        conflict_learning_boost=params.get("conflict_learning_boost", 1.5)
                    )
                )
            else:
                raise ValueError(f"Unknown strategy_type: {strategy_type} for agent {agent_name}")

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
        
        if n < 2: # Cannot form pairs if less than 2 agents
            return []

        if n == 3:
            # Special handling for three-person groups
            sitting_out = self.rounds % 3  # Player sitting out in rotation
            agents_playing = [agent for i, agent in enumerate(self.agents) if i != sitting_out]
            if len(agents_playing) == 2: # Ensure we still have two players
                 return [(agents_playing[0], agents_playing[1])]
            else: # Should not happen if n=3, but as a safeguard
                 return []
        
        elif n % 2 == 0:  # Even number of players
            # Use rotation matching algorithm
            # First player is fixed, others rotate
            # For example with 4 players:
            # Round 1: (0,1), (2,3)
            # Round 2: (0,2), (1,3)
            # Round 3: (0,3), (1,2)
            # ...then cycle
            
            # Adjust rounds for 0-based indexing for modulo operations if needed, but current logic seems fine
            # The number of distinct sets of pairings is n-1
            if n == 2: # Special case for 2 agents, always match them
                return [(self.agents[0], self.agents[1])]

            rotation_step = self.rounds % (n - 1) # self.rounds can start from 0 or 1. If 0, it's fine.
                                                  # If rounds starts from 1, (self.rounds -1) % (n-1) is also common.
                                                  # Let's assume self.rounds starts from 0 for simplicity here.
            
            matchups = []
            
            # Create a temporary list of agents to permute, excluding the first agent.
            # Agents from index 1 to n-1
            rotating_agents = list(self.agents[1:]) 
            
            # Apply the rotation to the list of rotating_agents
            # For each step in rotation_step, the last element moves to the first position
            for _ in range(rotation_step):
                last_agent = rotating_agents.pop()
                rotating_agents.insert(0, last_agent)

            # Match the first agent (self.agents[0]) with the first agent in the now-rotated list
            matchups.append((self.agents[0], rotating_agents[0]))
            
            # Pair up the rest of the agents in the rotated list
            # These are now from rotating_agents[1] to rotating_agents[n-2]
            for i in range(1, len(rotating_agents) // 2 + 1): # Iterate up to half the length of remaining agents
                idx1 = 2 * i - 1
                idx2 = 2 * i
                if idx2 < len(rotating_agents) : # Ensure the second index is within bounds
                    matchups.append((rotating_agents[idx1], rotating_agents[idx2]))
            
            return matchups
            
        else:  # Odd number of players (n > 3, since n=3 is handled)
            # Each player sits out once in n rounds
            sitting_out_idx = self.rounds % n
            active_agents = [agent for i, agent in enumerate(self.agents) if i != sitting_out_idx]
            
            # Now we have an even number of active_agents (n-1 agents)
            # We can apply the even number matching logic to active_agents
            n_active = len(active_agents)
            if n_active < 2: return []

            if n_active == 2:
                 return [(active_agents[0], active_agents[1])]

            matchups = []
            # rotation_step for the active_agents group
            # The number of distinct sets of pairings for n_active agents is n_active - 1
            rotation_step = self.rounds % (n_active - 1) 

            temp_rotating_agents = list(active_agents[1:])

            for _ in range(rotation_step):
                last_agent = temp_rotating_agents.pop()
                temp_rotating_agents.insert(0, last_agent)
            
            matchups.append((active_agents[0], temp_rotating_agents[0]))

            for i in range(1, len(temp_rotating_agents) // 2 + 1):
                idx1 = 2 * i - 1
                idx2 = 2 * i
                if idx2 < len(temp_rotating_agents):
                    matchups.append((temp_rotating_agents[idx1], temp_rotating_agents[idx2]))
            return matchups
    
    def run_round(self):
        """Run a single round of interactions"""
        self.rounds += 1 # Increment rounds at the beginning
        
        matchups = self._get_rotation_matchups()
        
        if not matchups: # If no matchups (e.g., less than 2 players, or error in logic)
            # Potentially log this or handle as an empty round
            # For stats, ensure no division by zero if interaction_stats expects updates
            self.interaction_stats["success_rate"].append(0) # Or np.nan / None
            self.interaction_stats["blue_choices"].append(0) # Or np.nan / None
            self._check_convergence() # Still check convergence, maybe they converged by doing nothing
            return

        successes = 0
        blue_count = 0
        num_interactions = len(matchups)
        num_choices_made = 0 # For blue_ratio calculation
        
        for agent1, agent2 in matchups:
            # Step 1: Agents decide signals
            signal1 = agent1.decide_signal(self.signal_condition)
            signal2 = agent2.decide_signal(self.signal_condition)
            
            # Step 2: Agents make final choices
            choice1 = agent1.decide_final_choice(signal2, signal1)
            choice2 = agent2.decide_final_choice(signal1, signal2)
            num_choices_made +=2
            
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
        current_success_rate = successes / num_interactions if num_interactions > 0 else 0
        current_blue_ratio = blue_count / num_choices_made if num_choices_made > 0 else 0
        
        # The adjustment factor logic for odd players (except 3) was complex and
        # might need re-evaluation or simplification if it was meant to normalize
        # per-capita interaction rates. Given rotation, each player participates
        # almost equally over time. For now, we'll record direct success rates.
        # If self.num_agents % 2 != 0 and self.num_agents > 3:
        #     adjustment_factor = self.num_agents / (self.num_agents - 1) 
        #     current_success_rate *= adjustment_factor # This adjustment seems specific and may need review

        self.interaction_stats["success_rate"].append(current_success_rate)
        self.interaction_stats["blue_choices"].append(current_blue_ratio)
        
        # Check for convergence
        self._check_convergence()
    
    def _check_convergence(self):
        """Check if all agents have converged to the same choice"""
        # Only check every 10 rounds to avoid excessive checking
        if self.rounds % 10 != 0: # Or self.rounds == 0 if rounds start from 0
            return # False is implicitly returned by no explicit return
            
        # Get last choices of all agents who have made choices
        if not self.agents: return # No agents, no convergence

        last_choices = [agent.choice_history[-1] for agent in self.agents 
                        if agent.choice_history] # Ensure choice_history is not empty
        
        # If all agents have made at least one choice and all choices are the same
        if (len(last_choices) == self.num_agents and self.num_agents > 0 and
            all(choice == last_choices[0] for choice in last_choices)):
            self.converged = True
            self.convergence_choice = last_choices[0]
            # return True # Not strictly necessary to return from here
        
        # return False # Not strictly necessary
    
    def run_simulation(self, max_rounds=100000):
        """Run the simulation until convergence or max rounds"""
        self.rounds = 0 # Ensure rounds reset for a new simulation run
        self.converged = False
        self.convergence_choice = None
        # Reset agent history for fresh simulation if env object is reused for multiple simulations
        # This should ideally be done when creating a new Environment instance for each run.
        # For now, assuming fresh Environment for each call to run_simulation.

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
        for agent in self.agents:
            if isinstance(agent, HistoryBasedAgent):
                print(f"{agent.name} (HistoryBased): Blue Ratio = {agent.get_blue_ratio():.2f}")
            elif isinstance(agent, RewardBasedAgent):
                print(f"{agent.name} (RewardBased): p_choice_blue = {agent.p_choice_blue:.2f}, " +
                      f"p_send_signal = {agent.p_send_signal:.2f}, " + # Added p_send_signal for completeness
                      f"p_signal_blue = {agent.p_signal_blue:.2f}")
            else:
                print(f"{agent.name} (Unknown Type): No specific stats available.")


def run_all_scenarios(experiment_setups: List[Dict[str, Any]], 
                      default_runs_per_setup=20, 
                      default_max_rounds=100000):
    """Run simulations for a defined list of experimental setups."""
    all_results = {}
    
    for setup_config in experiment_setups:
        setup_name = setup_config.get("name", f"Experiment_{len(all_results) + 1}")
        agent_configs = setup_config.get("agent_configs")
        signal_condition_enum = setup_config.get("signal_condition")
        
        # Ensure signal_condition is the Enum member, not just string value
        if isinstance(signal_condition_enum, str):
             try:
                 signal_condition = SignalCondition(signal_condition_enum) # If names match enum values
             except ValueError:
                 # Or try matching by name if string is like "NO_SIGNAL"
                 signal_condition = getattr(SignalCondition, signal_condition_enum.upper().replace(" ", "_"), None)
                 if signal_condition is None:
                     print(f"Warning: Could not parse signal_condition '{signal_condition_enum}' for setup '{setup_name}'. Skipping.")
                     continue
        elif isinstance(signal_condition_enum, SignalCondition):
            signal_condition = signal_condition_enum
        else:
            print(f"Warning: Invalid signal_condition type for setup '{setup_name}'. Skipping.")
            continue

        if not agent_configs:
            print(f"Warning: No agent_configs provided for setup '{setup_name}'. Skipping.")
            continue
            
        num_agents = len(agent_configs) # Derived from configs

        runs_for_this_setup = setup_config.get("runs_per_setup", default_runs_per_setup)
        max_rounds_for_this_setup = setup_config.get("max_rounds", default_max_rounds)
        
        all_results[setup_name] = {
            "config": { # Store config for reference
                "agent_configs": agent_configs, # Could be verbose, consider summarizing if too large
                "signal_condition": signal_condition.value,
                "num_agents": num_agents,
                "runs_per_setup": runs_for_this_setup,
                "max_rounds": max_rounds_for_this_setup
            },
            "runs_data": [] # Detailed data for each run
        }
            
        print(f"\nRunning Experiment Setup: {setup_name}")
        print(f"  Signal Condition: {signal_condition.value}")
        print(f"  Number of Agents: {num_agents}")
        print(f"  Runs for this setup: {runs_for_this_setup}")

        round_counts_all_runs = []
        convergence_counts_total = 0
        blue_convergence_total = 0
        
        for run_num in range(runs_for_this_setup):
            print(f"  Starting run {run_num + 1}/{runs_for_this_setup}...")
            # Critical: Create a new Environment instance for each run to ensure independence
            env = Environment(agent_configs=agent_configs, 
                              signal_condition=signal_condition)
            
            rounds, converged, choice = env.run_simulation(max_rounds_for_this_setup)
            
            run_data = {
                "run_number": run_num + 1,
                "rounds_to_convergence": rounds,
                "converged": converged,
                "convergence_choice": choice.value if choice else None # Store enum value
            }
            all_results[setup_name]["runs_data"].append(run_data)

            round_counts_all_runs.append(rounds)
            if converged:
                convergence_counts_total += 1
                if choice == "Blue": # Assuming choice is "Blue" or "Red" string
                    blue_convergence_total += 1
        
        # Calculate summary statistics for this setup
        avg_rounds = np.mean(round_counts_all_runs) if round_counts_all_runs else 0
        convergence_rate = convergence_counts_total / runs_for_this_setup if runs_for_this_setup > 0 else 0
        
        # Rate of converging to "Blue", given that convergence occurred
        blue_conv_rate_if_converged = blue_convergence_total / convergence_counts_total if convergence_counts_total > 0 else 0
        
        all_results[setup_name]["summary_stats"] = {
            "avg_rounds_to_convergence": avg_rounds,
            "convergence_rate": convergence_rate,
            "blue_convergence_rate_given_convergence": blue_conv_rate_if_converged,
            "total_runs": runs_for_this_setup,
            "total_converged": convergence_counts_total,
            "total_converged_blue": blue_convergence_total
        }
        
        print(f"  Setup '{setup_name}' Summary: Avg Rounds: {avg_rounds:.1f}, " +
              f"Convergence Rate: {convergence_rate:.2f}, " +
              f"Blue Conv. (if conv.): {blue_conv_rate_if_converged:.2f}")
    
    return all_results


def plot_results(results):
    """Plot comparison charts of all scenarios (NEEDS MAJOR REWORK for new results structure)"""
    # This function needs a complete overhaul to work with the new `results` structure.
    # The old structure was results[scenario_key][size][metric].
    # The new structure is results[setup_name]["summary_stats"][metric].
    # Plotting will need to consider how to group or compare different `setup_name`s.
    # For example, if setups vary by 'num_agents' systematically, one could plot against that.
    # Or, compare different strategies under the same num_agents and signal_condition.
    
    print("Plotting results (Note: plot_results needs rework for new data structure).")
    
    # Example: Plot average rounds to convergence for each setup if desired
    # This is a very basic plot and might not be what's needed.
    
    setup_names = list(results.keys())
    avg_rounds_list = [results[name]["summary_stats"]["avg_rounds_to_convergence"] for name in setup_names]
    
    if not setup_names:
        print("No results to plot.")
        return

    plt.figure(figsize=(max(10, len(setup_names) * 0.5), 6)) # Dynamic width
    plt.bar(setup_names, avg_rounds_list)
    plt.xlabel("Experiment Setup Name")
    plt.ylabel("Average Rounds to Convergence")
    plt.title("Average Convergence Rounds per Setup")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("convergence_rounds_per_setup.png")
    plt.show()
    plt.close()

    # Further plots (convergence rate, blue convergence rate) would follow a similar pattern
    # but require careful thought on how to present them meaningfully given the new structure.
    # For instance, if you have setups specifically designed to test N_agents,
    # you'd need to extract that N from the setup_name or config to plot against it.


def main():
    # This main is for testing environment.py directly.
    # It needs to be updated to create example `experiment_setups`.
    print("Running example with heterogeneous agents in environment.py main...")

    # Example Experiment Setups
    experiment_setups_example = [
        {
            "name": "2_Hist_vs_Rew_Mandatory",
            "signal_condition": SignalCondition.MANDATORY_SIGNAL,
            "runs_per_setup": 5, # Fewer runs for quick test
            "max_rounds": 50000,
            "agent_configs": [
                {"strategy_type": Strategy.HISTORY_BASED, "name": "HistAgent1", "params": {"pseudo_count": 1.0}},
                {"strategy_type": Strategy.REWARD_BASED, "name": "RewAgent1", "params": {"alpha": 0.1, "beta": 0.1}},
            ]
        },
        {
            "name": "3_All_History_Optional_Varied",
            "signal_condition": SignalCondition.OPTIONAL_SIGNAL,
            "runs_per_setup": 5,
            "max_rounds": 50000,
            "agent_configs": [
                {"strategy_type": Strategy.HISTORY_BASED, "name": "HistAgent_A", "params": {"pseudo_count": 1.0, "learning_step_follow": 0.3}},
                {"strategy_type": Strategy.HISTORY_BASED, "name": "HistAgent_B", "params": {"pseudo_count": 3.0, "learning_step_follow": 0.7}},
                {"strategy_type": Strategy.HISTORY_BASED, "name": "HistAgent_C"}, # Uses defaults
            ]
        },
        {
            "name": "4_Mixed_NoSignal",
            "signal_condition": SignalCondition.NO_SIGNAL,
            "runs_per_setup": 3,
            "max_rounds": 30000,
            "agent_configs": [
                {"strategy_type": Strategy.HISTORY_BASED, "name": "H1"},
                {"strategy_type": Strategy.REWARD_BASED, "name": "R1"},
                {"strategy_type": Strategy.HISTORY_BASED, "name": "H2", "params": {"pseudo_count": 0.5}},
                {"strategy_type": Strategy.REWARD_BASED, "name": "R2", "params": {"alpha": 0.3}},
            ]
        }
    ]
    
    results = run_all_scenarios(
        experiment_setups=experiment_setups_example,
        default_runs_per_setup=10, # Default if not specified in setup
        default_max_rounds=100000
    )
    
    print("\nPlotting results (example)...")
    plot_results(results) # Will use the basic bar plot for now
    
    print("\nSimulation examples complete!")


if __name__ == "__main__":
    main() 