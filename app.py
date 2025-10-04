import streamlit as st
import feedparser

# RSS feed URL (Spreadshop products)
RSS_URL = "https://style-threadz.myspreadshop.net/1482874/products.rss?pushState=false&targetPlatform=google"

st.set_page_config(page_title="Style Threadz Products", layout="wide")

st.title("🛍️ Style Threadz Products")
st.write("Fetched directly from Spreadshop RSS Feed")

# Fetch RSS data
feed = feedparser.parse(RSS_URL)

if not feed.entries:
    st.error("⚠️ Could not fetch products. Please check the RSS URL.")
else:
    for entry in feed.entries:
        with st.container():
            cols = st.columns([1, 3])  # image | details

            # Product Image
            if "media_content" in entry and entry.media_content:
                img_url = entry.media_content[0]['url']
                cols[0].image(img_url, use_container_width=True)

            # Product Details
            cols[1].markdown(f"### [{entry.title}]({entry.link})")
            cols[1].write(entry.description)
            
            # Sometimes price is in 'summary' or custom tags
            if hasattr(entry, "summary"):
                cols[1].markdown(f"💲 **{entry.summary}**")
            
            st.divider()
            
