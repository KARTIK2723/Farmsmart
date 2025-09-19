from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import json

app = Flask(__name__)
CORS(app)

# ✅ Replace with your API key
genai.configure(api_key="AIzaSyDRKZHxENN204iyEPEy-RyVuIVak2Jl2Ss")

# ---------------- Chatbot Route ----------------
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(user_message)

        # ✅ Extract text safely
        if hasattr(response, "text") and response.text:
            ai_reply = response.text
        else:
            ai_reply = response.candidates[0].content.parts[0].text if response.candidates else "⚠️ No response"

        return jsonify({"reply": ai_reply})

    except Exception as e:
        print("Error in backend:", str(e))
        return jsonify({"error": str(e)}), 500


# ---------------- Crop Recommendation Route ----------------
# ✅ Load UP soil data
with open("soilup.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

# Convert dict → list of dicts
soil_data = [{"district": k, "soil": v} for k, v in raw_data.items()]

@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        data = request.get_json()
        location = data.get("location", "").lower().strip()
        rainfall = data.get("rainfall", "").lower().strip()

        # ✅ find soil type from dataset
        district_info = next(
            (item for item in soil_data if item["district"].lower() == location),
            None
        )

        if not district_info:
            return jsonify({"error": "District not found in database"}), 404

        soil = district_info["soil"]

        # ✅ simple crop logic (you can expand later)
        if soil == "alluvial" and rainfall == "medium":
            crop = "Wheat"
        elif soil == "black" and rainfall == "medium":
            crop = "Cotton"
        elif soil == "red" and rainfall == "low":
            crop = "Groundnut"
        elif soil == "laterite" and rainfall == "high":
            crop = "Banana"
        elif soil == "sandy" and rainfall == "low":
            crop = "Carrot"
        else:
            crop = "Pulses / mixed cropping"

        return jsonify({
            "district": district_info["district"],
            "soil": soil,
            "rainfall": rainfall,
            "crop": crop
        })

    except Exception as e:
        print("Backend Error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)