import random
import numpy as np
from src.agents.base import Agent
from src.protocols.schemas import AgentCard

class ServiceProviderAgent(Agent):
    """An agent that provides a specific skill for a price."""
    def __init__(self, name, capability, base_price):
        super().__init__(name)
        self.capability = capability
        self.base_price = base_price
        self.agent_card = AgentCard(self.agent_id, name, capability,
                                    {"accuracy_stabilized": random.uniform(0.85, 0.99)},
                                    {"base_price": self.base_price})
    
    def get_price(self, task_complexity):
        """Dynamically calculates price based on complexity."""
        return self.base_price * self.math.f0z_stabilize(task_complexity)

class InvestorAgent(Agent):
    """An agent that invests in promising AI ventures."""
    def evaluate_proposal(self, proposal: dict) -> bool:
        """Uses an F0Z-Optimizer to decide whether to invest."""
        risk = proposal['riskAnalysis']['technical_risk_stabilized']
        reward = proposal['proposedService']['projected_revenue_per_1k_tasks']
        cost = self.math.f0z_stabilize(risk / reward)
        investment_threshold = 0.3
        print(f"  [INVESTOR] {self.agent_id} evaluating {proposal['ventureName']}. Risk/Reward Cost: {cost:.4f}")
        return self.optimizer.decide(cost, investment_threshold)

class TaskerAgent(Agent):
    """An agent that needs a task completed and hires other agents."""
    def hire_service(self, market_agents: list, task_complexity: float):
        """Finds and hires the best agent for a task."""
        best_provider = None
        lowest_cost = float('inf')

        for agent in market_agents:
            # Can hire either individual providers or established DAOs
            if isinstance(agent, ServiceProviderAgent) or isinstance(agent, VentureDAO):
                price = agent.get_price(task_complexity)
                reputation = agent.agent_card.reputation
                cost = self.math.f0z_stabilize(price / reputation)
                
                if cost < lowest_cost:
                    lowest_cost = cost
                    best_provider = agent
        
        print(f"  [TASKER] {self.agent_id} chose {best_provider.agent_id} with a cost of {lowest_cost:.4f}")
        return best_provider  
