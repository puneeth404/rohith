# Ivy AI Wealth Advisor - V2 UPGRADE GUIDE

Welcome to Ivy V2! This major release transforms the system from a simple LangGraph POC into a robust, enterprise-grade wealth orchestration platform.

## New Feature Highlights

### 1. Machine Learning Predictions (`src/models/ml_predictor.py`)
We have integrated a RandomForest Regressor to generate forward-looking return probabilities based on volatility and macro factors. 
- **Usage:** Included automatically if `ENABLE_ML=true` in your `.env`.

### 2. FinBERT Sentiment Analysis (`src/models/sentiment_analyzer.py`)
Provides realtime sentiment scores (Bullish/Bearish/Neutral) by crawling top news articles for each ticker in the client's portfolio.

### 3. Stress Testing Engine (`src/models/stress_tester.py`)
Simulates the portfolio's expected performance during historic and hypothetical shocks (e.g., 2008 Financial Crisis, Sudden Rate Hikes).

### 4. PDF Compliance Generation (`src/utils/pdf_generator.py`)
Generates beautiful, styled, compliance-ready PDFs from the AI's Markdown output using `WeasyPrint`. Includes all required client headers and regulatory footers.

### 5. Multi-Client Peer Comparison (`src/comparison/client_comparator.py`)
Advisors can now view multiple clients side-by-side to understand relative Sharpe ratios, CVaR rankings, and identify the safest portfolios.

### 6. Production Resilience
- **LLM Rate Limit Handling:** Exponential backoff added via `@llm_retry` in `generate_report.py`.
- **Database Connection Leaks:** Fixed via a `get_db_connection()` context manager.
- **Async Market Data:** Faster `yfinance` fetching using `asyncio.gather` for parallel requests.

## Deployment Changes
You can now deploy this instantly via Docker:
```bash
docker-compose up -d --build
```
This spins up the Streamlit app behind an Nginx reverse proxy, automatically mapping your `logs/` and `models/` folders to persistent volumes.
