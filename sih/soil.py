import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load soil mapping once at startup
with open("soilup.json", "r", encoding="utf-8") as f:
    soil_data = json.load(f)

@app.route("/get_soil", methods=["POST"])
def get_soil():
    data = request.json
    district = data.get("district", "").strip()

    soil_type = soil_data.get(district, "Soil information not available for this district.")

    return jsonify({"district": district, "soil": soil_type})

if __name__ == "__main__":
    app.run(debug=True)
