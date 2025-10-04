import streamlit as st
import requests
import xml.etree.ElementTree as ET

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
        link = item.findtext('link') or ''   # 🔹 Yehi link spreadshop ka hota hai
        price = item.findtext('{http://base.google.com/ns/1.0}price') or ''
        image = item.findtext('{http://base.google.com/ns/1.0}image_link') or ''

        products.append({
            'title': title.strip(),
            'link': link.strip(),
            'price': price.strip(),
            'image': image.strip()
        })
    return products

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="Style-Threadz Products", layout="wide")
st.title("🛍️ Style-Threadz Products")
st.caption("Products loaded from Spreadshop RSS feed.")

try:
    products = fetch_products_from_rss()
    if not products:
        st.warning("No products found.")
    else:
        # Grid of products
        cols_per_row = 4
        for i in range(0, len(products), cols_per_row):
            cols = st.columns(cols_per_row)
            for col, prod in zip(cols, products[i:i+cols_per_row]):
                with col:
                    # Product card with link redirect
                    st.markdown(
                        f"""
                        <div style="background-color:#1e1e1e;
                                    border-radius:10px;
                                    padding:10px;
                                    text-align:center;
                                    margin-bottom:15px;
                                    box-shadow:0 0 5px rgba(0,0,0,0.3);">
                            <a href="{prod['link']}" target="_blank">
                                <img src="{prod['image']}" style="width:100%; border-radius:8px;" />
                            </a>
                            <p style="font-weight:bold; margin:8px 0; color:white;">{prod['price']}</p>
                            <a href="{prod['link']}" target="_blank" style="color:#00c0ff; text-decoration:none; font-weight:bold;">View Product</a>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
except Exception as e:
    st.error(f"Error loading products: {e}")
