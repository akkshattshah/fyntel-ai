import requests
from bs4 import BeautifulSoup

def get_screener_data(stock_symbol):
    """
    Fetches financial data from Screener.in for the given stock symbol.
    """
    url = f"https://www.screener.in/company/{stock_symbol}/"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract key financial data
        data = {}
        
        # Example: Fetching market cap
        market_cap_element = soup.find("span", string="Market Cap")
        if market_cap_element:
            data["Market Cap"] = market_cap_element.find_next("span").text.strip()
        
        # Example: Fetching P/E Ratio
        pe_ratio_element = soup.find("span", string="P/E")
        if pe_ratio_element:
            data["P/E Ratio"] = pe_ratio_element.find_next("span").text.strip()
        
        # Extract other key financials dynamically
        financials_section = soup.find("section", class_="company-ratios")
        if financials_section:
            for row in financials_section.find_all("li"):
                key = row.find("span").text.strip()
                value = row.find("span", class_="number").text.strip()
                data[key] = value
        
        if not data:
            return "No financial data found."
        
        return data
    
    except requests.exceptions.RequestException as e:
        return f"Error fetching data: {e}"
