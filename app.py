# app.py (Streamlit)
import streamlit as st
import requests
import xml.etree.ElementTree as ET

# RSS feed URL (change if needed)
RSS_URL = "https://style-threadz.myspreadshop.net/1482874/products.rss?pushState=false&targetPlatform=google"

@st.cache_data(ttl=600)
def fetch_products_from_rss():
    resp = requests.get(RSS_URL, timeout=10)
    resp.raise_for_status()
    root = ET.fromstring(resp.text)

    products = []
    for item in root.findall('.//item'):
        title = item.findtext('title') or ''
        link = item.findtext('link') or ''
        price = item.findtext('{http://base.google.com/ns/1.0}price') or ''
        image = item.findtext('{http://base.google.com/ns/1.0}image_link') or ''

        products.append({
            "title": title.strip(),
            "link": link.strip(),
            "price": price.strip(),
            "image": image.strip()
        })
    return products

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="Style Threadz Products", layout="wide")
st.title("🛍️ Style Threadz Products")
st.caption("Products loaded from Spreadshop RSS feed — each product links to the main site below.")

try:
    products = fetch_products_from_rss()
    if not products:
        st.warning("No products found.")
    else:
        cols_per_row = 4
        for i in range(0, len(products), cols_per_row):
            cols = st.columns(cols_per_row)
            for col, prod in zip(cols, products[i:i+cols_per_row]):
                with col:
                    # show image (use container width so it fits the column)
                    if prod["image"]:
                        st.image(prod["image"], use_column_width=True)
                    st.subheader(prod["title"])
                    st.write(f"**Price:** {prod['price']}")
                    # Guaranteed clickable link to the main site under each product
                    st.markdown(
                        '<a href="https://stylethreadz.com/" target="_blank" rel="noopener noreferrer">'
                        '👉 Visit StyleThreadz</a>',
                        unsafe_allow_html=True
                    )
except Exception as e:
    st.error(f"Error loading products: {e}")

