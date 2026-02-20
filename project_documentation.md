# 🏦 Project Ivy: AI Wealth Advisor - Deep Dive Documentation

This document provides a comprehensive, end-to-end explanation of the **Ivy AI Wealth Advisor** project. It is designed to help you onboard teammates, explain the system architecture, and understand the technical decisions made during development.

---

## 1. Project Vision & Overview
**Project Ivy** is an enterprise-grade fintech application that leverages Agentic AI (via LangGraph) to automate wealth management analysis. Given a Client ID, it securely retrieves their portfolio, fetches real-time market data, computes advanced risk metrics (CVaR, Drawdown), and uses an LLM (Google Gemini) to generate a professional, compliance-ready wealth strategy report. 

The system features two user interfaces:
1. **A Streamlit Web Dashboard** (`app.py`) for financial advisors.
2. **A Command Line Interface** (`main.py`) for backend executions and testing.

---

## 2. Core Architecture & Tech Stack
The project is built on a modern, Python-based AI stack:

- **Language:** Python 
- **Orchestration Engine:** [LangGraph](https://python.langchain.com/docs/langgraph) (to manage the state and flow of the AI pipeline).
- **AI/LLM Engine:** Google Gemini (`gemini-2.5-flash`) via `langchain-google-genai`.
- **Frontend / UI:** [Streamlit](https://streamlit.io/) with custom CSS for a white-labeled, enterprise look.
- **Data & Math:** `pandas` and `numpy` for quantitative risk calculations.
- **Market Data Provider:** `yfinance` API for real-time stock histories.
- **Extensibility:** Pre-configured `mcp.json` pointing to an OpenBB Data Server via Model Context Protocol (MCP), showing a forward-looking design for scaling data integrations.

---

## 3. The LangGraph Pipeline (The "Brain")
The core of Project Ivy is a state machine defined in `src/orchestration/supervisor_graph.py`. LangGraph guarantees a reliable, predictable execution flow.

### A. The State (`AgentState`)
Data moves between nodes through a shared memory dictionary called the State. It holds:
- `client_id` (str): The requested client.
- `portfolio_assets` (list): The assets they own.
- `market_data` (dict): Real-time pricing data.
- `risk_metrics` (dict): Calculated financial risk.
- `final_report` (str): The Markdown output from the AI.
- `compliance_status` (str): Status of the report saving process.

### B. The Nodes (The Pipeline Steps)
The execution flows strictly through 5 sequential nodes:

1. **`fetch_portfolio` (`fetch_crm.py`)** 
   - **Role:** Simulates pulling client holdings from a secure CRM vault. 
   - **Action:** Currently returns a mocked portfolio of equities and bonds (AAPL, MSFT, GOOGL, AMZN, BND).

2. **`fetch_market` (`fetch_market.py`)**
   - **Role:** Obtains live pricing data to ensure the analysis is current.
   - **Action:** Loops through the portfolio tickers, uses `yfinance` to download 1-year historical pricing (Open, High, Low, Close), and saves it to the state.

3. **`analyze_risk` (`analyze_risk.py`)**
   - **Role:** The Quants Engine. 
   - **Action:** Converts the historical prices into daily percentage returns using `pandas.pct_change()`. It then uses `numpy` to calculate advanced metrics:
     - **CVaR (95%):** Conditional Value at Risk (Expected tail loss).
     - **Max Drawdown:** The largest peak-to-trough drop.
     - **Sharpe Ratio:** Risk-adjusted return.

4. **`generate_report` (`generate_report.py`)**
   - **Role:** The AI Synthesizer.
   - **Action:** Instantiates the Gemini 2.5 Flash model. It injects the `portfolio`, `market_data`, and `risk_metrics` into a highly specific prompt instructing the AI to act as a Wealth Advisor. The LLM returns a structured Markdown document.

5. **`save_draft` (`save_draft.py`)**
   - **Role:** Compliance and Finalization.
   - **Action:** Mocks an API call to save the generated report into a CRM (like Salesforce) and updates the `compliance_status` to Approved.

---

## 4. The Frontend Dashboard (`app.py`)
To make this powerful backend accessible to advisors, we built a Streamlit application. **Key Development Highlights:**

- **Critical Fix - Environment Loading:** `load_dotenv()` is called at the *very top* of the file (before importing LangGraph). This was a critical fix to ensure the `GOOGLE_API_KEY` is loaded into memory before the Gemini client initializes in the graph.
- **Enterprise Visuals:** We injected custom HTML/CSS to hide the default Streamlit header/footer (white-labeling) and applied "glassmorphic" styling to the metric cards.
- **Dynamic Checkpoints (`st.status`):** Instead of a generic loading spinner, the UI blocks execution inside an `st.status` container, visually updating the user ("Connecting to CRM...", "Running Risk Engine...") while `app.invoke()` runs in the background.
- **Tabbed Architecture:** The output is split into two `st.tabs`: 
   - *Executive Report:* Clean Markdown generation for the client.
   - *System Logic:* Exposes the JSON dictionary of portfolio and market data for developer/advisor debugging.
- **Human-in-the-Loop:** Features an "Approve & Save" button to represent the final human sign-off required in financial compliance workflows.

---

## 5. Development Hurdles Overcome
When explaining this to the team, it's worth noting the complex dependency management we resolved:
- **Pandas / Streamlit Conflict:** Streamlit currently requires `pandas < 3.0`. We encountered Windows file locks (`[WinError 5] Access is denied`) on the `__pycache__` inside our `.venv`. 
- **The Fix:** We had to manually force-clear the locked cache directories and explicitly command `python -m pip install "pandas<3" streamlit` directly into the `.venv` to ensure environmental purity.

---

## 6. How to Demo to the Team
To show this off to your teammates:
1. Ensure your `.env` contains a valid `GOOGLE_API_KEY`.
2. Activate your environment: `.\.venv\Scripts\activate`
3. Option A (UI): Run `streamlit run app.py` and click "Generate Wealth Report".
4. Option B (Terminal): Run `python main.py --client PUNEETH_001` to view the raw chronological execution in colored text.
