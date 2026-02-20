import yfinance as yf

def node_fetch_market_data(state):
    print("--- FETCHING REAL MARKET DATA (YAHOO FINANCE) ---")
    portfolio = state.get("portfolio_assets", [])
    
    if not portfolio:
        return {"market_data": {}}

    market_data = {}
    try:
        for asset in portfolio:
            ticker = asset.get("ticker")
            if not ticker:
                continue
            
            stock = yf.Ticker(ticker)
            history = stock.history(period="1y")
            
            prices = []
            for date, row in history.iterrows():
                prices.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "close": float(row["Close"]),
                    "high": float(row["High"]),
                    "low": float(row["Low"])
                })
            
            market_data[ticker] = prices
            
        return {"market_data": market_data}
        
    except Exception as e:
        return {"error": f"Yahoo Finance Error: {str(e)}"}