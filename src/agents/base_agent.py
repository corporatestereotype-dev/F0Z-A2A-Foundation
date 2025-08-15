import uuid
from src.f0z_algebra.stabilizer import PyZeroMath, F0ZOptimizer

class Agent:
    """Base class for all agents in our economy."""
    def __init__(self, name):
        self.agent_id = f"{name}-{uuid.uuid4().hex[:6]}"
        self.math = PyZeroMath()
        self.optimizer = F0ZOptimizer(self.math)
        print(f"  [AGENT CREATED] {self.agent_id} ({self.__class__.__name__})")
