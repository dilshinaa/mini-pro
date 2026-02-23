from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Bus Data
buses = {
    1: {
        "name": "KSRTC City Express",
        "route": "Calicut → Kozhikode Beach",
        "total_seats": 40,
        "passengers": 0
    },
    2: {
        "name": "Metro Fast Passenger",
        "route": "Calicut → Medical College",
        "total_seats": 35,
        "passengers": 0
    },
    3: {
        "name": "Town Circular",
        "route": "Calicut → Mavoor Road",
        "total_seats": 30,
        "passengers": 0
    }
}

# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Search Results Page
@app.route("/search", methods=["POST"])
def search():
    source = request.form.get("source")
    destination = request.form.get("destination")

    # Simulate arrival times
    bus_list = []
    for bus_id, bus in buses.items():
        arrival_time = random.randint(1, 10)
        bus_list.append({
            "id": bus_id,
            "name": bus["name"],
            "route": bus["route"],
            "arrival": f"Arriving in {arrival_time} mins"
        })

    return render_template("bus_list.html",
                           source=source,
                           destination=destination,
                           buses=bus_list)


# Bus Detail Page
@app.route("/bus/<int:bus_id>")
def bus_detail(bus_id):
    bus = buses.get(bus_id)

    if not bus:
        return "Bus Not Found", 404

    return render_template("bus_detail.html",
                           bus_id=bus_id,
                           bus=bus)


# API for real-time updates
@app.route("/api/bus/<int:bus_id>")
def bus_api(bus_id):
    bus = buses.get(bus_id)

    if not bus:
        return {"error": "Bus not found"}, 404

    change = random.randint(-3, 5)
    bus["passengers"] += change

    if bus["passengers"] < 0:
        bus["passengers"] = 0

    if bus["passengers"] > bus["total_seats"]:
        bus["passengers"] = bus["total_seats"]

    available = bus["total_seats"] - bus["passengers"]

    occupancy = bus["passengers"] / bus["total_seats"]

    if occupancy < 0.4:
        crowd = "Low"
    elif occupancy < 0.75:
        crowd = "Medium"
    else:
        crowd = "High"

    return {
        "passengers": bus["passengers"],
        "available": available,
        "crowd": crowd
    }


if __name__ == "__main__":
    app.run(debug=True)
   

  


    
    
             