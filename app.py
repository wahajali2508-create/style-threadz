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
        link = item.findtext('link') or ''   # 🔹 This is the Spreadshop product link
        price = item.findtext('{http://base.google.com/ns/1.0}price') or ''
        image = item.findtext('{http://base.google.com/ns/1.0}image_link') or ''

        products.append({
            'title': title.strip(),
            'link': link.strip(),   # direct redirect to Spreadshop product page
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
        # Grid layout (4 per row)
        cols_per_row = 4
        for i in range(0, len(products), cols_per_row):
            cols = st.columns(cols_per_row)
            for col, prod in zip(cols, products[i:i+cols_per_row]):
                with col:
                    # Product card
                    html = f"""
                    <div style="background:#fff; border:1px solid #ddd; border-radius:10px; 
                                padding:10px; text-align:center; margin-bottom:15px;">
                        <!-- 🔹 Image click = Spreadshop product page -->
                        <a href="{prod['link']}" target="_blank" rel="noopener noreferrer">
                            <img src="{prod['image']}" style="width:100%; border-radius:8px;" />
                        </a>
                        <h4 style="margin:8px 0; color:#333;">{prod['title']}</h4>
                        <p style="font-weight:bold; color:green; margin:5px 0;">{prod['price']}</p>
                        <!-- 🔹 Button also goes to Spreadshop product page -->
                        <a href="{prod['link']}" target="_blank" rel="noopener noreferrer"
                           style="display:inline-block; padding:6px 12px; background:#00c0ff; 
                                  color:white; border-radius:5px; text-decoration:none; font-weight:bold;">
                           View Product
                        </a>
                    </div>
                    """
                    col.markdown(html, unsafe_allow_html=True)
except Exception as e:
    st.error(f"Error loading products: {e}")

