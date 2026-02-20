import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

class StressTester:
    def __init__(self):
        # Define Historical and Hypothetical Scenarios
        # Values represent expected market shock per asset class (equities broadly)
        self.scenarios = {
            "2008_Financial_Crisis": {"equity_drop": -0.50, "bond_change": 0.10, "prob": 0.05},
            "Dot_Com_Crash_Tech": {"equity_drop": -0.40, "bond_change": 0.05, "prob": 0.05},
            "Severe_Inflation_Spike": {"equity_drop": -0.25, "bond_change": -0.15, "prob": 0.20},
            "Sudden_Rate_Hike": {"equity_drop": -0.15, "bond_change": -0.10, "prob": 0.30},
        }

    def run_stress_test(self, portfolio_assets: list, total_value: float = 1000000) -> dict:
        """
        Runs predefined shock scenarios against a portfolio.
        Assume total_value is 1M if not provided.
        """
        results = {}
        expected_loss = 0
        
        # Calculate rough equity/bond split
        equity_weight = sum([p['quantity'] for p in portfolio_assets if p.get('asset_type', 'equity') == 'equity'])
        bond_weight = sum([p['quantity'] for p in portfolio_assets if p.get('asset_type', 'equity') in ['bond', 'bond_etf']])
        
        total_qty = equity_weight + bond_weight if (equity_weight + bond_weight) > 0 else 1
        pct_equity = equity_weight / total_qty
        pct_bond = bond_weight / total_qty

        for name, params in self.scenarios.items():
            # Calculate shock
            equity_hit = pct_equity * params["equity_drop"]
            bond_hit = pct_bond * params["bond_change"]
            
            total_shock_pct = equity_hit + bond_hit
            dollar_loss = total_value * total_shock_pct
            
            results[name] = {
                "impact_pct": round(total_shock_pct, 4),
                "potential_loss_usd": round(dollar_loss, 2),
                "probability": params["prob"],
                "risk_rating": "Severe" if total_shock_pct < -0.3 else "Moderate" if total_shock_pct < -0.1 else "Low"
            }
            
            expected_loss += (dollar_loss * params["prob"])

        # Mitigation logic
        recommendations = []
        if pct_equity > 0.8:
            recommendations.append("High equity concentration detected. Consider rebalancing into fixed income to survive rate hikes.")
        if expected_loss < -50000:
            recommendations.append("Probability-weighted loss exceeds $50k. Explore downside protection via put options.")

        return {
            "scenarios": results,
            "weighted_expected_loss": round(expected_loss, 2),
            "mitigation_recommendations": recommendations or ["Portfolio appears adequately diversified."]
        }
