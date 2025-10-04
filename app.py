from flask import Flask, render_template, send_from_directory
import requests
import xml.etree.ElementTree as ET
import os
from datetime import datetime, timedelta

app = Flask(__name__, template_folder='templates', static_folder='static')

# Change this RSS URL if needed
RSS_URL = "https://style-threadz.myspreadshop.net/1482874/products.rss?pushState=false&targetPlatform=google"

# Simple in-memory cache to avoid fetching feed on every request in development
CACHE = {
    'products': [],
    'fetched_at': None
}
CACHE_TTL = timedelta(minutes=10)  # change as needed

def fetch_products_from_rss():
    # Use cached version if fresh
    now = datetime.utcnow()
    if CACHE['fetched_at'] and (now - CACHE['fetched_at']) < CACHE_TTL and CACHE['products']:
        return CACHE['products']

    resp = requests.get(RSS_URL, timeout=10)
    resp.raise_for_status()
    root = ET.fromstring(resp.text)
    products = []
    # iterate <item> entries
    for item in root.findall('.//item'):
        title = item.findtext('title') or ''
        link = item.findtext('link') or ''
        description = item.findtext('description') or ''
        price = item.findtext('{http://base.google.com/ns/1.0}price') or ''
        image = item.findtext('{http://base.google.com/ns/1.0}image_link') or ''
        prod = {
            'title': title.strip(),
            'link': link.strip(),
            'description': description.strip(),
            'price': price.strip(),
            'image': image.strip()
        }
        products.append(prod)

    CACHE['products'] = products
    CACHE['fetched_at'] = now
    return products

@app.route('/')
def index():
    try:
        products = fetch_products_from_rss()
    except Exception as e:
        # In case of error, show friendly message and empty list
        products = []
        error = str(e)
        return render_template('index.html', products=products, error=error)
    return render_template('index.html', products=products, error=None)

@app.route('/health')
def health():
    return {'status':'ok'}

if __name__ == '__main__':
    # For local dev only. In production use gunicorn or similar.
    app.run(host='0.0.0.0', port=5000, debug=True)
