from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END

# 1. State Definition
class AgentState(TypedDict):
    client_id: str
    portfolio_assets: List[Dict[str, Any]]
    market_data: Dict[str, Any]
    risk_metrics: Dict[str, Any]
    final_report: str
    compliance_status: str 

# 2. Node Imports (Ensure these names exist in your node files!)
from .nodes.fetch_crm import fetch_crm
from .nodes.fetch_market import node_fetch_market_data
from .nodes.analyze_risk import node_analyze_risk
from .nodes.generate_report import generate_report
from .nodes.save_draft import node_save_draft

# 3. Graph Logic
def build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("fetch_portfolio", fetch_crm)
    workflow.add_node("fetch_market", node_fetch_market_data)
    workflow.add_node("analyze_risk", node_analyze_risk)
    workflow.add_node("generate_report", generate_report)
    workflow.add_node("save_draft", node_save_draft)

    workflow.set_entry_point("fetch_portfolio")
    workflow.add_edge("fetch_portfolio", "fetch_market")
    workflow.add_edge("fetch_market", "analyze_risk")
    workflow.add_edge("analyze_risk", "generate_report")
    workflow.add_edge("generate_report", "save_draft")
    workflow.add_edge("save_draft", END)

    return workflow.compile()

app = build_graph()