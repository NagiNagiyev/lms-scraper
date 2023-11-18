from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS extension
from scraper import scrape_data

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/scrape', methods=['POST'])
def api_scrape():
    content = request.json

    # Extract parameters from the request
    username = content.get('username')
    password = content.get('password')
    semester = content.get('semester')

    # Validate input
    if not all([username, password, semester]):
        return jsonify({"error": "Missing username, password, or semester"}), 400

    try:
        # Call your scraping function
        data = scrape_data(username, password, semester)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0')