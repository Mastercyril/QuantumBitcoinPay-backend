# ============================================
# QuantumBitcoinPay - Dell Backend Server
# Domain: quantumbitcoinpay.com
# File: qbp_server.py
# Created: 2/25/2026
# ============================================

import requests
import sqlite3
import json
from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# Live domain - no old URLs
WIX_BASE = "https://www.quantumbitcoinpay.com/_functions"
DB_PATH = r"C:\Users\josep\OneDrive\Desktop\quantumpay_ecosystem\quantumpay.db"

# ─────────────────────────────────────────
# PRICE ENDPOINTS
# ─────────────────────────────────────────

@app.route('/prices', methods=['GET'])
def get_prices():
    """Fetch live crypto prices from Wix backend"""
    try:
        r = requests.get(f"{WIX_BASE}/prices", timeout=10)
        return jsonify(r.json())
    except Exception as e:
        # Fallback: hit CoinGecko directly if Wix not ready yet
        try:
            cg = requests.get(
                "https://api.coingecko.com/api/v3/simple/price"
                "?ids=bitcoin,ethereum,litecoin,dogecoin"
                "&vs_currencies=usd&include_24hr_change=true",
                timeout=10
            )
            return jsonify({"success": True, "source": "coingecko_direct", "data": cg.json()})
        except Exception as e2:
            return jsonify({"success": False, "error": str(e2)}), 500

@app.route('/market', methods=['GET'])
def get_market():
    """Fetch global market summary"""
    try:
        r = requests.get(f"{WIX_BASE}/market", timeout=10)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ─────────────────────────────────────────
# WALLET ENDPOINTS
# ─────────────────────────────────────────

@app.route('/validate', methods=['POST'])
def validate_wallet():
    """Validate a BTC or ETH wallet address"""
    try:
        data = request.get_json()
        r = requests.post(f"{WIX_BASE}/validateWallet", json=data, timeout=10)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/wallets', methods=['GET'])
def list_wallets():
    """Read wallets from local SQLite database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cur.fetchall()]
        conn.close()
        return jsonify({"success": True, "tables": tables})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ─────────────────────────────────────────
# TRANSACTION ENDPOINTS
# ─────────────────────────────────────────

@app.route('/tx', methods=['GET'])
def lookup_tx():
    """Look up a transaction hash on BTC or ETH"""
    try:
        tx_hash = request.args.get('hash')
        network = request.args.get('network', 'BTC')
        if not tx_hash:
            return jsonify({"success": False, "error": "hash param required"}), 400
        r = requests.get(f"{WIX_BASE}/tx?hash={tx_hash}&network={network}", timeout=10)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ─────────────────────────────────────────
# STATUS / HEALTH CHECK
# ─────────────────────────────────────────

@app.route('/', methods=['GET'])
@app.route('/ping', methods=['GET'])
def ping():
    """Health check - confirm server is running"""
    return jsonify({
        "status": "ONLINE",
        "name": "QuantumBitcoinPay Dell Backend",
        "domain": "quantumbitcoinpay.com",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "endpoints": ["/prices", "/market", "/validate", "/wallets", "/tx", "/ping"]
    })

# ─────────────────────────────────────────
if __name__ == '__main__':
    print("=" * 50)
    print("  QuantumBitcoinPay Dell Server STARTING...")
    print("  URL: http://localhost:5050")
    print("  Domain: quantumbitcoinpay.com")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5050, debug=True)
