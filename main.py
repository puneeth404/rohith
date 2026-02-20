import argparse
import os
import warnings
from dotenv import load_dotenv
from colorama import init, Fore
from src.orchestration.supervisor_graph import app

# Suppress technical warnings for a clean UI
warnings.filterwarnings("ignore")
load_dotenv()

def run_pipeline(client_id):
    init(autoreset=True)
    print(Fore.CYAN + f"--- Starting Wealth Management Pipeline for Client: {client_id} ---")
    
    # 1. Initialize the State (Memory)
    initial_state = {
        "client_id": client_id,
        "portfolio_assets": [],
        "market_data": {},
        "risk_metrics": {},
        "final_report": "",
        "compliance_status": "Processing..." 
    }
    
    # 2. Run the LangGraph
    final_state = app.invoke(initial_state)
    
    # 3. Print the Final Results
    print(Fore.GREEN + "Success: Pipeline Execution Complete")
    print("\n" + "="*30)
    print(Fore.YELLOW + "FINAL WEALTH REPORT")
    print("="*30)
    print(final_state.get("final_report", "No report generated."))
    print("="*30)
    
    # 4. Show the dynamic Compliance Status
    status = final_state.get("compliance_status", "N/A")
    print(Fore.BLUE + f"Compliance Status: {status}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ivy Wealth Advisor CLI")
    parser.add_argument("--client", required=True, help="The ID of the client")
    args = parser.parse_args()
    run_pipeline(args.client)