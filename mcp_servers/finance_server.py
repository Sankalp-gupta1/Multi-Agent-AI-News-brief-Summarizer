import requests


def get_finance(market="global"):
    try:
        market = market.lower()

        if market == "india":
            symbol = "^NSEI"
            index_name = "NIFTY 50"

        elif market == "usa":
            symbol = "^GSPC"
            index_name = "S&P 500"

        elif market == "crypto":
            symbol = "BTC-USD"
            index_name = "Bitcoin"

        else:
            symbol = "^DJI"
            index_name = "Dow Jones"

        url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}"
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return {"error": "Finance API error."}

        data = response.json()
        results = data.get("quoteResponse", {}).get("result", [])

        if not results:
            return {"error": "Finance data not available."}

        result = results[0]

        return {
            "index": index_name,
            "price": result.get("regularMarketPrice", "N/A"),
            "change": f"{result.get('regularMarketChangePercent', 'N/A')}%",
            "status": result.get("marketState", "N/A")
        }

    except Exception as e:
        return {"error": str(e)}


# import requests

# def get_finance():
#     try:
#         url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=%5ENSEI"
#         response = requests.get(url)

#         if response.status_code != 200:
#             return "Finance API error."

#         data = response.json()
#         results = data.get("quoteResponse", {}).get("result", [])

#         if not results:
#             return "Finance data not available."

#         price = results[0].get("regularMarketPrice", "N/A")

#         return f"NIFTY Current Value: {price}"

#     except Exception as e:
#         return f"Finance API Error: {str(e)}"
