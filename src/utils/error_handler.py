import time
import logging
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = logging.getLogger(__name__)

class IvyError(Exception):
    """Base exception for Ivy ecosystem."""
    pass

class MarketDataError(IvyError):
    pass

class LLMRateLimitError(IvyError):
    pass

class DatabaseConnectionError(IvyError):
    pass

def handle_rate_limit(retry_state):
    logger.warning(f"Rate limited. Retrying... Attempt {retry_state.attempt_number}")

# Retry decorator for LLM calls
llm_retry = retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=4, max=60),
    retry=retry_if_exception_type(Exception),
    after=handle_rate_limit
)

def graceful_fallback(fallback_value):
    """Decorator to return a fallback value upon failure."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error in {func.__name__}: {str(e)}. Using fallback.")
                return fallback_value
        return wrapper
    return decorator
