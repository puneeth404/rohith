import logging
import os
from typing import Any
from langchain_google_genai import ChatGoogleGenerativeAI
from src.utils.error_handler import llm_retry

logger = logging.getLogger(__name__)

# --- FIX 5: LLM Rate Limiting Handler ---
@llm_retry
def _call_llm_with_retry(llm, prompt):
    """Wrapped LLM call to handle HTTP 429 status codes transparently."""
    return llm.invoke(prompt)

def generate_report(state: dict[str, Any]) -> dict[str, Any]:
    """Generate a structured Markdown wealth management report using Google Gemini."""
    logger.info("generate_report: building report for client %s", state["client_id"])
    print("--- GENERATING REAL AI REPORT (GOOGLE GEMINI) ---")
    
    client_id = state.get("client_id", "Unknown")
    portfolio = state.get("portfolio_assets", [])
    market = state.get("market_data", {})
    risk = state.get("risk_metrics", {})

    try:
        # Wake up the Gemini Brain
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            api_key=os.getenv("GOOGLE_API_KEY")
        )
        
        prompt = f"""
        You are an expert Wealth Advisor. Write a professional wealth management report in Markdown for Client: {client_id}.
        
        Here is their portfolio data: {portfolio}
        Here is their risk analysis: {risk}
        Here is the recent market data: {market}
        
        Format the report beautifully with headings, bullet points, and an executive summary. 
        Analyze their market performance and risk metrics to provide a brief 1-paragraph insight. 
        Do not include any placeholders. Be concise and professional. Conclude with a standard financial disclaimer.
        """
        
        # Use our new resilient retry wrapper
        response = _call_llm_with_retry(llm, prompt)
        final_report = response.content
        
    except Exception as e:
        logger.error(f"AI Generation Error: {str(e)}")
        final_report = f"AI Generation Error: {str(e)}"

    logger.info("generate_report: completed — %d characters", len(final_report))
    return {"final_report": final_report}