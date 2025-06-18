import requests
from bs4 import BeautifulSoup as Bs
import pandas as pd
import streamlit as st

st.title("HTML Diagnosis")
st.write("Enter a URL to analyze whether the page is static or requires JS libraries.")

url = st.text_input("URL to analyze:", "")
if st.button("Analyze"):
    if not url:
        st.error("Please enter a valid URL.")
    else:
        if not url.lower().startswith(("http://", "https://")):
            url = "https://" + url

        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()
        except Exception as e:
            st.error(f"Error fetching the URL: {e}")
        else:
            html = response.text
            soup = Bs(html, 'lxml')

            scripts_count = len(soup.find_all('script'))
            paragraphs_count = len(soup.find_all('p'))
            headers_count = sum(len(soup.find_all(h)) for h in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            tables_count = len(soup.find_all('table'))
            text_length = len(soup.get_text(separator=" ", strip=True))
            html_length = len(html)

            if (paragraphs_count + headers_count + tables_count > 5) and scripts_count > 0:
                st.warning("Possibly JS-rendered: HTML has very little direct content.")
            else:
                st.success("Likely static: Page content is present in the initial HTML")

            if any(framework in html.lower() for framework in ['react', 'angular', 'vue']):
                st.info("Detected references to React/Angular/Vue in the HTML (may indicate JS framework)")

            st.subheader("Page Analysis Summary")
            st.write(f"HTML content length (characters): {html_length}")
            st.write(f"Text content length (characters): {text_length}")
            st.write(f"Number of <script> tags: {scripts_count}")
            st.write(f"Number of <p> tags: {paragraphs_count}")
            st.write(f"Number of header tags (h1–h6): {headers_count}")
            st.write(f"Number of <table> tags: {tables_count}")

            st.subheader("Extracted Tables")
            try:
                tables = pd.read_html(html)
            except ValueError:
                tables = []
            if tables:
                for idx, table in enumerate(tables, start=1):
                    st.markdown(f"**Table {idx}:**")
                    st.dataframe(table)
            else:
                st.write("No HTML tables found on the page.")