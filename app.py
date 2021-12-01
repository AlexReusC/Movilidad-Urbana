import flask
from flask.json import jsonify
import uuid
import os
from sanAndres import City
from car import Car

games = {}

app = flask.Flask(__name__)

@app.route("/games", methods=["POST"])
def create():
    global games
    id = str(uuid.uuid4())
    games[id] = City()
    return "ok", 201, {'Location': f"/games/{id}", "Items": len(games[id].schedule.agents) - 1}

@app.route("/games/<id>", methods=["GET"])
def queryState(id):
    global model
    model = games[id]
    model.step()
    cars = []
    for car in model.schedule.agents:
        if isinstance(car, Car):
            cars.append({"x": car.exactPos[0], "y": car.exactPos[1], "theta": car.angle})
    return jsonify({"Items": cars})
app.run()

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5001)))
