# Check-for-JS
Code checks if HTML page on any given URL is static or if there is JavaScript rendering
  This is done by running a couple of diagnistics:
    counts the length of direct content available in the initial page load (paragraphs, headers, tables) and if there is any scripting that leads to content after page loads
    also checks for references to popular JS frameworks such as React Angular and Vue
  Python script scrapes any available tables
  User available interface available through Streamlit
Note:
  Highly dynamic pages may be flagged as static, but may have content that is available after the initial page load
