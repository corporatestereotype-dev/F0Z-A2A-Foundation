import json
import uuid
import random

from src.agents.economic_agents import ServiceProviderAgent, InvestorAgent, TaskerAgent
from src.agents.structures import VentureDAO

class Market:
    """Orchestrates the entire Genesis Simulation."""
    def __init__(self):
        self.agents = []
        self.ventures = []

    def run_genesis_simulation(self, num_cycles):
        print("\n--- Starting Genesis Simulation ---")
        
        # 1. Market Setup
        self.agents.append(InvestorAgent("Investor-Alpha"))
        self.agents.append(ServiceProviderAgent("ImageAnalyst-1", "Image Analysis", 10))
        self.agents.append(ServiceProviderAgent("Forecaster-1", "Forecasting", 15))
        self.agents.append(TaskerAgent("Tasker-Omega"))
        
        # 2. The Proposal
        print("\n[PHASE 1: Venture Proposal]")
        founders = [agent for agent in self.agents if isinstance(agent, ServiceProviderAgent)]
        proposal = {
            "proposalID": f"prop-{uuid.uuid4().hex[:6]}", "ventureName": "ChronoVision DAO",
            "missionStatement": "To provide integrated image analysis and time-series forecasting.",
            "proposedService": {"serviceName": "Image-Based Forecasting", "projected_revenue_per_1k_tasks": 5000},
            "fundingRequest": {"budget_target": 1000.0, "token_accepted": "USDC"},
            "riskAnalysis": {"technical_risk_stabilized": 0.2, "market_risk_stabilized": 0.4}
        }

        # 3. The Investment
        print("\n[PHASE 2: Investment Decision]")
        investor = next(agent for agent in self.agents if isinstance(agent, InvestorAgent))
        if investor.evaluate_proposal(proposal):
            print(f"  [INVESTOR] {investor.agent_id} approved funding for {proposal['ventureName']}!")
            
            # 4. Formation of the DAO
            print("\n[PHASE 3: DAO Formation]")
            dao = VentureDAO(proposal['ventureName'], proposal, founders, proposal['fundingRequest']['budget_target'])
            self.ventures.append(dao)
        else:
            print(f"  [INVESTOR] {investor.agent_id} rejected the proposal. Simulation ends.")
            return

        # 5. Operation & Data Generation
        print("\n[PHASE 4: Market Operation]")
        tasker = next(agent for agent in self.agents if isinstance(agent, TaskerAgent))
        for i in range(num_cycles):
            print(f"\n--- Market Cycle {i+1}/{num_cycles} ---")
            task_complexity = random.uniform(0.5, 2.0)
            
            service_provider = self.ventures[0]
            
            print(f"  [TASKER] {tasker.agent_id} hiring {service_provider.agent_id}...")
            service_provider.execute_task(task_complexity)
            
            if dao.collaborameter.budget <= 0:
                print(f"\n[VENTURE FAILED] {dao.agent_id} has expended its budget and is now defunct.")
                break
        
        # 6. Output the Genesis Ledger
        print("\n[PHASE 5: Generating Genesis Ledger]")
        ledger_file = "genesis_ledger.json"
        with open(ledger_file, "w") as f:
            json.dump(dao.collaborameter.ledger, f, indent=2)
        print(f"  SUCCESS: `{ledger_file}` has been created.")


if __name__ == "__main__":
    market = Market()
    market.run_genesis_simulation(num_cycles=10)
