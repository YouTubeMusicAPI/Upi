from flask import Flask, render_template, request
import json
import os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    upi = request.form["upi"]
    amount = request.form["amount"]
    utr = request.form["utr"]

    data = load_data()
    data.append({
        "name": name,
        "upi": upi,
        "amount": amount,
        "utr": utr,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Pending"
    })
    save_data(data)
    return render_template("success.html")

@app.route("/admin")
def admin():
    data = load_data()
    return render_template("admin.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
  
