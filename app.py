import streamlit as st
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# RSS URL
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
        description = item.findtext('description') or ''
        price = item.findtext('{http://base.google.com/ns/1.0}price') or ''
        image = item.findtext('{http://base.google.com/ns/1.0}image_link') or ''

        products.append({
            'title': title.strip(),
            'link': link.strip(),   # 🔹 RSS se aaya link use ho raha hai
            'description': description.strip(),
            'price': price.strip(),
            'image': image.strip()
        })
    return products

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="Style Threadz Products", layout="wide")
st.title("🛍️ Style Threadz Products")

try:
    products = fetch_products_from_rss()
    if not products:
        st.warning("No products found.")
    else:
        for prod in products:
            with st.container():
                cols = st.columns([1, 3])
                with cols[0]:
                    if prod['image']:
                        # Image clickable → product link
                        st.markdown(
                            f'<a href="{prod["link"]}" target="_blank">'
                            f'<img src="{prod["image"]}" width="150"></a>',
                            unsafe_allow_html=True
                        )
                with cols[1]:
                    st.subheader(prod['title'])
                    st.markdown(f"**Price:** {prod['price']}")
                    st.markdown(prod['description'])
                    # 🔹 View Product → RSS link
                    st.markdown(f"[🔗 View Product]({prod['link']})")
                st.markdown("---")
except Exception as e:
    st.error(f"Error loading products: {e}")
