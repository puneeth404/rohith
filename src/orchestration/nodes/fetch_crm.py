import logging
from typing import Any

logger = logging.getLogger(__name__)

def fetch_crm(state: dict[str, Any]) -> dict[str, Any]:
    """Retrieve the client's portfolio holdings from the local vault."""
    client_id = state.get("client_id", "Unknown")
    print(f"--- FETCHING PORTFOLIO FOR {client_id} (LOCAL CRM VAULT) ---")
    
    # Secure Local Vault data for development
    portfolio_assets = [
        {"ticker": "AAPL", "quantity": 150, "asset_type": "equity"},
        {"ticker": "MSFT", "quantity": 200, "asset_type": "equity"},
        {"ticker": "GOOGL", "quantity": 100, "asset_type": "equity"},
        {"ticker": "AMZN", "quantity": 80, "asset_type": "equity"},
        {"ticker": "BND", "quantity": 500, "asset_type": "bond_etf"},
    ]
    
    return {"portfolio_assets": portfolio_assets}