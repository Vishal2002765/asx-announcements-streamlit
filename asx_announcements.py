import streamlit as st
import requests

# Function to fetch announcements
def fetch_announcements(company_code):
    url = f"https://www.asx.com.au/asx/1/company/{company_code}/announcements?count=20&market_sensitive=false"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        st.error(f"Failed to retrieve data for {company_code}: {response.status_code}")
        return []

# Function to check for "Trading Halt" announcements
def check_trading_halt(announcements):
    for announcement in announcements:
        if "Trading Halt" in announcement['header']:
            return True
    return False

# Streamlit app
st.title("ASX Company Announcements")

# List of company codes
company_codes = ["AEE", "REZ", "1AE", "1MC", "NRZ"]

# Dropdown menu for selecting company code
selected_company = st.selectbox("Select Company Code", company_codes)

if selected_company:
    st.header(f"Announcements for {selected_company}")
    announcements = fetch_announcements(selected_company)
    
    if announcements:
        for announcement in announcements:
            st.subheader(announcement['header'])
            st.write(f"**ID:** {announcement['id']}")
            st.write(f"**Release Date:** {announcement['document_release_date']}")
            st.write(f"**Document Date:** {announcement['document_date']}")
            st.write(f"**URL:** Link")
            st.write(f"**Market Sensitive:** {announcement['market_sensitive']}")
            st.write(f"**Number of Pages:** {announcement['number_of_pages']}")
            st.write(f"**Size:** {announcement['size']}")
            st.write(f"**Issuer Code:** {announcement['issuer_code']}")
            st.write(f"**Issuer Short Name:** {announcement['issuer_short_name']}")
            st.write(f"**Issuer Full Name:** {announcement['issuer_full_name']}")
            st.write("---")
    else:
        st.write("No announcements found.")

# Check for "Trading Halt" announcements
st.header("Tickers with 'Trading Halt' Announcements")
trading_halt_tickers = []

for company_code in company_codes:
    announcements = fetch_announcements(company_code)
    if check_trading_halt(announcements):
        trading_halt_tickers.append(company_code)

if trading_halt_tickers:
    st.write("The following tickers have 'Trading Halt' announcements:")
    for ticker in trading_halt_tickers:
        st.write(f"- {ticker}")
else:
    st.write("No tickers with 'Trading Halt' announcements found.")

