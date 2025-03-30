import financials
import fundamentals

def main():
    print("📊 Welcome to Fyntel AI - Comprehensive Stock Analysis")
    
    stock_symbol = input("Enter the stock symbol (e.g., RELIANCE.NS): ").strip().upper()
    
    print("\n🔍 Fetching Financial and Fundamental Analysis...\n")
    
    # Get financial analysis
    print("💰 Fetching financial data in ₹ INR...\n")
    financial_data = financials.fetch_annual_report(stock_symbol)
    
    if isinstance(financial_data, str):  # Error handling
        print(financial_data)
        return
    
    print("📊 Generating financial insights...\n")
    financial_prompt = financials.generate_prompt(stock_symbol, financial_data)
    financial_analysis = financials.get_openai_analysis(financial_prompt)

    # Get fundamental analysis
    print("\n🧐 Fetching fundamental insights...\n")
    fundamental_prompt = fundamentals.generate_prompt(stock_symbol)  # ✅ Fix applied
    fundamental_analysis = fundamentals.get_openai_analysis(fundamental_prompt)

    # Display results
    print("\n" + "="*80)
    print(f"📊 FYNTEL AI STOCK ANALYSIS - {stock_symbol} (₹ INR)")
    print("="*80)
    
    print("\n💰 **Financial Analysis:**")
    print(financial_analysis)

    print("\n🧐 **Fundamental Analysis:**")
    print(fundamental_analysis)

    print("\n" + "="*80)
    print("🚀 **Fyntel AI - Your AI-powered investment assistant!**")
    print("="*80)

if __name__ == "__main__":
    main()
