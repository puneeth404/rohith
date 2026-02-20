# Ivy AI V2 - API Reference

This document outlines the interfaces for the new V2 modules.

## `src.models.sentiment_analyzer.SentimentAnalyzer`
Analyzes financial sentiment using the HuggingFace `ProsusAI/finbert` model.
*   `fetch_news(ticker: str) -> list`: Gets recent news from yfinance.
*   `analyze_ticker(ticker: str) -> dict`: Returns `{"sentiment": "Bullish", "score": 0.8, "articles_analyzed": 5}`.
*   `analyze_portfolio(portfolio: list) -> dict`: Aggregates sentiment across all held assets.

## `src.models.ml_predictor.MLPredictor`
RandomForest regression model for predicting short-term returns.
*   `predict_returns(current_features: np.ndarray) -> dict`: Returns expected return and 95% confidence intervals.
*   `get_feature_importance() -> dict`: Returns the relative importance of Volatility, Trailing Return, and Macro Factors.

## `src.models.stress_tester.StressTester`
Calculates expected losses based on historical crises.
*   `run_stress_test(portfolio_assets: list, total_value: float) -> dict`: Simulates 4 macro shocks and returns the probability-weighted expected loss and mitigation recommendations.

## `src.comparison.client_comparator.ClientComparator`
Cross-client analytics engine.
*   `compare_clients(client_data_list: list) -> dict`: Ranks clients by Sharpe ratio and Risk (CVaR).

## `src.utils.pdf_generator.generate_wealth_pdf`
*   `generate_wealth_pdf(markdown_text: str, client_id: str) -> str`: Converts raw markdown to a formatted PDF. Returns the file path of the generated PDF.

## `src.utils.batch_processor.process_client_batch`
*   `process_client_batch(client_ids: list, max_workers: int = 4) -> dict`: Invokes the LangGraph pipeline concurrently across multiple clients using `ThreadPoolExecutor`.
