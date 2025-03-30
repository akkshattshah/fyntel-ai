import os
import openai
import yfinance as yf
import pandas as pd
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def fetch_annual_report(stock_symbol):
    """Fetch annual financial statements from Yahoo Finance (converted to ₹ INR)."""
    stock = yf.Ticker(stock_symbol)
    
    try:
        financials = stock.financials  # Annual financials
        balance_sheet = stock.balance_sheet  # Balance sheet
        cash_flow = stock.cashflow  # Cash flow statements
        
        # Convert all values to ₹ (assuming default values are in USD)
        exchange_rate = 83  # Approximate USD to INR conversion rate
        financials *= exchange_rate
        balance_sheet *= exchange_rate
        cash_flow *= exchange_rate

        # Convert data to readable format
        data = {
            "Income Statement": financials.to_string(),
            "Balance Sheet": balance_sheet.to_string(),
            "Cash Flow Statement": cash_flow.to_string()
        }
        return data
    except Exception as e:
        return f"❌ Error fetching data: {e}"

def generate_prompt(stock_symbol, financial_data):
    """Generates a detailed prompt for OpenAI GPT based on financial data in INR."""
    prompt = f"""
    Analyze the **annual financial report** of {stock_symbol} and provide insights on the company's performance.
    Focus on **revenue growth, profitability, liquidity, solvency, and cash flow trends**.
    
    **📊 Income Statement (₹ INR):**
    {financial_data['Income Statement']}
    
    **📑 Balance Sheet (₹ INR):**
    {financial_data['Balance Sheet']}
    
    **💰 Cash Flow Statement (₹ INR):**
    {financial_data['Cash Flow Statement']}
    
    **🔍 Provide an in-depth analysis on:**
    
    1️⃣ **Revenue & Profit Trends:**  
       - How have revenue and profits changed over the years?  
       - Key drivers behind growth or decline?  

    2️⃣ **Financial Ratios & Health:**  
       - Debt-to-Equity, Current Ratio, Profit Margins, etc.  
       - Are these ratios strong compared to financial standards?  

    3️⃣ **Cash Flow Sustainability:**  
       - Is free cash flow sufficient for growth and stability?  
       - Any concerns about liquidity or cash reserves?  

    4️⃣ **Risk Factors & Red Flags:**  
       - Major debts or financial obligations?  
       - Any unusual trends in expenses or liabilities?  

    5️⃣ **Investment Outlook:**  
       - Does the company show signs of **strong financial health**?  
       - What are the key strengths and areas for improvement?  
    """
    return prompt

def get_openai_analysis(prompt):
    """Fetches AI-generated financial analysis from OpenAI's GPT model."""
    if openai.api_key is None:
        return "❌ ERROR: OpenAI API Key not found. Check your .env file."
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a financial analyst."},
                  {"role": "user", "content": prompt}]
    )
    
    return response["choices"][0]["message"]["content"]

def main():
    stock_symbol = input("Enter the stock symbol (e.g., RELIANCE.NS): ").strip().upper()
    
    print("🔍 Fetching annual financial data in ₹ INR...")
    financial_data = fetch_annual_report(stock_symbol)
    
    if isinstance(financial_data, str):  # Error message case
        print(financial_data)
        return
    
    print("📊 Generating financial analysis...\n")
    prompt = generate_prompt(stock_symbol, financial_data)
    analysis = get_openai_analysis(prompt)
    
    print("\n" + "="*60)
    print(f"📊 FYNTEL FINANCIAL ANALYSIS - {stock_symbol} (₹ INR)")
    print("="*60)
    print(analysis)
    print("="*60)

if __name__ == "__main__":
    main()