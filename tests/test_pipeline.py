import pytest
from src.orchestration.supervisor_graph import app
from src.orchestration.nodes.fetch_crm import fetch_crm

def test_fetch_crm_mock():
    # Test state management
    initial_state = {"client_id": "TEST_001"}
    result = fetch_crm(initial_state)
    assert "portfolio_assets" in result
    assert len(result["portfolio_assets"]) > 0

def test_pipeline_missing_client():
    initial_state = {
        "client_id": "",
        "portfolio_assets": [],
        "market_data": {},
        "risk_metrics": {},
        "final_report": "",
        "compliance_status": "Processing..."
    }
    # It should still run and handle empty gracefully through the nodes
    final_state = app.invoke(initial_state)
    assert "final_report" in final_state
    assert final_state["compliance_status"] == "✅ Approved & Saved to Client File"

def test_pipeline_graph_structure():
    # Verify nodes and edges compile
    assert app is not None
