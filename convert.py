from flask import Flask, request, jsonify, send_from_directory
import requests

app = Flask(__name__)

# Free currency API
API_URL = "https://open.er-api.com/v6/latest/"

# =========================
# Serve Frontend
# =========================
@app.route("/")
def home():
    return send_from_directory(".", "index.html")

# =========================
# Currency Converter API
# =========================
@app.route("/convert")
def convert_currency():
    from_currency = request.args.get("from")
    to_currency = request.args.get("to")
    amount = request.args.get("amount")

    # Validation
    if not from_currency or not to_currency or not amount:
        return jsonify({"error": "Missing parameters"}), 400

    try:
        amount = float(amount)
    except ValueError:
        return jsonify({"error": "Invalid amount"}), 400

    # Fetch exchange rates
    response = requests.get(API_URL + from_currency.upper())
    data = response.json()

    if data.get("result") != "success":
        return jsonify({"error": "Invalid FROM currency"}), 400

    rate = data["rates"].get(to_currency.upper())
    if rate is None:
        return jsonify({"error": "Invalid TO currency"}), 400

    converted = amount * rate

    return jsonify({
        "from": from_currency.upper(),
        "to": to_currency.upper(),
        "amount": amount,
        "converted_amount": round(converted, 2)
    })

# =========================
# Run Server
# =========================
if __name__ == "__main__":
    app.run(debug=True)
