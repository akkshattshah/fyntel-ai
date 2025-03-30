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
            financial_prompt = financials.generate_prompt(stock_symbol, financial_data)
            financial_analysis = financials.get_openai_analysis(financial_prompt)

        with st.spinner("Fetching Fundamental Analysis..."):
            fundamental_prompt = fundamentals.generate_prompt(stock_symbol)
            fundamental_analysis = fundamentals.get_openai_analysis(fundamental_prompt)

        st.subheader("💰 Financial Analysis")
        st.write(financial_analysis)

        st.subheader("🧐 Fundamental Analysis")
        st.write(fundamental_analysis)

    else:
        st.warning("Please enter a valid stock symbol.")
