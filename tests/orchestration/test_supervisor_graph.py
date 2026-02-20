import pytest
from unittest.mock import patch

def test_compliance_firewall():
    from src.orchestration.nodes.save_draft import node_save_draft
    state = {"final_report": "Test Report", "client_id": "123"}
    result = node_save_draft(state)
    assert result["compliance_status"] == "Pending Review"

def test_openbb_api_failure():
    from src.orchestration.nodes.fetch_market import node_fetch_market_data
    state = {"portfolio_assets": [{"ticker": "AAPL"}]}
    with patch("httpx.post", side_effect=Exception("API Down")):
        result = node_fetch_market_data(state)
    assert "error" in result

def test_empty_portfolio():
    from src.orchestration.nodes.analyze_risk import node_analyze_risk
    state = {"portfolio_assets": [], "market_data": {}}
    result = node_analyze_risk(state)
    assert result["risk_metrics"]["cvar"] == 0
