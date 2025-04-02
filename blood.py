from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB Configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/blood_donor_db"
mongo = PyMongo(app)

donors = mongo.db.donors

@app.route("/register", methods=["POST"])
def register_donor():
    data = request.json
    name = data.get("name")
    blood_type = data.get("blood_type")
    contact = data.get("contact")
    location = data.get("location")

    if not all([name, blood_type, contact, location]):
        return jsonify({"error": "All fields are required"}), 400
    
    donor_id = donors.insert_one({
        "name": name,
        "blood_type": blood_type,
        "contact": contact,
        "location": location
    }).inserted_id
    
    return jsonify({"message": "Donor registered successfully", "id": str(donor_id)})

@app.route("/donors", methods=["GET"])
def get_donors():
    blood_type = request.args.get("blood_type")
    if not blood_type:
        return jsonify({"error": "Blood type is required"}), 400
    
    donor_list = list(donors.find({"blood_type": blood_type}, {"_id": 0}))
    return jsonify(donor_list)

@app.route("/donor/<id>", methods=["GET"])
def get_donor(id):
    donor = donors.find_one({"_id": ObjectId(id)})
    if donor:
        donor["_id"] = str(donor["_id"])
        return jsonify(donor)
    return jsonify({"error": "Donor not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
