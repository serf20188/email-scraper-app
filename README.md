# Email Scraper App

This is a web app built with Streamlit that allows you to:
- Search Google for websites using a keyword or domain
- Scrape email addresses from those sites
- Validate them using DNS MX lookups
- Export results as CSV

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Cloud

1. Push this folder to GitHub
2. Go to https://streamlit.io/cloud
3. Connect your repo and deploy `app.py`
