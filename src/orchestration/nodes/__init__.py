"""
Pipeline node functions for the wealth management supervisor graph.
"""

from .fetch_crm import fetch_crm
from .fetch_market import node_fetch_market_data
from .analyze_risk import node_analyze_risk
from .generate_report import generate_report
from .save_draft import node_save_draft

__all__ = [
    "fetch_crm",
    "node_fetch_market_data",
    "node_analyze_risk",
    "generate_report",
    "node_save_draft",
]
