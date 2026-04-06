import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import math_service

app = Flask(__name__, static_folder='.')
CORS(app)

@app.route('/')
def home():
    # This now serving your website directly!
    return send_from_directory('.', 'index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    f1 = data.get('f1', 'x^2')
    f2 = data.get('f2', '2*x + 8')
    x_range = data.get('x_range', [-12, 12])
    
    try:
        plot_data = math_service.get_plot_data(f1, f2, x_range)
        return jsonify(plot_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
