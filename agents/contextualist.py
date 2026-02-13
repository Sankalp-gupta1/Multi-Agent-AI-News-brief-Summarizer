from mcp_servers.weather_server import get_weather
from mcp_servers.news_server import get_news
from mcp_servers.finance_server import get_finance

def gather_context():
    return {
        "weather": get_weather(),
        "news": get_news(),
        "finance": get_finance()
    }
