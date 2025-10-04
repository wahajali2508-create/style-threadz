# Style-Threadz Spreadshop RSS -> Flask App

This small Flask app fetches product data from the Spreadshop RSS feed and renders a simple product grid.

## Files
- `app.py` - main Flask application (development server)
- `templates/index.html` - product listing template
- `static/styles.css` - basic styling
- `requirements.txt` - Python dependencies

## How to run locally
1. Create a Python virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate   # or `venv\Scripts\activate` on Windows
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python app.py
   ```
4. Open http://127.0.0.1:5000 in your browser.

## Notes
- The RSS URL is set to the Spreadshop feed by default. If you want a different feed, update `RSS_URL` inside `app.py`.
- For production use, run with a WSGI server like `gunicorn` and configure proper caching and error handling.
- If your environment blocks outgoing HTTP requests, the app won't be able to fetch the remote RSS feed.

