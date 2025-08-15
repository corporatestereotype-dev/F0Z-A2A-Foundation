import uuid
import random

class AgentCard:
    """Represents the AgentCard.json schema."""
    def __init__(self, agent_id, agent_name, capability_name, performance, price_model):
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.capability_name = capability_name
        self.performance = performance
        self.price_model = price_model
        self.reputation = 0.5  # Start with a neutral reputation

    def to_dict(self):
        return {
            "agentID": self.agent_id,
            "agentName": self.agent_name,
            "capabilities": [{"capabilityName": self.capability_name, "performanceMetrics": self.performance}],
            "pricingModel": {"type": "dynamic_f0z", "details": self.price_model},
            "reputation": {"score_stabilized": self.reputation, "confidence_epsilon": 1e-4}
        }
