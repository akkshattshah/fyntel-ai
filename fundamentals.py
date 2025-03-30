import os
import openai
import yfinance as yf
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def fetch_company_info(stock_symbol):
    """Fetch company profile and key details from Yahoo Finance."""
    stock = yf.Ticker(stock_symbol)
    info = stock.info

    if not info:
        return None

    company_data = {
        "Company Name": info.get("longName", "N/A"),
        "Industry": info.get("industry", "N/A"),
        "Sector": info.get("sector", "N/A"),
        "CEO": info.get("companyOfficers", [{}])[0].get("name", "N/A"),
        "Market Cap": info.get("marketCap", "N/A"),
        "Business Summary": info.get("longBusinessSummary", "N/A"),
        "Headquarters": info.get("city", "N/A") + ", " + info.get("country", "N/A"),
    }
    
    return company_data

def generate_prompt(stock_symbol):
    """Generates a detailed prompt for OpenAI GPT based on qualitative aspects like leadership, vision, and expansion."""
    prompt = f"""
    Analyze the fundamental aspects of {stock_symbol}. Focus on leadership, vision, expansion plans, and competitive positioning.
    
    Provide insights on:
    1. **Leadership & Management** - Background of top executives, leadership style, and decision-making.
    2. **Company Vision & Strategy** - Long-term goals, market positioning, and core business strategy.
    3. **Expansion Plans** - Future growth strategies, mergers, acquisitions, and expansion into new markets.
    4. **Market Reputation** - Brand value, trustworthiness, and public perception.
    5. **Innovation & R&D** - Focus on innovation, technological advancements, and research spending.
    6. **ESG & Ethical Practices** - Environmental and social impact, governance, and sustainability efforts.
    
    Summarize the company’s qualitative strengths and weaknesses.
    """
    return prompt

def generate_qualitative_prompt(stock_symbol, company_data):
    """Generates a detailed prompt for OpenAI GPT based on qualitative data."""
    prompt = f"""
    Provide a **qualitative fundamental analysis** of {company_data['Company Name']} ({stock_symbol}).
    
    **📌 Key Areas to Cover:**
    
    1️⃣ **Leadership & Management:**  
       - Who is the CEO? What is their background and track record?  
       - Any notable executives or board members?  
       - How has leadership impacted company performance?  

    2️⃣ **Vision & Mission:**  
       - What are the company's long-term goals?  
       - Core philosophy & values that drive business decisions?  

    3️⃣ **Business Model & Competitive Edge:**  
       - How does the company make money? What are its revenue streams?  
       - Who are its biggest competitors? What makes it unique?  
       - Does it have a strong brand presence?  

    4️⃣ **Expansion & Future Strategy:**  
       - Is the company expanding into new markets?  
       - Any recent acquisitions or partnerships?  
       - How is the company investing in innovation?  

    5️⃣ **Risk Factors & Challenges:**  
       - Any major risks that could affect future growth?  
       - Are there any regulatory, geopolitical, or economic threats?  

    6️⃣ **Public Perception & Reputation:**  
       - How do customers and investors perceive the company?  
       - Has it faced any controversies or major issues in the past?  

    7️⃣ **Sustainability & ESG (Environmental, Social, Governance):**  
       - Does the company follow ethical business practices?  
       - Any notable sustainability initiatives?  

    **📍 Additional Info:**  
    - **Industry:** {company_data['Industry']}  
    - **Sector:** {company_data['Sector']}  
    - **Market Cap:** {company_data['Market Cap']}  
    - **Headquarters:** {company_data['Headquarters']}  
    - **Business Summary:** {company_data['Business Summary']}  
    """
    
    return prompt

def get_openai_analysis(prompt):
    """Fetches AI-generated qualitative analysis from OpenAI's GPT model."""
    if openai.api_key is None:
        return "❌ ERROR: OpenAI API Key not found. Check your .env file."
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a business analyst providing qualitative stock analysis."},
                  {"role": "user", "content": prompt}]
    )
    
    return response["choices"][0]["message"]["content"]

def main():
    stock_symbol = input("Enter the stock symbol (e.g., RELIANCE.NS): ").strip().upper()
    
    print("🔍 Fetching company fundamentals...")
    company_data = fetch_company_info(stock_symbol)
    
    if company_data is None:
        print("❌ Error: Could not fetch company information. The stock symbol might be incorrect or data is unavailable.")
        return
    
    print("📊 Generating qualitative analysis...\n")
    prompt = generate_qualitative_prompt(stock_symbol, company_data)
    analysis = get_openai_analysis(prompt)
    
    print("\n" + "="*60)
    print(f"📊 FYNTEL QUALITATIVE FUNDAMENTAL ANALYSIS - {company_data['Company Name']}")
    print("="*60)
    print(analysis)
    print("="*60)

if __name__ == "__main__":
    main()
