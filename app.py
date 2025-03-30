import streamlit as st
import financials
import fundamentals



st.set_page_config(page_title="Fyntel AI - Stock Analysis", layout="wide")

st.title("📊 Fyntel AI - Stock Market Analyzer")
st.write("Enter a stock symbol to get a complete financial and fundamental analysis.")

# Input field for stock symbol
stock_symbol = st.text_input("Enter Stock Symbol (e.g., RELIANCE.NS)")

if st.button("Analyze"):
    if stock_symbol:
        with st.spinner("Fetching Financial Data..."):
            financial_data = financials.fetch_annual_report(stock_symbol)

            if financial_data:  # Ensure data is fetched before proceeding
                financial_prompt = financials.generate_prompt(stock_symbol, financial_data)
                if financial_prompt:  # Ensure prompt is generated
                    financial_analysis = financials.get_openai_analysis(financial_prompt)
                else:
                    financial_analysis = "⚠️ Error: Unable to generate financial prompt."
            else:
                financial_analysis = "⚠️ Error: No financial data available."

        with st.spinner("Fetching Fundamental Analysis..."):
            fundamental_prompt = fundamentals.generate_prompt(stock_symbol)
            if fundamental_prompt:  # Ensure prompt is generated
                fundamental_analysis = fundamentals.get_openai_analysis(fundamental_prompt)
            else:
                fundamental_analysis = "⚠️ Error: Unable to generate fundamental prompt."

        st.subheader("💰 Financial Analysis")
        st.write(financial_analysis)

        st.subheader("🧐 Fundamental Analysis")
        st.write(fundamental_analysis)

    else:
        st.warning("Please enter a valid stock symbol.")
