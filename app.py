import streamlit as st
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# RSS URL
RSS_URL = "https://style-threadz.myspreadshop.net/1482874/products.rss?pushState=false&targetPlatform=google"

# Cache
CACHE = {
    'products': [],
    'fetched_at': None
}
CACHE_TTL = timedelta(minutes=10)

def fetch_products_from_rss():
    now = datetime.utcnow()
    if CACHE['fetched_at'] and (now - CACHE['fetched_at']) < CACHE_TTL and CACHE['products']:
        return CACHE['products']

    resp = requests.get(RSS_URL, timeout=10)
    resp.raise_for_status()
    root = ET.fromstring(resp.text)

    products = []
    for item in root.findall('.//item'):
        title = item.findtext('title') or ''
        description = item.findtext('description') or ''
        price = item.findtext('{http://base.google.com/ns/1.0}price') or ''
        image = item.findtext('{http://base.google.com/ns/1.0}image_link') or ''

        prod = {
            'title': title.strip(),
            'description': description.strip(),
            'price': price.strip(),
            'image': image.strip()
        }
        products.append(prod)

    CACHE['products'] = products
    CACHE['fetched_at'] = now
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
                        # Image clickable → redirects to stylethreadz.com
                        st.markdown(
                            f'<a href="https://stylethreadz.com" target="_blank">'
                            f'<img src="{prod["image"]}" width="150"></a>',
                            unsafe_allow_html=True
                        )
                with cols[1]:
                    st.subheader(prod['title'])
                    st.markdown(f"**Price:** {prod['price']}")
                    st.markdown(prod['description'])
                    st.markdown(f"[🔗 View Product](https://stylethreadz.com)")
                st.markdown("---")
except Exception as e:
    st.error(f"Error loading products: {e}")
