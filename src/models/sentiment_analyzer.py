import yfinance as yf
from transformers import pipeline
import logging

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    def __init__(self):
        try:
            # Load FinBERT for financial sentiment analysis
            self.nlp = pipeline("sentiment-analysis", model="ProsusAI/finbert")
            logger.info("FinBERT model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load FinBERT: {e}")
            self.nlp = None

    def fetch_news(self, ticker: str) -> list:
        try:
            stock = yf.Ticker(ticker)
            return stock.news or []
        except Exception as e:
            logger.error(f"Failed fetching news for {ticker}: {e}")
            return []

    def analyze_ticker(self, ticker: str) -> dict:
        if not self.nlp:
            return {"sentiment": "neutral", "score": 0.0, "articles_analyzed": 0}
            
        news = self.fetch_news(ticker)
        if not news:
            return {"sentiment": "neutral", "score": 0.0, "articles_analyzed": 0}
            
        texts = [article.get('title', '') for article in news][:5] # Analyze top 5 recent headlines
        
        try:
            results = self.nlp(texts)
            scores = []
            for r in results:
                if r['label'] == 'positive':
                    scores.append(r['score'])
                elif r['label'] == 'negative':
                    scores.append(-r['score'])
                else:
                    scores.append(0)
                    
            avg_score = sum(scores) / len(scores) if scores else 0
            
            if avg_score > 0.15:
                label = "Bullish"
            elif avg_score < -0.15:
                label = "Bearish"
            else:
                label = "Neutral"
                
            return {
                "sentiment": label,
                "score": round(avg_score, 3),
                "articles_analyzed": len(texts)
            }
        except Exception as e:
            logger.error(f"Sentiment analysis failed for {ticker}: {e}")
            return {"sentiment": "error", "score": 0.0, "articles_analyzed": 0}

    def analyze_portfolio(self, portfolio: list) -> dict:
        results = {}
        market_score = 0
        
        for asset in portfolio:
            ticker = asset.get('ticker')
            if ticker:
                res = self.analyze_ticker(ticker)
                results[ticker] = res
                market_score += res['score']
                
        avg_market = market_score / len(portfolio) if portfolio else 0
        
        return {
            "assets": results,
            "market_wide_score": round(avg_market, 3),
            "market_sentiment": "Bullish" if avg_market > 0.1 else "Bearish" if avg_market < -0.1 else "Neutral"
        }
