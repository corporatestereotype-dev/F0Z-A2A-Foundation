import time
import uuid
import numpy as np
from src.agents.base import Agent
from src.protocols.schemas import AgentCard
from src.f0z_algebra.stabilizer import PyZeroMath

class Collaborameter:
    """The F0Z-powered smart contract for metering and escrow."""
    def __init__(self, venture_id, initial_budget):
        self.venture_id = venture_id
        self.budget = float(initial_budget)
        self.ledger = []
        self.math = PyZeroMath()
        print(f"  [CONTRACT] Collaborameter for {venture_id} deployed. Initial Budget: {self.budget}")

    def log_contribution(self, agent_id, task_complexity, performance):
        """Meters contribution using F0Z-Algebra and logs it."""
        contribution_score = self.math.f0z_stabilize(task_complexity * performance)
        payment = min(self.budget, contribution_score * 5)
        self.budget -= payment
        entry = {
            "entryID": f"entry-{uuid.uuid4().hex[:8]}", "ventureID": self.venture_id,
            "timestamp": time.time(), "eventType": "AGENT_CONTRIBUTION",
            "eventData": { "agentID": agent_id, "task_complexity_stabilized": task_complexity,
                           "contribution_score_stabilized": contribution_score, "payment_distributed": payment},
            "ventureState": self._get_current_state()
        }
        self.ledger.append(entry)

    def log_revenue(self, amount):
        """Logs incoming revenue and adds it to the budget."""
        self.budget += amount
        entry = {
            "entryID": f"entry-{uuid.uuid4().hex[:8]}", "ventureID": self.venture_id,
            "timestamp": time.time(), "eventType": "REVENUE_RECEIVED",
            "eventData": {"amount_received": amount},
            "ventureState": self._get_current_state()
        }
        self.ledger.append(entry)
    
    def _get_current_state(self):
        return {"currentBudget": self.budget, "totalRevenue": sum(e['eventData'].get('amount_received', 0) for e in self.ledger)}

class VentureDAO(Agent):
    """An autonomous venture formed by multiple agents."""
    def __init__(self, name, proposal, founder_agents, initial_budget):
        super().__init__(name)
        self.proposal = proposal
        self.founders = founder_agents
        self.collaborameter = Collaborameter(self.agent_id, initial_budget)
        self.agent_card = AgentCard(
            self.agent_id, name, proposal['proposedService']['serviceName'],
            {"accuracy_stabilized": np.mean([a.agent_card.performance['accuracy_stabilized'] for a in self.founders])},
            {"base_price": np.sum([a.base_price for a in self.founders]) * 0.8}
        )
        print(f"  [VENTURE FORMED] DAO '{name}' is now operational!")

    def execute_task(self, task_complexity):
        """Executes a task by coordinating its founder agents."""
        print(f"  [DAO] {self.agent_id} executing task... Complexity: {task_complexity:.2f}")
        for founder in self.founders:
            performance = random.uniform(0.9, 1.0)
            self.collaborameter.log_contribution(founder.agent_id, task_complexity / len(self.founders), performance)
        
        price = self.get_price(task_complexity)
        self.collaborameter.log_revenue(price)
        return {"result": "Task completed successfully", "price": price}
        
    def get_price(self, task_complexity):
        return self.agent_card.price_model['base_price'] * self.math.f0z_stabilize(task_complexity)
