
import streamlit as st
import re
import requests
from bs4 import BeautifulSoup
from email_validator import validate_email, EmailNotValidError
import dns.resolver
import pandas as pd

EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

def search_google(query, num_results=10):
    headers = {'User-Agent': 'Mozilla/5.0'}
    links = []
    for start in range(0, num_results, 10):
        url = f"https://www.google.com/search?q={query}&start={start}"
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        for a in soup.find_all('a'):
            href = a.get('href')
            if href and '/url?q=' in href:
                clean_url = href.split('/url?q=')[1].split('&')[0]
                if 'google.com' not in clean_url:
                    links.append(clean_url)
    return links

def scrape_emails_from_url(url):
    try:
        res = requests.get(url, timeout=5)
        emails = re.findall(EMAIL_REGEX, res.text)
        return list(set(emails))
    except:
        return []

def validate_email_address(email):
    try:
        valid = validate_email(email)
        domain = valid.domain
        mx_records = dns.resolver.resolve(domain, 'MX')
        return True
    except (EmailNotValidError, dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return False

st.title("Email Scraper & Validator")
st.markdown("Search for emails by keyword and domain.")

query = st.text_input("Enter keywords or domain (e.g. site:harvard.edu contact):")
num_sites = st.slider("Number of search results to scan:", 10, 50, 20)

if st.button("Start Scraping") and query:
    with st.spinner("Searching and scraping emails..."):
        result_links = search_google(query, num_sites)
        email_data = []

        for link in result_links:
            emails = scrape_emails_from_url(link)
            for email in emails:
                is_valid = validate_email_address(email)
                email_data.append({
                    "Email": email,
                    "Source": link,
                    "Valid": "✅" if is_valid else "❌"
                })

        df = pd.DataFrame(email_data)
        if not df.empty:
            st.success(f"Found {len(df)} emails.")
            st.dataframe(df)
            csv = df.to_csv(index=False)
            st.download_button("Download as CSV", csv, "emails.csv", "text/csv")
        else:
            st.warning("No emails found.")
